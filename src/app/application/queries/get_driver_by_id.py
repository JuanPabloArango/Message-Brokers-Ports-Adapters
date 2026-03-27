"""Módulo que contiene la definición de una query básica para obtener una entidad
Driver particular mediante su ID."""

# Librerías Externas.
from dataclasses import dataclass

# Librerías Internas.
from app.application.queries.base import Query


@dataclass(frozen = True)
class GetDriverQuery(Query):
    """Clase que define una query de búsqueda específica de una única entidad."""

    driver_id: str

    def __post_init__(self) -> None:
        """Método dunder ara aplicar un poco de seguridad y validación."""

        if not isinstance(self.driver_id, str):
            raise ValueError("El ID de un conductor debe ser un string.")
