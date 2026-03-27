"""Módulo que contiene una query particular que necesitamos para nuestras
necesidades de negocio."""

# Librerías Externas.
from dataclasses import dataclass

# Librerías Internas.
from app.application.queries.base import Query

from app.application.ports.persistence.criteria import Criteria, Filter, Operator, Pagination


@dataclass(frozen = True)
class ListPendingPackagesQuery(Query):
    """Clase que encapsula una query que se encarga de obtener qué Packages
    no han sido asignados a un Driver."""

    criteria: Criteria = Criteria(
        filters = [
            Filter(field = "status", value = "PENDING", operator = Operator.EQ)
        ],
        pagination = Pagination(limit = 10, order_by = "created_at", order_dir = "asc")
    )
