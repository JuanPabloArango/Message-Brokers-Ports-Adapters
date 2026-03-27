"""Módulo que contiene la definición del comando base para poder encapsular
todos los comandos en un solo punto para cuando hablemos de 'Mensajes'."""

# Librerías Externas.
from dataclasses import dataclass


@dataclass(frozen = True)
class Command:
    """Clase base que sirve como SuperClass para todos los Commands
    en nuestra aplicación."""

    ...
