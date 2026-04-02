"""Módulo que contiene pruebas unitarias para la creación de Senders."""

# Librerías Externas.
from typing import List

import pytest

# Librerías Internas.
from app.domain.entities.driver import Driver
from app.domain.value_objects.driver_status import DriverStatus

from app.application.commands.free_driver import FreeDriverCommand
from app.application.command_handlers.free_driver import FreeDriverHandler

from app.application.exceptions import DriverNotFound

from app.infrastructure.persistence.repository.fake.uow import FakeUnitOfWorkAdapter


class TestCreateSenderHandler:
    """Módulo que contiene pruebas unitarias para el handler."""

    def test_correct_status_change(self, base_drivers: List[Driver]) -> None:
        """Método que contiene la prueba unitaria del happy path
        del handler.
        
        Args:
        ----------
        base_drivers: List[Driver].
            Lista base de Drivers."""
        
        unit_of_work = FakeUnitOfWorkAdapter(drivers = base_drivers)

        with unit_of_work as uow:
            driver = uow.driver_repository.get(driver_id = "2")

            assert driver.status == DriverStatus.OCCUPIED, "Valide el correcto estado inicial"

        handler = FreeDriverHandler(unit_of_work = unit_of_work)
        handler.handle(command = FreeDriverCommand(driver_id = "2"))

        driver = unit_of_work.driver_repository.get(driver_id = "2")
        assert driver.status == DriverStatus.AVAILABLE, "Valide que se haya cambiado el estado."

    def test_incorrect_status_change_due_to_nonexistent_driver(self, base_drivers: List[Driver]) -> None:
        """Método que contiene la prueba unitaria del happy path
        del handler.
        
        Args:
        ----------
        base_drivers: List[Driver].
            Lista base de Drivers."""
        
        unit_of_work = FakeUnitOfWorkAdapter(drivers = base_drivers)

        handler = FreeDriverHandler(unit_of_work = unit_of_work)

        with pytest.raises(DriverNotFound):
            handler.handle(command = FreeDriverCommand(driver_id = "42"))
