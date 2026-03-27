"""Módulo que contiene la base para nuestras Queries."""

# Librerías Externas.
from typing import Any, List, Optional, Literal

from enum import Enum
from dataclasses import dataclass, field


class Operator(Enum):
    """Clase que define los operadores que soportaremos en nuestro
    patrón Criteria."""

    EQ: str = "eq"
    NEQ: str = "neq"
    GT: str = "gt"
    GTE: str = "gte"
    LT: str = "lt"
    LTE: str = "lte"
    IN: str = "in"


@dataclass(frozen = True)
class Filter:
    """Clase que permite expresar una condición de filtrado como un objeto."""

    field: str
    value: Any
    operator: Operator


@dataclass(frozen = True)
class Pagination:
    """Clase que permite ordernar los objetos filtrados según unos criterios."""

    limit: int
    offset: Optional[int] = 0
    order_by: Optional[str] = None
    order_dir: Optional[Literal["asc", "desc"]] = "asc"


@dataclass(frozen = True)
class Criteria:
    """Clase que encapsula N objetos de filtrado."""

    filters: List[Filter] = field(default_factory = list)
    pagination: Optional[Pagination] = None
