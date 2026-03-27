"""Módulo que contiene la realización del puerto de atomicidad de trabajo."""

# Librerías Externas.
from typing import List, Optional

# Librerías Internas.
from app.domain.entities.driver import Driver
from app.domain.entities.sender import Sender
from app.domain.entities.package import Package

from app.application.ports.persistence.uow import UnitOfWorkPort

from app.infrastructure.persistence.repository.fake.driver_repository import FakeDriverRepositoryAdapter
from app.infrastructure.persistence.repository.fake.sender_repository import FakeSenderRepositoryAdapter
from app.infrastructure.persistence.repository.fake.package_repository import FakePackageRepositoryAdapter


class FakeUnitOfWorkAdapter(UnitOfWorkPort):
    """Clase realización del puerto especificado."""

    def __init__(self, senders: Optional[List[Sender]] = None,
                 drivers: Optional[List[Driver]] = None,
                 packages: Optional[List[Package]] = None) -> None:
        """Método de instanciación de objetos de clase.
        
        Args:
        ----------
        session_factory: Type[Session].
            Factory que permite crear sesiones de BD."""
        
        self._commited: bool = False
        
        self._senders = senders
        self._drivers = drivers
        self._packages = packages

    def commit(self) -> None:
        """Método que permite confirmar todo cambio aplicado en el dominio."""

        self._commited = True

    def rollback(self):
        """Método que permite revertir todo cambio en dominio que no se haya
        persistido. Muy útil ante errores."""

        pass

    def __enter__(self) -> None:
        """Método dunder que permite iniciar el context manager."""

        self.driver_repository = FakeDriverRepositoryAdapter(base = self._drivers)
        self.sender_repository = FakeSenderRepositoryAdapter(base = self._senders)
        self.package_repository = FakePackageRepositoryAdapter(base = self._packages)

        return super(FakeUnitOfWorkAdapter, self).__enter__()
