"""Módulo que contiene las pruebas unitarias para el handler GetSenderHandler."""

# Librerías Externas.
from typing import List

import pytest

# Librerías Internas.
from app.domain.entities.sender import Sender
from app.domain.value_objects.sender_status import SenderStatus

from app.application.dtos.sender import SenderDTO

from app.application.queries.get_sender_by_id import GetSenderQuery
from app.application.query_handlers.get_sender import GetSenderHandler

from app.application.exceptions import SenderNotFound

from app.infrastructure.persistence.repository.fake.uow import FakeUnitOfWorkAdapter


class TestGetSenderHandler:
    """Módulo que encapsula las pruebas unitarias del handler."""

    def test_sender_found_handler(self, base_senders: List[Sender]) -> None:
        """Método que contiene la prueba unitaria del método 'handle' en el
        caso donde existe la entidad.
        
        Args:
        ----------
        base_senders: List[Sender].
            Lista base de los senders para la prueba."""
        
        unit_of_work = FakeUnitOfWorkAdapter(senders = base_senders)

        handler = GetSenderHandler(unit_of_work = unit_of_work)
        sender = handler.handle(query = GetSenderQuery(sender_id = "1"))

        assert isinstance(sender, SenderDTO), "Valide que la entidad obtenida sea del tipo correcto."
        assert sender.status == "VERIFIED", "Valide que haya obtenido la entidad esperada."

    def test_sender_not_found_handler(self, base_senders: List[Sender]) -> None:
        """Método que contiene la prueba unitaria del método 'handle' en el
        caso donde existe la entidad.
        
        Args:
        ----------
        base_senders: List[Sender].
            Lista base de los senders para la prueba."""

        uow = FakeUnitOfWorkAdapter(drivers = base_senders)

        handler = GetSenderHandler(unit_of_work = uow)
        
        with pytest.raises(SenderNotFound):
            handler.handle(query = GetSenderQuery(sender_id = "42"))
