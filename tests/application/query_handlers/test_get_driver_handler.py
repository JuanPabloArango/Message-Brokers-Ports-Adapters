"""Módulo que contiene pruebas unitarias para un handler de Queries."""

# Librerías Externas.
from typing import List

import pytest

# Librerías Internas.
from app.domain.entities.driver import Driver

from app.application.dtos.driver import DriverDTO

from app.application.queries.get_driver_by_id import GetDriverQuery
from app.application.query_handlers.get_driver import GetDriverHandler

from app.application.exceptions import DriverNotFound

from app.infrastructure.persistence.repository.fake.uow import FakeUnitOfWorkAdapter


class TestGetDriverHandler:
    """Clase que encapsula las pruebas unitarias para el handler GetDriverHandler."""

    def test_driver_found_handler(self, base_drivers: List[Driver]) -> None:
        """Método que contiene la prueba unitaria del método 'handle' en el
        caso donde existe la entidad.
        
        Args:
        ----------
        base_drivers: List[Driver].
            Lista base de los conductores para la prueba."""

        uow = FakeUnitOfWorkAdapter(drivers = base_drivers)

        handler = GetDriverHandler(unit_of_work = uow)
        driver = handler.handle(query = GetDriverQuery(driver_id = "4"))

        assert isinstance(driver, DriverDTO), "Valide que la instancia sea hallada y tenga el typing correcto."
        assert driver.id == "4", "Valide que los atributos de la instancia sean los esperados."

    def test_driver_not_found_handler(self, base_drivers: List[Driver]) -> None:
        """Método que contiene la prueba unitaria del método 'handle' en el
        caso donde existe la entidad.
        
        Args:
        ----------
        base_drivers: List[Driver].
            Lista base de los conductores para la prueba."""

        uow = FakeUnitOfWorkAdapter(drivers = base_drivers)

        handler = GetDriverHandler(unit_of_work = uow)

        with pytest.raises(DriverNotFound):
            driver = handler.handle(query = GetDriverQuery(driver_id = "42"))
