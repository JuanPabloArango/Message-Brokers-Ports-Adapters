"""Módulo que contiene la definición de una query para listar, según criterios
indicados por el usuario, Drivers."""

# Librerías Externas.
from dataclasses import dataclass

# Librerías Internas.
from app.application.queries.base import Query
from app.application.ports.persistence.criteria import Criteria


@dataclass(frozen = True)
class ListDriversQuery(Query):
    """Clase que define y encapsula los criterios de búsqueda."""

    criteria: Criteria

    def __post_init__(self) -> None:
        """Método dunder ara aplicar un poco de seguridad y validación."""

        if not isinstance(self.criteria, Criteria):
            raise ValueError("Para queries de búsqueda genérica solo soportamos objetos de tipo 'Criteria'.")