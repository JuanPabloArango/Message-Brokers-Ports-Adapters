"""Módulo que contiene la definición del puerto para atomicidad de operaciones."""

# Librerías Externas.
from __future__ import annotations

from abc import ABC, abstractmethod

# Librerías Internas.
from app.application.ports.persistence.repositories.sender_repository import SenderRepositoryPort
from app.application.ports.persistence.repositories.driver_repository import DriverRepositoryPort
from app.application.ports.persistence.repositories.package_repository import PackageRepositoryPort


class UnitOfWorkPort(ABC):
    """Clase que define el contrato nominal para el puerto de atomicidad de
    trabajo en bases de datos."""

    sender_repository: SenderRepositoryPort
    driver_repository: DriverRepositoryPort
    package_repository: PackageRepositoryPort

    @abstractmethod
    def commit(self) -> None:
        """Método abstracto que define parte del contrato enfocado en la persistencia
        de los cambios aplicados sobre el dominio."""

        raise NotImplementedError("Si tu clase es una realización de 'UnitOfWorkPort', debes implementar el método 'commit'.")
    
    @abstractmethod
    def rollback(self) -> None:
        """Método abstracto que define parte del contrato enfocado en la devolución
        de los cambios aplicados sobre el dominio si algo sale mal sobre el mismo."""

        raise NotImplementedError("Si tu clase es una realización de 'UnitOfWorkPort', debes implementar el método 'rollback'.")
    
    def __enter__(self) -> UnitOfWorkPort:
        """Método dunder que define que trabajaremos el UoW como un context
        manager para garantizar rollback automático al final de cada sesión."""

        return self
    
    def __exit__(self, *args) -> None:
        """Método dunder que garantiza la ejecución del rollback al final de
        cada sesión por seguridad."""

        self.rollback()
