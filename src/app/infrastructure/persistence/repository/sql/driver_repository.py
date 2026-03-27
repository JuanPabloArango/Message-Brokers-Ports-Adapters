"""Módulo que contiene la realización del puerto de persistencia enfocado
en definir el contrato del repositorio para la entidad Driver."""

# Librerías Externas.
from typing import Any, List, Dict, Callable

from sqlalchemy import select
from sqlalchemy.orm import Session

# Librerías Internas.
from app.domain.entities.driver import Driver

from app.application.ports.persistence.criteria import Operator, Criteria
from app.application.ports.persistence.repositories.driver_repository import DriverRepositoryPort

from app.application.exceptions import NotAValidAttribute


class SQLDriverRepositoryAdapter(DriverRepositoryPort):
    """Clase que sirve como realización del puerto especificado."""

    OPERATOR_MAP: Dict[Operator, Callable[[str, Any], bool]] = {
        Operator.EQ: lambda col, val: col == val,
        Operator.NEQ: lambda col, val: col != val,
        Operator.GT: lambda col, val: col > val,
        Operator.GTE: lambda col, val: col >= val,
        Operator.LT: lambda col, val: col < val,
        Operator.LTE: lambda col, val: col <= val,
        Operator.IN: lambda col, val: col.in_(val)
    }

    def __init__(self, session: Session) -> None:
        """Método de instanciación de objetos de clase.
        
        Args:
        ----------
        session: Session.
            Sesión que establece la conexión con la BD."""
        
        self._session = session

    def get(self, driver_id: str) -> Driver:
        """Método que permite obtener la entidad de dominio mediante
        la Primary Key asociada en la definición de la tabla.
        
        Args:
        ----------
        driver_id: str.
            ID del conductor que desea consultar.
        
        Returns:
        ----------
        Driver.
            Entidad de dominio."""
        
        driver = self._session.get(Driver, driver_id)
        return driver
    
    def save(self, driver: Driver) -> None:
        """Métoo que permite almacenar la entidad de dominio en la tabla
        de persistencia.
        
        Args:
        ----------
        driver: Driver.
            Entidad a almacenar."""
        
        self._session.add(driver)

    def list_all(self, criteria: Criteria) -> List[Driver]:
        """Método que permite listar todas las entidades persistidas.

        Args:
        ----------
        criteria: Criteria.
            Criterios de búsqueda sobre todas las entidades.
        
        Returns:
        ----------
        List[Driver].
            Entidades de dominio."""
        
        q = self._session.query(Driver)

        for filter in criteria.filters:
            attr = f"_{filter.field}"
            if not hasattr(Driver, attr):
                raise NotAValidAttribute(f"El atributo {filter.field} no es un campo de filtrado válido.")
            
            column = getattr(Driver, attr)
            condition = self.OPERATOR_MAP[filter.operator](column, filter.value)

            q = q.filter(condition)
        
        if criteria.pagination:
            pagination = criteria.pagination

            if pagination.order_by and hasattr(Driver, f"_{pagination.order_by}"):
                ordering_column = getattr(Driver, f"_{pagination.order_by}")
                ordering_direction = ordering_column.asc() if pagination.order_dir == "asc" else ordering_column.desc()

                q = q.order_by(ordering_direction)

            q = q.offset(pagination.offset).limit(pagination.limit)
        
        filtered_drivers = q.all()
        return filtered_drivers
