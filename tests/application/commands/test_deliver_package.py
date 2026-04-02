"""Módulo que contiene pruebas unitarias para validación de información
en Commands."""

# Librerías Externas.
import pytest

# Librerías Internas.
from app.application.commands.deliver_package import DeliverPackageCommand


class TestDeliverPackageCommand:
    """Clase que encapsula pruebas unitarias del comando."""

    def test_init(self) -> None:
        """Método que contiene prueba unitaria para validar
        instanciación de comando."""

        command = DeliverPackageCommand(package_id = "12")

        assert command.package_id == "12", "Valide que la información sí la transfiera el comando."

    def test_init_error(self) -> None:
        """Método que contiene la prueba unitaria para validar
        validaciones de instanciación."""

        with pytest.raises(ValueError):
            DeliverPackageCommand(package_id = 12)