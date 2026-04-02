"""Módulo que contiene la realización del puerto de persistencia para la entidad
Package."""

# Librerías Externas.
from typing import Any, Dict, List, Optional, Union, Callable

# Librerías Internas.
from app.domain.entities.package import Package

from app.application.ports.persistence.criteria import Criteria, Operator
from app.application.ports.persistence.repositories.package_repository import PackageRepositoryPort

from app.application.exceptions import NotAValidAttribute


class FakePackageRepositoryAdapter(PackageRepositoryPort):
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

    COLUMNS_MAP: Dict[str, Callable[[Package], Any]] = {
        "id": lambda entity: entity.id,
        "sender_id": lambda entity: entity.sender_id,
        "driver_id": lambda entity: entity.driver_id,
        "status": lambda entity: entity.status,
        "created_at": lambda entity: entity.created_at,
        "updated_at": lambda entity: entity.updated_at
    }

    def __init__(self, base: Optional[List[Package]] = None) -> None:
        """Método de instanciación de objetos de la clase.
        
        Args:
        ----------
        base: Optional[List[Package]].
            Packages base para realizar las pruebas."""
        
        self._base = set(base) if base else set()

    def get(self, package_id: str) -> Union[Package, None]:
        """Método que permite obtener la entidad Package por su identidad.
        
        Args:
        ----------
        package_id: str.
            ID de la entidad que desea obtener.
        
        Returns:
        ----------
        Union[Package, None].
            Entidad de dominio obtenida."""
        
        package = next((package for package in self._base if package.id.value == package_id), None)
        return package
    
    def save(self, package: Package) -> None:
        """Método que permite almaceran una entidad de dominio.
        
        Args:
        ----------
        package: Package.
            Entidad de dominio a persistir."""
        
        self._base.add(package)

    def list_all(self, criteria: Criteria) -> List[Package]:
        """Método que permite devolver todos los objetos de la entidad que han
        sido persistidos de acuerdo a unos filtros.
        
        Args:
        ----------
        criteria: Criteria.
            Criterios de filtrado de entidades.
            
        Returns:
        ----------
        List[Driver].
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
