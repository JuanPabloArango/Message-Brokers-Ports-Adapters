"""Módulo que contiene pruebas unitarias para la creación de Senders."""

# Librerías Externas.
from typing import List

# Librerías Internas.
from app.domain.entities.sender import Sender

from app.application.commands.create_sender import CreateSenderCommand
from app.application.command_handlers.create_sender import CreateSenderHandler

from app.infrastructure.persistence.repository.fake.uow import FakeUnitOfWorkAdapter


class TestCreateSenderHandler:
    """Módulo que contiene pruebas unitarias para el handler."""

    def test_correct_creation(self, base_senders: List[Sender]) -> None:
        """Método que contiene la prueba unitaria del happy path
        del handler.
        
        Args:
        ----------
        base_senders: List[Sender].
            Lista base de senders."""
        
        unit_of_work = FakeUnitOfWorkAdapter(senders = base_senders)

        handler = CreateSenderHandler(unit_of_work = unit_of_work)
        sender_id = handler.handle(command = CreateSenderCommand(sender_id = "1"))

        assert sender_id is not None, "Valide que se haya devuelto el ID."
        assert isinstance(sender_id, str), "Valide que el ID sea correcto."
        assert sender_id == "1", "Valide que se haya transferido la información del comando."
