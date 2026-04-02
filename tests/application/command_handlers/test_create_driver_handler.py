"""Módulo que contiene pruebas unitarias para la creación de Drivers."""

# Librerías Internas.
from app.domain.entities.driver import Driver
from app.domain.value_objects.delivery_date import DeliveryDate

from app.application.commands.create_driver import CreateDriverCommand
from app.application.command_handlers.create_driver import CreateDriverHandler

from app.infrastructure.persistence.repository.fake.uow import FakeUnitOfWorkAdapter


class TestCreateDriverHandler:
    """Módulo que contiene pruebas unitarias para el handler."""

    def test_correct_creation(self) -> None:
        """Método que contiene la prueba unitaria del happy path
        del handler."""
        
        unit_of_work = FakeUnitOfWorkAdapter()

        handler = CreateDriverHandler(unit_of_work = unit_of_work)
        driver_id = handler.handle(command = CreateDriverCommand(driver_id = "1", last_delivery = "2000-06-07 00:00:00"))

        assert driver_id is not None, "Valide que se haya devuelto el ID."
        assert isinstance(driver_id, str), "Valide que el ID sea correcto."
        assert driver_id == "1", "Valide que se haya transferido la información del comando."

        created_driver = unit_of_work.driver_repository.get(driver_id = "1")
        
        assert isinstance(created_driver, Driver), "Valide que la creación se refleje en bases de datos."
        assert created_driver.last_delivery == DeliveryDate("2000-06-07 00:00:00"), "Valide que la información de creación se persista."
