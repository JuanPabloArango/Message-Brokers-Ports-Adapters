"""Módulo que define el comando que usaremos para la creación de Senders."""

# Librerías Externas.
from dataclasses import dataclass

# Librerías Internas.
from app.application.commands.base import Command


@dataclass(frozen = True)
class CreateSender(Command):
    """Clase que contiene la información necesaria que construye el
    comando de creación de una entidad de dominio Sender."""

    ...
