"""Módulo que contiene la definición base del Registry para ligar nuestras
entidades de dominio a tablas de persistencia."""

# Librerías Externas.
from sqlalchemy.orm import registry


mapper_registry = registry()
metadata = mapper_registry.metadata
