"""Módulo que define el comando que usaremos para la creación de Drivers."""

# Librerías Externas.
from typing import Optional

from dataclasses import dataclass

# Librerías Internas.
from app.application.commands.base import Command


@dataclass(frozen = True)
class CreateDriver(Command):
    """Clase que contiene la información necesaria que construye el
    comando de creación de una entidad de dominio Driver."""

    last_delivery: Optional[str] = None
