"""Módulo que contiene pruebas unitarias para validación de información
en Commands."""

# Librerías Externas.
import pytest

# Librerías Internas.
from app.application.commands.create_package import CreatePackageCommand


class TestCreatePackageCommand:
    """Clase que encapsula pruebas unitarias del comando."""

    def test_init(self) -> None:
        """Método que contiene prueba unitaria para validar
        instanciación de comando."""

        command = CreatePackageCommand(sender_id = "123")

        assert command.sender_id == "123", "Valide que la información sí la transfiera el comando."
        assert not command.package_id, "Valide que la información sí la transfiera el comando."

    def test_init_error(self) -> None:
        """Método que contiene la prueba unitaria para validar
        validaciones de instanciación."""

        with pytest.raises(ValueError):
            CreatePackageCommand(sender_id = 123)
