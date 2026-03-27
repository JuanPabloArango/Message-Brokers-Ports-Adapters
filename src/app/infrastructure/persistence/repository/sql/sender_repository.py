"""Módulo que contiene la realización del puerto de persistencia enfocado
en definir el contrato del repositorio para la entidad Driver."""

# Librerías Externas.
from typing import Any, Dict, List, Callable

from sqlalchemy import select
from sqlalchemy.orm import Session

# Librerías Internas.
from app.domain.entities.sender import Sender

from app.application.ports.persistence.criteria import Operator, Criteria
from app.application.ports.persistence.repositories.sender_repository import SenderRepositoryPort

from app.application.exceptions import NotAValidAttribute


class SQLSenderRepositoryAdapter(SenderRepositoryPort):
    """Clase que sirve como realización del puerto especificado."""

    OPERATOR_MAP: Dict[Operator, Callable[[str, Any], bool]] = {
        Operator.EQ: lambda col, val: col == val,
        Operator.NEQ: lambda col, val: col != val,
        Operator.GT: lambda col, val: col > val,
        Operator.GTE: lambda col, val: col >= val,
        Operator.LT: lambda col, val: col < val,
        Operator.LTE: lambda col, val: col <= val,
        Operator.IN: lambda col, val: col.in_(val.split(","))
    }

    def __init__(self, session: Session) -> None:
        """Método de instanciación de objetos de clase.
        
        Args:
        ----------
        session: Session.
            Sesión que establece la conexión con la BD."""
        
        self._session = session

    def get(self, sender_id: str) -> Sender:
        """Método que permite obtener la entidad de dominio mediante
        la Primary Key asociada en la definición de la tabla.
        
        Args:
        ----------
        sender_id: str.
            ID del usuario que desea consultar.
        
        Returns:
        ----------
        Sender.
            Entidad de dominio."""
        
        sender = self._session.get(Sender, sender_id)
        return sender
    
    def save(self, sender: Sender) -> None:
        """Métoo que permite almacenar la entidad de dominio en la tabla
        de persistencia.
        
        Args:
        ----------
        sender: Sender.
            Entidad a almacenar."""
        
        self._session.add(sender)

    def list_all(self, criteria: Criteria) -> List[Sender]:
        """Método que permite listar todas las entidades persistidas.
        
        Returns:
        ----------
        List[Sender].
            Entidades de dominio."""
        
        q = self._session.query(Sender)
        for filter in criteria.filters:

            attr = f"_{filter.field}"
            if not hasattr(Sender, attr):
                raise NotAValidAttribute(f"El atributo {filter.field} no es un campo de filtrado válido.")
            
            column = getattr(Sender, attr)
            condition = self.OPERATOR_MAP[filter.operator](column, filter.value)
            q = q.filter(condition)

        if criteria.pagination:
            pagination = criteria.pagination
            if pagination.order_by and hasattr(Sender, f"_{pagination.order_by}"):
                ordering_columns = getattr(Sender, f"_{pagination.order_by}")
                ordering_direction = ordering_columns.asc() if pagination.order_dir == "asc" else ordering_columns.desc()

                q = q.order_by(ordering_direction)

            q = q.offset(pagination.offset).limit(pagination.limit)

        filterd_packages = q.all()
        return filterd_packages
