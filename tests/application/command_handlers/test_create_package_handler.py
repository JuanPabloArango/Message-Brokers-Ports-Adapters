"""Módulo que contiene pruebas unitarias para la creación de Packages."""

# Librerías Externas.
from typing import List

import pytest

# Librerías Internas.
from app.domain.entities.sender import Sender
from app.domain.entities.package import Package

from app.domain.value_objects.id import ID

from app.application.commands.create_package import CreatePackageCommand
from app.application.command_handlers.create_package import CreatePackageHandler

from app.domain.exceptions import SenderNotVerified
from app.application.exceptions import SenderNotFound

from app.infrastructure.persistence.repository.fake.uow import FakeUnitOfWorkAdapter


class TestCreatePackageHandler:
    """Módulo que contiene pruebas unitarias para el handler."""

    def test_correct_creation(self, base_senders: List[Sender]) -> None:
        """Método que contiene la prueba unitaria del happy path
        del handler.
        
        Args:
        ----------
        base_senders: List[Sender].
            Lista base de senders."""
        
        unit_of_work = FakeUnitOfWorkAdapter(senders = base_senders)

        handler = CreatePackageHandler(unit_of_work = unit_of_work)
        package_id = handler.handle(command = CreatePackageCommand(sender_id = "1"))

        assert package_id is not None, "Valide que se haya devuelto el ID."
        assert isinstance(package_id, str), "Valide que el ID sea correcto."

        package = unit_of_work.package_repository.get(package_id)

        assert isinstance(package, Package), "Valide que se haya creado una instancia correcta."
        assert package.sender_id == ID("1"), "Valide que se haya reportado el Sender ID al Package."

    def test_incorrect_creation_due_to_nonexistent_sender(self, base_senders: List[Sender]) -> None:
        """Método que contiene la prueba unitaria del happy path
        del handler.
        
        Args:
        ----------
        base_senders: List[Sender].
            Lista base de senders."""
        
        unit_of_work = FakeUnitOfWorkAdapter(senders = base_senders)

        handler = CreatePackageHandler(unit_of_work = unit_of_work)

        with pytest.raises(SenderNotFound):
            handler.handle(command = CreatePackageCommand(sender_id = "42"))

    def test_incorrect_creation_due_to_sender_unable_to_send(self, base_senders: List[Sender]) -> None:
        """Método que contiene la prueba unitaria del happy path
        del handler.
        
        Args:
        ----------
        base_senders: List[Sender].
            Lista base de senders."""
        
        unit_of_work = FakeUnitOfWorkAdapter(senders = base_senders)

        handler = CreatePackageHandler(unit_of_work = unit_of_work)

        with pytest.raises(SenderNotVerified):
            handler.handle(command = CreatePackageCommand(sender_id = "2"))
