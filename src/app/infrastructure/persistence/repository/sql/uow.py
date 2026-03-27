"""Módulo que contiene la realización del puerto de atomicidad de trabajo."""

# Librerías Externas.
from typing import Type

from sqlalchemy.orm import Session

# Librerías Internas.
from app.application.ports.persistence.uow import UnitOfWorkPort

from app.infrastructure.persistence.repository.sql.driver_repository import SQLDriverRepositoryAdapter
from app.infrastructure.persistence.repository.sql.sender_repository import SQLSenderRepositoryAdapter
from app.infrastructure.persistence.repository.sql.package_repository import SQLPackageRepositoryAdapter


class SQLUnitOfWorkAdapter(UnitOfWorkPort):
    """Clase realización del puerto especificado."""

    def __init__(self, session_factory: Type[Session]) -> None:
        """Método de instanciación de objetos de clase.
        
        Args:
        ----------
        session_factory: Type[Session].
            Factory que permite crear sesiones de BD."""
        
        self._session_factory = session_factory

    def commit(self) -> None:
        """Método que permite confirmar todo cambio aplicado en el dominio."""

        self._session.commit()

    def rollback(self):
        """Método que permite revertir todo cambio en dominio que no se haya
        persistido. Muy útil ante errores."""

        self._session.rollback()

    def __enter__(self) -> None:
        """Método dunder que permite iniciar el context manager."""

        self._session = self._session_factory()

        self.driver_repository = SQLDriverRepositoryAdapter(session = self._session)
        self.sender_repository = SQLSenderRepositoryAdapter(session = self._session)
        self.package_repository = SQLPackageRepositoryAdapter(session = self._session)

        return super(SQLUnitOfWorkAdapter, self).__enter__()
    
    def __exit__(self, *args) -> None:
        """Método dunder que siempre permite cerrar el context manager y asegurar
        la atomicidad de las transacciónes de la sesión."""

        super(SQLUnitOfWorkAdapter, self).__exit__()
        self._session.close()
