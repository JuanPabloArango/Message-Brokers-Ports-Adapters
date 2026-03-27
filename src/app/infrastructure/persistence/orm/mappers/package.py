"""Módulo que define el vínculo entre la entidad de dominio Package y su tabla
de persistencia."""

# Librerías Externas.
import datetime as dt

from sqlalchemy import Connection, event
from sqlalchemy.orm import Mapper, registry

# Librerías Internas.
from app.domain.entities.package import Package

from app.infrastructure.persistence.orm.tables.package import packages_table


def start_packages_mapper(registry: registry) -> None:
    """Función que centraliza la creación del vínculo entre tabla de
    persistencia y entidad de dominio.
    
    Args:
    ----------
    registry:
        Entidad sobre la cual se registrará el mapper."""
    
    registry.map_imperatively(
        Package,
        packages_table,
        properties = {
            "_id": packages_table.c.id,
            "_sender_id": packages_table.c.sender_id,
            "_driver_id": packages_table.c.driver_id,
            "_status": packages_table.c.status,
            "_created_at": packages_table.c.created_at,
            "_updated_at": packages_table.c.updated_at,
        }
    )

    @event.listens_for(Package, "before_insert")
    def generate_audit_dates(mapper: Mapper[Package], connection: Connection, target: Package) -> None:
        """Función que se encarga, cada que se vaya a insertar una nueva fila
        en la tabla de persistencia, de registrar fechas auditables de transacción.
        
        Args:
        ----------
        mapper: Mapper[Package].
        
        connection: Connection.

        target: Package.
            Entidad que actualizará o sobre la cual configurará valores
            previo a la inserción en BD."""
        
        target._created_at = dt.datetime.now()
        target._updated_at = dt.datetime.now()

    @event.listens_for(Package, "before_update")
    def generate_audit_dates(mapper: Mapper[Package], connection: Connection, target: Package) -> None:
        """Función que se encarga, cada que se vaya a actualizar una fila
        en la tabla de persistencia, de registrar fechas auditables de transacción.
        
        Args:
        ----------
        mapper: Mapper[Package].
            Mapper que contiene el vínculo entre entidad de dominio y tabla de
            persistencia.
        
        connection: Connection.
            Conexión activa que existe hacia base de datos.

        target: Package.
            Entidad que actualizará o sobre la cual configurará valores
            previo a la inserción en BD."""
        
        target._updated_at = dt.datetime.now()

