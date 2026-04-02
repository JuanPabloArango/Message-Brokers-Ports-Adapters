"""Módulo que contiene pruebas unitarias para la verificación de Senders."""

# Librerías Externas.
from typing import List

import pytest

# Librerías Internas.
from app.domain.entities.sender import Sender
from app.domain.value_objects.sender_status import SenderStatus

from app.application.commands.verify_sender import VerifySenderCommand
from app.application.command_handlers.verify_sender import VerifySenderHandler

from app.application.exceptions import SenderNotFound

from app.infrastructure.persistence.repository.fake.uow import FakeUnitOfWorkAdapter


class TestVerifySenderHandler:
    """Módulo que contiene pruebas unitarias para el handler."""

    def test_correct_status_change(self, base_senders: List[Sender]) -> None:
        """Método que contiene la prueba unitaria del happy path
        del handler.
        
        Args:
        ----------
        base_senders: List[Sender].
            Lista base de Senders."""
        
        unit_of_work = FakeUnitOfWorkAdapter(senders = base_senders)

        with unit_of_work as uow:
            sender = uow.sender_repository.get(sender_id = "2")

            assert sender.status == SenderStatus.UNVERIFIED, "Valide el correcto estado inicial"

        handler = VerifySenderHandler(unit_of_work = unit_of_work)
        handler.handle(command = VerifySenderCommand(sender_id = "2"))

        sender = unit_of_work.sender_repository.get(sender_id = "2")
        assert sender.status == SenderStatus.VERIFIED, "Valide que se haya cambiado el estado."

    def test_incorrect_status_change_due_to_nonexistent_sender(self, base_senders: List[Sender]) -> None:
        """Método que contiene la prueba unitaria del unhappy path
        del handler.
        
        Args:
        ----------
        base_senders: List[Sender].
            Lista base de Senders."""
        
        unit_of_work = FakeUnitOfWorkAdapter(senders = base_senders)

        handler = VerifySenderHandler(unit_of_work = unit_of_work)

        with pytest.raises(SenderNotFound):
            handler.handle(command = VerifySenderCommand(sender_id = "42"))
