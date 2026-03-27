"""Módulo que define la construcción de la tabla donde almacenaremos
entidades Driver."""

# Librerías Externas.
from sqlalchemy import Table, Column, DateTime

# Librerías Internas.
from app.infrastructure.persistence.orm.base import metadata

from app.infrastructure.persistence.orm.custom_types.id import CustomIDType
from app.infrastructure.persistence.orm.custom_types.delivery_date import CustomDeliveryDate
from app.infrastructure.persistence.orm.custom_types.driver_status import CustomDriverStatus


drivers_table = Table(
    "drivers",
    metadata,
    Column("id", CustomIDType, primary_key = True),
    Column("status", CustomDriverStatus, nullable = False, unique = False),
    Column("last_delivery", CustomDeliveryDate, nullable = True, unique = False),
    Column("created_at", DateTime, unique = False, nullable = False),
    Column("updated_at", DateTime, unique = False, nullable = False),
)
