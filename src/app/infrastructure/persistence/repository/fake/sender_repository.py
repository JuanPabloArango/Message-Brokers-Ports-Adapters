"""Módulo que contiene la realización del puerto de persistencia para la entidad
Sender."""

# Librerías Externas.
from typing import Any, List, Dict, Optional, Union, Callable

# Librerías Internas.
from app.domain.entities.sender import Sender

from app.application.ports.persistence.criteria import Criteria, Pagination, Filter, Operator
from app.application.ports.persistence.repositories.sender_repository import SenderRepositoryPort

from app.application.exceptions import NotAValidAttribute


class FakeSenderRepositoryAdapter(SenderRepositoryPort):
    """Clase que define la realización del puerto especificado."""

    OPERATOR_MAP: Dict[Operator, Callable[[str, Any], bool]] = {
        Operator.EQ: lambda col, val: col == val,
        Operator.NEQ: lambda col, val: col != val,
        Operator.GT: lambda col, val: col > val,
        Operator.GTE: lambda col, val: col >= val,
        Operator.LT: lambda col, val: col < val,
        Operator.LTE: lambda col, val: col <= val,
        Operator.IN: lambda col, val: col in val
    }

    COLUMNS_MAP: Dict[str, Callable[[Sender], Any]] = {
        "id": lambda entity: entity.id,
        "status": lambda entity: entity.status,
        "created_at": lambda entity: entity.created_at,
        "updated_at": lambda entity: entity.updated_at
    }

    def __init__(self, base: Optional[List[Sender]] = None) -> None:
        """Método de instanciación de objetos de la clase.
        
        Args:
        ----------
        base: Optional[List[Sender]].
            Senders base para realizar las pruebas."""
        
        self._base = set(base) if base else set()

    def get(self, sender_id: str) -> Union[Sender, None]:
        """Método que permite obtener la entidad Sender por su identidad.
        
        Args:
        ----------
        sender_id: str.
            ID de la entidad que desea obtener.
        
        Returns:
        ----------
        Union[Sender, None].
            Entidad de dominio obtenida."""
        
        sender = next((sender for sender in self._base if sender.id.value == sender_id), None)
        return sender
    
    def save(self, sender: Sender) -> None:
        """Método que permite almaceran una entidad de dominio.
        
        Args:
        ----------
        sender: Sender.
            Entidad de dominio a persistir."""
        
        self._base.add(sender)

    def list_all(self, criteria: Criteria) -> List[Sender]:
        """Método que permite devolver todos los objetos de la entidad que han
        sido persistidos de acuerdo a unos filtros.
        
        Args:
        ----------
        criteria: Criteria.
            Criterios de filtrado de entidades.
            
        Returns:
        ----------
        List[Sender].
            Entidades que cumplen con los requisitos de la búsqueda."""

        results = list(self._base)
        for filter in criteria.filters:
            
            getter = self.COLUMNS_MAP.get(filter.field)
            if results and not getter:
                raise NotAValidAttribute(f"El atributo {filter.field} no es un campo de filtrado válido.")

            condition_func = self.OPERATOR_MAP[filter.operator]
            results = [entity for entity in results if condition_func(getter(entity), filter.value)]

        if criteria.pagination:
            pagination = criteria.pagination

            getter = self.COLUMNS_MAP.get(pagination.order_by)
            if pagination.order_by and results and getter:
                results = sorted(results, key = lambda x: getter(x),
                                 reverse = True if pagination.order_dir == "desc" else False)
            
            results = results[pagination.offset: pagination.offset + pagination.limit]
        return results

