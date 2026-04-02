"""Módulo que contiene pruebas unitarias para un handler de Queries."""

# Librerías Externas.
from typing import List

# Librerías Internas.
from app.domain.entities.sender import Sender
from app.domain.value_objects.sender_status import SenderStatus

from app.application.ports.persistence.criteria import Criteria, Filter, Operator

from app.application.queries.list_senders import ListSendersQuery
from app.application.query_handlers.list_senders import ListSendersHandler

from app.infrastructure.persistence.repository.fake.uow import FakeUnitOfWorkAdapter


class TestListSenderssHandler:
    """Clase que encapsula las pruebas unitarias para el handler ListSenderssHandler."""

    def test_list_many_senders_handler(self, base_senders: List[Sender]) -> None:
        """Método que contiene la prueba unitaria del método 'handle' en el
        caso donde existe la entidad.
        
        Args:
        ----------
        base_senders: List[Sender].
            Lista base de los senders para la prueba."""

        uow = FakeUnitOfWorkAdapter(senders = base_senders)

        criteria = Criteria(
            filters = [
                Filter(field = "status", value = SenderStatus.VERIFIED, operator = Operator.EQ)
            ]
        )

        handler = ListSendersHandler(unit_of_work = uow)
        senders = handler.handle(query = ListSendersQuery(criteria = criteria))

        assert len(senders) == 2, "Valide que haya obtenido la cantidad esperada de Senders."

    def test_list_no_senders_handler(self, base_senders: List[Sender]) -> None:
        """Método que contiene la prueba unitaria del método 'handle' en el
        caso donde existe la entidad.
        
        Args:
        ----------
        base_senders: List[Sender].
            Lista base de los senders para la prueba."""

        uow = FakeUnitOfWorkAdapter(senders = base_senders)

        criteria = Criteria(
            filters = [
                Filter(field = "created_at", value = "2027-10-31", operator = Operator.EQ)
            ]
        )

        handler = ListSendersHandler(unit_of_work = uow)
        senders = handler.handle(query = ListSendersQuery(criteria = criteria))

        assert len(senders) == 0, "Valide que haya obtenido la cantidad esperada de Senders."
