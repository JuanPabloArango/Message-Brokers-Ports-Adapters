"""Módulo que contiene pruebas unitarias para la marcación de un Package como
'DELIVERED'."""

# Librerías Externas.
from typing import List

import pytest

# Librerías Internas.
from app.domain.entities.driver import Driver
from app.domain.entities.package import Package
from app.domain.value_objects.package_status import PackageStatus

from app.application.commands.deliver_package import DeliverPackageCommand
from app.application.command_handlers.deliver_package import DeliverPackageHandler

from app.application.exceptions import PackageNotFound

from app.infrastructure.persistence.repository.fake.uow import FakeUnitOfWorkAdapter


class TestDeliverPackageHandler:
    """Módulo que contiene pruebas unitarias para el handler."""

    def test_correct_status_change(self, base_packages: List[Package], base_drivers: List[Driver]) -> None:
        """Método que contiene la prueba unitaria del happy path
        del handler.
        
        Args:
        ----------
        base_packages: List[Package].
            Lista base de Packages.
            
        base_drivers: List[Driver].
            Lista base de Drivers."""
        
        unit_of_work = FakeUnitOfWorkAdapter(packages = base_packages, drivers = base_drivers)

        with unit_of_work as uow:
            package = uow.package_repository.get(package_id = "2")

            assert package.status == PackageStatus.ASSIGNED, "Valide el correcto estado inicial"

        handler = DeliverPackageHandler(unit_of_work = unit_of_work)
        package_id = handler.handle(command = DeliverPackageCommand(package_id = "2"))

        assert isinstance(package_id, str), "Valide la correcta devolución."

        package = unit_of_work.package_repository.get(package_id = "2")

        assert package.status == PackageStatus.DELIVERED, "Valide que se haya cambiado el estado."

    def test_incorrect_status_change_due_to_nonexistent_driver(self, base_packages: List[Package]) -> None:
        """Método que contiene la prueba unitaria del happy path
        del handler.
        
        Args:
        ----------
        base_packages: List[Package].
            Lista base de Package."""
        
        unit_of_work = FakeUnitOfWorkAdapter(packages = base_packages)

        handler = DeliverPackageHandler(unit_of_work = unit_of_work)

        with pytest.raises(PackageNotFound):
            handler.handle(command = DeliverPackageCommand(package_id = "42"))
