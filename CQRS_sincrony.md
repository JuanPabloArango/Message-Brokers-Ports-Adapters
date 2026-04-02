# CQRS: Read Repository con PyMongo

Este documento explica cómo implementar un **Read Repository separado con PyMongo** en un proyecto CQRS, y cómo mantenerlo sincronizado con el Write Model tanto de forma **síncrona** como **asíncrona**.

---

## Tabla de contenidos

1. [Contexto](#contexto)
2. [Por qué un Read Repository separado](#por-qué-un-read-repository-separado)
3. [Read Model en MongoDB](#read-model-en-mongodb)
4. [Implementación del Read Repository](#implementación-del-read-repository)
5. [Sincronización síncrona](#sincronización-síncrona)
6. [Sincronización asíncrona](#sincronización-asíncrona)
7. [Comparación entre ambos enfoques](#comparación-entre-ambos-enfoques)

---

## Contexto

Este proyecto usa **CQRS** con:

- **Write side**: SQLAlchemy + PostgreSQL — modela el dominio con sus invariantes, usa UoW + repositorios.
- **Query side**: actualmente, los queries también pasan por el mismo repositorio SQL.

El objetivo es introducir un **Read Repository en MongoDB** para los queries, optimizado para lectura, con documentos desnormalizados y sin lógica de negocio.

```
Write Side (SQLAlchemy / PostgreSQL)
     │
     │  Domain Events
     ▼
Read Side (PyMongo / MongoDB)
     │
     │  Queries
     ▼
Query Handlers → HTTP Response
```

---

## Por qué un Read Repository separado

| Aspecto | Write Repository (SQL) | Read Repository (Mongo) |
|---|---|---|
| Propósito | Garantizar invariantes de dominio | Servir vistas optimizadas |
| Modelo | Normalizado (entidades separadas) | Desnormalizado (documentos planos) |
| Acceso | UoW + transacciones | Solo lectura directa |
| Schema | Estricto (tablas relacionales) | Flexible (documentos JSON) |
| Escalado | Vertical | Horizontal (read replicas) |

El Read Model no replica las entidades de dominio: **proyecta** los datos en la forma exacta que necesita la vista.

---

## Read Model en MongoDB

En lugar de guardar un `Sender` con su lógica de dominio, el documento en MongoDB es una proyección plana:

```json
// Colección: senders_read
{
  "_id": "a3f1c2d4-...",
  "status": "VERIFIED",
  "created_at": "2026-03-30T10:00:00Z",
  "updated_at": "2026-03-30T12:00:00Z",
  "total_packages": 3,
  "pending_packages": 1
}
```

El Read Model puede incluir datos agregados o desnormalizados que serían costosos de calcular en tiempo de consulta.

---

## Implementación del Read Repository

### 1. Interfaz (Port)

Define el contrato del Read Repository como un puerto en la capa de aplicación:

```python
# src/app/application/ports/persistence/repositories/sender_read_repository.py

from abc import ABC, abstractmethod
from typing import Optional, List
from src.app.application.dtos.sender import SenderDTO
from src.app.application.ports.persistence.criteria import Criteria


class SenderReadRepositoryPort(ABC):

    @abstractmethod
    def get(self, sender_id: str) -> Optional[SenderDTO]:
        ...

    @abstractmethod
    def list_all(self, criteria: Criteria) -> List[SenderDTO]:
        ...

    @abstractmethod
    def save(self, dto: SenderDTO) -> None:
        """Upsert del documento en el read store."""
        ...

    @abstractmethod
    def update_status(self, sender_id: str, new_status: str) -> None:
        """Actualización parcial sin recargar toda la entidad."""
        ...
```

### 2. Adaptador (PyMongo)

Implementación concreta con PyMongo. El documento en Mongo refleja exactamente el `SenderDTO`:

```python
# src/app/infrastructure/persistence/repository/mongo/sender_read_repository.py

from typing import Optional, List
from pymongo.collection import Collection
from src.app.application.ports.persistence.repositories.sender_read_repository import (
    SenderReadRepositoryPort,
)
from src.app.application.dtos.sender import SenderDTO
from src.app.application.ports.persistence.criteria import Criteria, Operator


OPERATOR_MAP = {
    Operator.EQ: "$eq",
    Operator.NEQ: "$ne",
    Operator.GT: "$gt",
    Operator.GTE: "$gte",
    Operator.LT: "$lt",
    Operator.LTE: "$lte",
    Operator.IN: "$in",
}


class MongoSenderReadRepository(SenderReadRepositoryPort):

    def __init__(self, collection: Collection):
        self._col = collection

    def get(self, sender_id: str) -> Optional[SenderDTO]:
        doc = self._col.find_one({"_id": sender_id})
        if not doc:
            return None
        return self._to_dto(doc)

    def list_all(self, criteria: Criteria) -> List[SenderDTO]:
        mongo_filter = self._build_filter(criteria)
        sort_field = criteria.pagination.order_by or "created_at"
        sort_dir = 1 if criteria.pagination.order_dir == "asc" else -1

        cursor = (
            self._col.find(mongo_filter)
            .sort(sort_field, sort_dir)
            .skip(criteria.pagination.offset)
            .limit(criteria.pagination.limit)
        )
        return [self._to_dto(doc) for doc in cursor]

    def save(self, dto: SenderDTO) -> None:
        # upsert: inserta si no existe, reemplaza si ya existe
        self._col.replace_one(
            {"_id": dto.id},
            {
                "_id": dto.id,
                "status": dto.status,
                "created_at": dto.created_at,
                "updated_at": dto.updated_at,
            },
            upsert=True,
        )

    def update_status(self, sender_id: str, new_status: str) -> None:
        import datetime as dt
        self._col.update_one(
            {"_id": sender_id},
            {"$set": {"status": new_status, "updated_at": dt.datetime.utcnow()}},
        )

    # ------------------------------------------------------------------ #

    def _build_filter(self, criteria: Criteria) -> dict:
        mongo_filter = {}
        for f in criteria.filters:
            op = OPERATOR_MAP.get(f.operator, "$eq")
            mongo_filter[f.field] = {op: f.value}
        return mongo_filter

    @staticmethod
    def _to_dto(doc: dict) -> SenderDTO:
        return SenderDTO(
            id=doc["_id"],
            status=doc["status"],
            created_at=doc["created_at"],
            updated_at=doc["updated_at"],
        )
```

### 3. Query Handler usando el Read Repository

Los Query Handlers dejan de depender del `UnitOfWorkPort` y pasan a usar directamente el Read Repository:

```python
# src/app/application/query_handlers/get_sender.py

from typing import Union
from src.app.application.queries.get_sender_by_id import GetSenderQuery
from src.app.application.dtos.sender import SenderDTO
from src.app.application.ports.persistence.repositories.sender_read_repository import (
    SenderReadRepositoryPort,
)
from src.app.application.exceptions import SenderNotFound


class GetSenderHandler:

    def __init__(self, read_repo: SenderReadRepositoryPort):
        self._read_repo = read_repo

    def handle(self, query: GetSenderQuery) -> SenderDTO:
        sender = self._read_repo.get(query.sender_id)
        if not sender:
            raise SenderNotFound(f"El Sender con ID {query.sender_id} no existe.")
        return sender
```

---

## Sincronización síncrona

La sincronización síncrona ocurre **dentro del mismo proceso**, inmediatamente después de que el Command Handler escribe en el Write Store. El Read Store se actualiza en la misma llamada HTTP.

### Flujo

```
HTTP Request
    │
    ▼
Command Handler
    ├─ Escribe en PostgreSQL (Write Store)
    ├─ Emite Domain Events (in-memory)
    │
    ▼
Event Dispatcher (síncrono)
    │
    ▼
Projection Handler
    └─ Escribe en MongoDB (Read Store)
    │
    ▼
HTTP Response
```

### Implementación paso a paso

#### Paso 1: Eventos de dominio

```python
# src/app/domain/events.py

from dataclasses import dataclass


@dataclass(frozen=True)
class DomainEvent:
    pass


@dataclass(frozen=True)
class SenderCreated(DomainEvent):
    sender_id: str
    status: str


@dataclass(frozen=True)
class SenderVerified(DomainEvent):
    sender_id: str
```

#### Paso 2: Agregado con soporte de eventos

El agregado acumula eventos en una lista interna. El repositorio (o UoW) los recoge al hacer commit:

```python
# src/app/domain/entities/sender.py  (fragmento)

from src.app.domain.events import SenderCreated, SenderVerified


class Sender:

    def __init__(self, id, status=SenderStatus.UNVERIFIED):
        self.id = id
        self.status = status
        self._events: list = []

    @classmethod
    def create(cls, sender_id: str) -> "Sender":
        sender = cls(id=ID(sender_id))
        sender._events.append(
            SenderCreated(sender_id=sender_id, status=SenderStatus.UNVERIFIED.value)
        )
        return sender

    def verify(self) -> None:
        if self.status == SenderStatus.VERIFIED:
            raise SenderAlreadyVerified(...)
        self.status = SenderStatus.VERIFIED
        self._events.append(SenderVerified(sender_id=self.id.value))

    def collect_events(self) -> list:
        events = list(self._events)
        self._events.clear()
        return events
```

#### Paso 3: Projection Handler

El Projection Handler escucha el evento y actualiza el Read Store. No tiene lógica de negocio:

```python
# src/app/application/projections/sender_projection.py

from src.app.domain.events import SenderCreated, SenderVerified
from src.app.application.ports.persistence.repositories.sender_read_repository import (
    SenderReadRepositoryPort,
)
from src.app.application.dtos.sender import SenderDTO
import datetime as dt


class SenderProjection:

    def __init__(self, read_repo: SenderReadRepositoryPort):
        self._read_repo = read_repo

    def handle_created(self, event: SenderCreated) -> None:
        dto = SenderDTO(
            id=event.sender_id,
            status=event.status,
            created_at=dt.datetime.utcnow(),
            updated_at=dt.datetime.utcnow(),
        )
        self._read_repo.save(dto)

    def handle_verified(self, event: SenderVerified) -> None:
        self._read_repo.update_status(
            sender_id=event.sender_id,
            new_status="VERIFIED",
        )
```

#### Paso 4: Event Dispatcher síncrono

Despacha eventos en memoria. Los suscriptores se registran en el bootstrap:

```python
# src/app/infrastructure/event_dispatcher.py

from typing import Callable, Dict, List, Type
from src.app.domain.events import DomainEvent


class SyncEventDispatcher:

    def __init__(self):
        self._handlers: Dict[Type[DomainEvent], List[Callable]] = {}

    def subscribe(self, event_type: Type[DomainEvent], handler: Callable) -> None:
        self._handlers.setdefault(event_type, []).append(handler)

    def dispatch(self, event: DomainEvent) -> None:
        for handler in self._handlers.get(type(event), []):
            handler(event)
```

#### Paso 5: Command Handler publica eventos

Tras el commit en SQL, el Command Handler recoge los eventos del agregado y los despacha:

```python
# src/app/application/command_handlers/create_sender.py

from src.app.application.commands.create_sender import CreateSenderCommand
from src.app.application.ports.persistence.uow import UnitOfWorkPort
from src.app.infrastructure.event_dispatcher import SyncEventDispatcher
from src.app.domain.entities.sender import Sender


class CreateSenderHandler:

    def __init__(
        self,
        unit_of_work: UnitOfWorkPort,
        dispatcher: SyncEventDispatcher,
    ):
        self._unit_of_work = unit_of_work
        self._dispatcher = dispatcher

    def handle(self, command: CreateSenderCommand) -> str:
        with self._unit_of_work as uow:
            new_sender = Sender.create(sender_id=command.sender_id)
            uow.sender_repository.save(sender=new_sender)
            uow.commit()  # Persiste en SQL

        # Fuera de la transacción SQL: despacha eventos
        for event in new_sender.collect_events():
            self._dispatcher.dispatch(event)  # Actualiza MongoDB

        return new_sender.id.value
```

#### Paso 6: Bootstrap — registrar proyecciones

```python
# src/app/infrastructure/bootstrap.py  (fragmento)

from pymongo import MongoClient
from src.app.infrastructure.event_dispatcher import SyncEventDispatcher
from src.app.infrastructure.persistence.repository.mongo.sender_read_repository import (
    MongoSenderReadRepository,
)
from src.app.application.projections.sender_projection import SenderProjection
from src.app.domain.events import SenderCreated, SenderVerified


def bootstrap(app):
    # --- Write side ---
    session_factory = get_session_factory()
    unit_of_work = SQLUnitOfWorkAdapter(session_factory=session_factory)

    # --- Read side ---
    mongo_client = MongoClient(os.getenv("MONGO_URL", "mongodb://localhost:27017"))
    mongo_db = mongo_client["message_broker_read"]
    sender_read_repo = MongoSenderReadRepository(
        collection=mongo_db["senders_read"]
    )

    # --- Dispatcher ---
    dispatcher = SyncEventDispatcher()
    sender_projection = SenderProjection(read_repo=sender_read_repo)
    dispatcher.subscribe(SenderCreated, sender_projection.handle_created)
    dispatcher.subscribe(SenderVerified, sender_projection.handle_verified)

    # --- Handlers ---
    SenderBlueprint.add_url_rule(
        rule="",
        view_func=SenderView.as_view(
            name="sender_view",
            list_handler=ListSendersHandler(sender_read_repo),      # Lee de Mongo
            create_handler=CreateSenderHandler(unit_of_work, dispatcher),  # Escribe en SQL
        ),
    )
```

---

## Sincronización asíncrona

La sincronización asíncrona desacopla el Write Store del Read Store. El Command Handler publica el evento en un **bus de mensajes** externo (Pub/Sub, RabbitMQ, Kafka, etc.). Un **worker** separado consume los eventos y actualiza MongoDB.

### Flujo

```
HTTP Request
    │
    ▼
Command Handler
    ├─ Escribe en PostgreSQL (Write Store)    ─── commit ───►  PostgreSQL
    └─ Publica evento en Pub/Sub              ─── publish ──►  Pub/Sub Topic
    │
    ▼
HTTP Response (202 Accepted)          ← Respuesta ANTES de que Mongo se actualice


                                        Pub/Sub Topic
                                             │
                                             │  (worker separado)
                                             ▼
                                    Projection Worker
                                             │
                                             ▼
                                         MongoDB (Read Store)
```

> **Nota**: Con sincronización asíncrona existe una ventana de **eventual consistency**: inmediatamente después de crear un Sender, el Read Store puede no reflejarlo todavía.

### Implementación paso a paso

#### Paso 1: Publisher de eventos (Puerto)

```python
# src/app/application/ports/event_publisher.py

from abc import ABC, abstractmethod
from src.app.domain.events import DomainEvent


class EventPublisherPort(ABC):

    @abstractmethod
    def publish(self, event: DomainEvent) -> None:
        ...
```

#### Paso 2: Adaptador Google Cloud Pub/Sub

```python
# src/app/infrastructure/pubsub/publisher.py

import json
from google.cloud import pubsub_v1
from src.app.application.ports.event_publisher import EventPublisherPort
from src.app.domain.events import DomainEvent


class PubSubEventPublisher(EventPublisherPort):

    def __init__(self, project_id: str, topic_id: str):
        self._client = pubsub_v1.PublisherClient()
        self._topic_path = self._client.topic_path(project_id, topic_id)

    def publish(self, event: DomainEvent) -> None:
        payload = {
            "event_type": type(event).__name__,
            "data": event.__dict__,
        }
        message_bytes = json.dumps(payload).encode("utf-8")
        future = self._client.publish(self._topic_path, data=message_bytes)
        future.result()  # Espera confirmación del broker
```

#### Paso 3: Command Handler publica en Pub/Sub

```python
# src/app/application/command_handlers/create_sender.py

from src.app.application.commands.create_sender import CreateSenderCommand
from src.app.application.ports.persistence.uow import UnitOfWorkPort
from src.app.application.ports.event_publisher import EventPublisherPort
from src.app.domain.entities.sender import Sender


class CreateSenderHandler:

    def __init__(
        self,
        unit_of_work: UnitOfWorkPort,
        event_publisher: EventPublisherPort,
    ):
        self._unit_of_work = unit_of_work
        self._event_publisher = event_publisher

    def handle(self, command: CreateSenderCommand) -> str:
        with self._unit_of_work as uow:
            new_sender = Sender.create(sender_id=command.sender_id)
            uow.sender_repository.save(sender=new_sender)
            uow.commit()

        # Publica en Pub/Sub — el worker actualiza MongoDB después
        for event in new_sender.collect_events():
            self._event_publisher.publish(event)

        return new_sender.id.value
```

#### Paso 4: Worker consumidor (proceso separado)

El worker se ejecuta de forma independiente. Suscribe a Pub/Sub y proyecta los eventos en MongoDB:

```python
# src/app/workers/projection_worker.py

import json
from google.cloud import pubsub_v1
from pymongo import MongoClient
from src.app.application.projections.sender_projection import SenderProjection
from src.app.infrastructure.persistence.repository.mongo.sender_read_repository import (
    MongoSenderReadRepository,
)
from src.app.domain.events import SenderCreated, SenderVerified


EVENT_MAP = {
    "SenderCreated": SenderCreated,
    "SenderVerified": SenderVerified,
}


def build_projection() -> SenderProjection:
    mongo_client = MongoClient("mongodb://localhost:27017")
    read_repo = MongoSenderReadRepository(
        collection=mongo_client["message_broker_read"]["senders_read"]
    )
    return SenderProjection(read_repo=read_repo)


def callback(message: pubsub_v1.subscriber.message.Message) -> None:
    payload = json.loads(message.data.decode("utf-8"))
    event_type_name = payload["event_type"]
    event_data = payload["data"]

    event_cls = EVENT_MAP.get(event_type_name)
    if not event_cls:
        message.nack()
        return

    event = event_cls(**event_data)
    projection = build_projection()

    if isinstance(event, SenderCreated):
        projection.handle_created(event)
    elif isinstance(event, SenderVerified):
        projection.handle_verified(event)

    message.ack()


def run():
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(
        "my-project", "sender-events-sub"
    )
    streaming_pull = subscriber.subscribe(subscription_path, callback=callback)
    print("Worker escuchando eventos...")
    streaming_pull.result()


if __name__ == "__main__":
    run()
```

#### Paso 5: Versión con asyncio (worker asíncrono)

Si el worker necesita mayor throughput, puede usar `asyncio` con un subscriber asíncrono:

```python
# src/app/workers/async_projection_worker.py

import asyncio
import json
from motor.motor_asyncio import AsyncIOMotorClient  # PyMongo async
from src.app.domain.events import SenderCreated, SenderVerified
import datetime as dt


EVENT_MAP = {
    "SenderCreated": SenderCreated,
    "SenderVerified": SenderVerified,
}


async def project_event(event, collection) -> None:
    if isinstance(event, SenderCreated):
        await collection.replace_one(
            {"_id": event.sender_id},
            {
                "_id": event.sender_id,
                "status": event.status,
                "created_at": dt.datetime.utcnow(),
                "updated_at": dt.datetime.utcnow(),
            },
            upsert=True,
        )
    elif isinstance(event, SenderVerified):
        await collection.update_one(
            {"_id": event.sender_id},
            {"$set": {"status": "VERIFIED", "updated_at": dt.datetime.utcnow()}},
        )


async def process_message(raw_message: bytes, collection) -> None:
    payload = json.loads(raw_message)
    event_cls = EVENT_MAP.get(payload["event_type"])
    if event_cls:
        event = event_cls(**payload["data"])
        await project_event(event, collection)


async def run():
    mongo = AsyncIOMotorClient("mongodb://localhost:27017")
    collection = mongo["message_broker_read"]["senders_read"]

    # Aquí iría la integración con el subscriber asíncrono (aiormq, aio-pika, etc.)
    # Este loop simula la recepción de mensajes
    print("Worker asíncrono escuchando...")
    while True:
        await asyncio.sleep(1)


if __name__ == "__main__":
    asyncio.run(run())
```

---

## Comparación entre ambos enfoques

| Criterio | Síncrono | Asíncrono |
|---|---|---|
| **Consistencia** | Inmediata (strong consistency) | Eventual (eventual consistency) |
| **Acoplamiento** | Alto (mismo proceso) | Bajo (procesos independientes) |
| **Complejidad** | Baja | Alta (worker, broker, retry logic) |
| **Tolerancia a fallos** | Si Mongo falla, el request falla | Si Mongo falla, el worker reintenta |
| **Escalabilidad** | Limitada (mismo proceso HTTP) | Alta (workers independientes) |
| **Latencia de lectura** | 0ms de retraso | Puede haber segundos de retraso |
| **Orden garantizado** | Sí (secuencial) | Depende del broker |
| **Uso recomendado** | MVPs, sistemas pequeños | Sistemas con alta carga de escritura |

### Cuándo elegir cada uno

**Síncrono** cuando:
- El sistema es pequeño o en etapa temprana.
- La consistencia inmediata es un requisito del negocio.
- No quieres añadir infraestructura de mensajería.

**Asíncrono** cuando:
- El Read Store puede tolerar datos ligeramente desactualizados.
- El volumen de escrituras es alto y no quieres bloquear el HTTP response.
- Necesitas escalar el procesamiento de proyecciones independientemente.
- Quieres resiliencia: si MongoDB cae, los mensajes no se pierden (están en el broker).
