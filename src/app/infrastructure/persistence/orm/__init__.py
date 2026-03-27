"""Módulo que encapsula todo lo relacionado con el ORM para servir como
único punto de encapsulamiento."""

# Librerías Externas.
from typing import Type
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker

# Librerías Internas.
from app.settings import Settings

from app.infrastructure.persistence.orm.base import metadata, mapper_registry
from app.infrastructure.persistence.orm.mappers.driver import start_drivers_mapper
from app.infrastructure.persistence.orm.mappers.sender import start_senders_mapper
from app.infrastructure.persistence.orm.mappers.package import start_packages_mapper


def start_mappers() -> None:
    """Función que se encarga de centralizar el mapeo de entidades
    a filas de tablas y viceversa."""

    start_drivers_mapper(mapper_registry)
    start_senders_mapper(mapper_registry)
    start_packages_mapper(mapper_registry)


def get_session_factory() -> Type[Session]:
    """Función que se encarga de construir sesiones de conexión a las BDs.
    
    Returns:
    ----------
    Type[Session].
        Factory que construye sesiones de conexión a BD."""

    configured_url = Settings.get_database_url()

    engine: Engine = create_engine(url = configured_url, echo = True,
                                   pool_size = 10, max_overflow = 10,
                                   pool_timeout = 5, pool_recycle = 1800)
    metadata.create_all(engine)

    session_factory: Type[Session] = sessionmaker(bind = engine)
    return session_factory
