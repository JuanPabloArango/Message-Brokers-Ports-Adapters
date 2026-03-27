"""Módulo que define la construcción de la tabla donde almacenaremos
entidades Package."""

# Librerías Externas.
from sqlalchemy import Table, Column, ForeignKey, DateTime

# Librerías Internas.
from app.infrastructure.persistence.orm.base import metadata

from app.infrastructure.persistence.orm.custom_types.id import CustomIDType
from app.infrastructure.persistence.orm.custom_types.package_status import CustomPackageStatus


packages_table = Table(
    "packages",
    metadata,
    Column("id", CustomIDType, primary_key = True),
    Column("sender_id", CustomIDType, ForeignKey("senders.id"), unique = False, nullable = False),
    Column("driver_id", CustomIDType, ForeignKey("drivers.id"), unique = False, nullable = True),
    Column("status", CustomPackageStatus, nullable = False, unique = False),
    Column("created_at", DateTime, unique = False, nullable = False),
    Column("updated_at", DateTime, unique = False, nullable = False),
)
