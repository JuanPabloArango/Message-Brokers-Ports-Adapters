"""Módulo que define la construcción de la tabla donde almacenaremos
entidades Sender."""

# Librerías Externas.
from sqlalchemy import Table, Column, DateTime

# Librerías Internas.
from app.infrastructure.persistence.orm.base import metadata

from app.infrastructure.persistence.orm.custom_types.id import CustomIDType
from app.infrastructure.persistence.orm.custom_types.sender_status import CustomSenderStatus


sender_table = Table(
    "senders",
    metadata,
    Column("id", CustomIDType, primary_key = True),
    Column("status", CustomSenderStatus, nullable = False, unique = False),
    Column("created_at", DateTime, unique = False, nullable = False),
    Column("updated_at", DateTime, unique = False, nullable = False),
)
