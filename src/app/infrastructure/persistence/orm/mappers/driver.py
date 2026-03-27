"""Módulo que define el vínculo entre la entidad de dominio Driver y su tabla
de persistencia."""

# Librerías Externas.
import datetime as dt

from sqlalchemy import Connection, event
from sqlalchemy.orm import Mapper, registry

# Librerías Internas.
from app.domain.entities.driver import Driver

from app.infrastructure.persistence.orm.tables.driver import drivers_table


def start_drivers_mapper(registry: registry) -> None:
    """Función que centraliza la creación del vínculo entre tabla de
    persistencia y entidad de dominio.
    
    Args:
    ----------
    registry:
        Entidad sobre la cual se registrará el mapper."""
    
    registry.map_imperatively(
        Driver,
        drivers_table,
        properties = {
            "_id": drivers_table.c.id,
            "_status": drivers_table.c.status,
            "_last_delivery": drivers_table.c.last_delivery,
            "_created_at": drivers_table.c.created_at,
            "_updated_at": drivers_table.c.updated_at
        }
    )

    @event.listens_for(Driver, "before_insert")
    def generate_audit_dates(mapper: Mapper[Driver], connection: Connection, target: Driver) -> None:
        """Función que se encarga, cada que se vaya a insertar una nueva fila
        en la tabla de persistencia, de registrar fechas auditables de transacción.
        
        Args:
        ----------
        mapper: Mapper[Driver].
        
        connection: Connection.

        target: Driver.
            Entidad que actualizará o sobre la cual configurará valores
            previo a la inserción en BD."""
        
        target._created_at = dt.datetime.now()
        target._updated_at = dt.datetime.now()

    @event.listens_for(Driver, "before_update")
    def generate_audit_dates(mapper: Mapper[Driver], connection: Connection, target: Driver) -> None:
        """Función que se encarga, cada que se vaya a actualizar una fila
        en la tabla de persistencia, de registrar fechas auditables de transacción.
        
        Args:
        ----------
        mapper: Mapper[Driver].
            Mapper que contiene el vínculo entre entidad de dominio y tabla de
            persistencia.
        
        connection: Connection.
            Conexión activa que existe hacia base de datos.

        target: Driver.
            Entidad que actualizará o sobre la cual configurará valores
            previo a la inserción en BD."""
        
        target._updated_at = dt.datetime.now()
