"""Módulo que contiene pruebas unitarias para validación de información
en Commands."""

# Librerías Externas.
import pytest

# Librerías Internas.
from app.application.commands.create_sender import CreateSenderCommand


class TestCreateSenderCommand:
    """Clase que encapsula pruebas unitarias del comando."""

    def test_init(self) -> None:
        """Método que contiene prueba unitaria para validar
        instanciación de comando."""

        command = CreateSenderCommand()

        assert not command.sender_id, "Valide que la información sí la transfiera el comando."

        command = CreateSenderCommand(sender_id = "1")
        
        assert command.sender_id == "1", "Valide que la información sí la transfiera el comando."

    def test_init_error(self) -> None:
        """Método que contiene la prueba unitaria para validar
        validaciones de instanciación."""

        with pytest.raises(ValueError):
            CreateSenderCommand(sender_id = 123)
