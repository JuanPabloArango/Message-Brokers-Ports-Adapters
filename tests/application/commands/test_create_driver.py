"""Módulo que contiene pruebas unitarias para validación de información
en Commands."""

# Librerías Externas.
import pytest
import datetime as dt

# Librerías Internas.
from app.application.commands.create_driver import CreateDriverCommand


class TestCreateDriverCommand:
    """Clase que encapsula pruebas unitarias del comando."""

    def test_init(self) -> None:
        """Método que contiene prueba unitaria para validar
        instanciación de comando."""

        command = CreateDriverCommand()

        assert not command.driver_id, "Valide que la información sí la transfiera el comando."
        assert not command.last_delivery, "Valide que la información sí la transfiera el comando."

        command = CreateDriverCommand(driver_id = "42", last_delivery = "2025-10-01 12:00:00")

        assert command.driver_id == "42", "Valide que la información sí la transfiera el comando."
        assert command.last_delivery == "2025-10-01 12:00:00", "Valide que la información sí la transfiera el comando."

    def test_init_error(self) -> None:
        """Método que contiene la prueba unitaria para validar
        validaciones de instanciación."""

        with pytest.raises(ValueError):
            CreateDriverCommand(driver_id = 12)

        with pytest.raises(ValueError):
            CreateDriverCommand(last_delivery = dt.datetime(2025, 10, 1, 12, 0, 0))