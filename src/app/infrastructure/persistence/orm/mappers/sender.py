"""Módulo que define el vínculo entre la entidad de dominio Sender y su tabla
de persistencia."""

# Librerías Externas.
import datetime as dt

from sqlalchemy import Connection, event
from sqlalchemy.orm import Mapper, registry

# Librerías Internas.
from app.domain.entities.sender import Sender

from app.infrastructure.persistence.orm.tables.sender import sender_table


def start_senders_mapper(registry: registry) -> None:
    """Función que centraliza la creación del vínculo entre tabla de
    persistencia y entidad de dominio.
    
    Args:
    ----------
    registry:
        Entidad sobre la cual se registrará el mapper."""
    
    registry.map_imperatively(
        Sender,
        sender_table,
        properties = {
            "_id": sender_table.c.id,
            "_status": sender_table.c.status,
            "_created_at": sender_table.c.created_at,
            "_updated_at": sender_table.c.updated_at
        }
    )

    @event.listens_for(Sender, "before_insert")
    def generate_audit_dates(mapper: Mapper[Sender], connection: Connection, target: Sender) -> None:
        """Función que se encarga, cada que se vaya a insertar una nueva fila
        en la tabla de persistencia, de registrar fechas auditables de transacción.
        
        Args:
        ----------
        mapper: Mapper[Sender].
        
        connection: Connection.

        target: Sender.
            Entidad que actualizará o sobre la cual configurará valores
            previo a la inserción en BD."""
        
        target._created_at = dt.datetime.now()
        target._updated_at = dt.datetime.now()

    @event.listens_for(Sender, "before_update")
    def generate_audit_dates(mapper: Mapper[Sender], connection: Connection, target: Sender) -> None:
        """Función que se encarga, cada que se vaya a actualizar una fila
        en la tabla de persistencia, de registrar fechas auditables de transacción.
        
        Args:
        ----------
        mapper: Mapper[Sender].
            Mapper que contiene el vínculo entre entidad de dominio y tabla de
            persistencia.
        
        connection: Connection.
            Conexión activa que existe hacia base de datos.

        target: Sender.
            Entidad que actualizará o sobre la cual configurará valores
            previo a la inserción en BD."""
        
        target._updated_at = dt.datetime.now()
