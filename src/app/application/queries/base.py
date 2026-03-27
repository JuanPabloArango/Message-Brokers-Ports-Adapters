"""Módulo que contiene la definición de la query base para poder encapsular
todas las queries en un solo cuando hablemos de CQRS."""

# Librerías Externas.
from dataclasses import dataclass


@dataclass(frozen = True)
class Query:
    """Clase base que sirve como SuperClass para todas las Queries
    en nuestra aplicación."""

    ...
