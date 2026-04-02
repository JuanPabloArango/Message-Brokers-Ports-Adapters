"""Módulo que contiene las pruebas unitarias para el handler de asignación
de un Driver a un Package."""

# Librerías Externas.
from typing import List

import pytest

# Librerías Internas.
from app.domain.entities.driver import Driver
from app.domain.entities.package import Package

from app.domain.value_objects.driver_status import DriverStatus
from app.domain.value_objects.package_status import PackageStatus

from app.application.commands.assign_driver import AssignDriverCommand
from app.application.command_handlers.assign_driver import AssignDriverHandler

from app.domain.exceptions import PackageTransitionError
from app.application.exceptions import PackageNotFound, NotCurrenltyAvailableDrivers

from app.infrastructure.persistence.repository.fake.uow import FakeUnitOfWorkAdapter


class TestAssignDriverHandler:
    """Clase que encapsula las pruebas unitarias del handler."""

    def test_assign_driver_happy_path(self, base_drivers: List[Driver], base_packages: List[Package]) -> None:
        """Método que contiene la prueba unitaria de asignación de un Driver
        a un Package.
        
        Args:
        ----------
        base_drivers: List[Driver].
            Conductores base para la prueba unitaria.
            
        base_packages: List[Package].
            Paquetes base para la prueba unitaria."""
        
        unit_of_work = FakeUnitOfWorkAdapter(drivers = base_drivers, packages = base_packages)

        handler = AssignDriverHandler(unit_of_work = unit_of_work)
        assigned_driver_id = handler.handle(command = AssignDriverCommand(package_id = "1"))

        package = unit_of_work.package_repository.get(package_id = "1")
        driver = unit_of_work.driver_repository.get(driver_id = assigned_driver_id)

        assert package.status == PackageStatus.ASSIGNED, "Valide que se haya asignado el paquete."
        assert package.driver_id.value == "3", "Valide que se haya asignado al conductor esperado."

        assert driver.status == DriverStatus.OCCUPIED, "Valide que también haya modificado el estado del Driver."

    def test_assign_driver_failed_due_to_package_not_found(self, base_drivers: List[Driver], base_packages: List[Package]) -> None:
        """Método que contiene la prueba unitaria de asignación de un Driver
        a un Package.
        
        Args:
        ----------
        base_drivers: List[Driver].
            Conductores base para la prueba unitaria.
            
        base_packages: List[Package].
            Paquetes base para la prueba unitaria."""
        
        unit_of_work = FakeUnitOfWorkAdapter(drivers = base_drivers, packages = base_packages)

        handler = AssignDriverHandler(unit_of_work = unit_of_work)

        with pytest.raises(PackageNotFound):
            handler.handle(command = AssignDriverCommand(package_id = "70"))

    def test_assign_driver_failed_due_unavailable_drivers(self, base_packages: List[Package]) -> None:
        """Método que contiene la prueba unitaria de asignación de un Driver
        a un Package.
        
        Args:
        ----------
        base_packages: List[Package].
            Paquetes base para la prueba unitaria."""
        
        unit_of_work = FakeUnitOfWorkAdapter(packages = base_packages)

        handler = AssignDriverHandler(unit_of_work = unit_of_work)

        with pytest.raises(NotCurrenltyAvailableDrivers):
            handler.handle(command = AssignDriverCommand(package_id = "1"))

    def test_assign_driver_failed_due_unavailable_drivers(self, base_drivers: List[Driver], base_packages: List[Package]) -> None:
        """Método que contiene la prueba unitaria de asignación de un Driver
        a un Package.
        
        Args:
        ----------
        base_drivers: List[Driver].
            Conductores base para la prueba unitaria.

        base_packages: List[Package].
            Paquetes base para la prueba unitaria."""
        
        unit_of_work = FakeUnitOfWorkAdapter(drivers = base_drivers, packages = base_packages)

        handler = AssignDriverHandler(unit_of_work = unit_of_work)

        with pytest.raises(PackageTransitionError):
            handler.handle(command = AssignDriverCommand(package_id = "2"))
