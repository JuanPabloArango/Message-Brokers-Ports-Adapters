"""Módulo que contiene la definición de una query básica para obtener una entidad
Sender particular mediante su ID."""

# Librerías Externas.
from dataclasses import dataclass

# Librerías Internas.
from app.application.queries.base import Query


@dataclass(frozen = True)
class GetSenderQuery(Query):
    """Clase que define una query de búsqueda específica de una única entidad."""

    sender_id: str

    def __post_init__(self) -> None:
        """Método dunder ara aplicar un poco de seguridad y validación."""

        if not isinstance(self.sender_id, str):
            raise ValueError("El ID de un usuario debe ser un string.")
