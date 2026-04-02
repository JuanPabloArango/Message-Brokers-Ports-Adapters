"""Módulo que contiene pruebas unitarias para un handler de Queries."""

# Librerías Externas.
from typing import List

# Librerías Internas.
from app.domain.entities.package import Package
from app.domain.value_objects.package_status import PackageStatus

from app.application.ports.persistence.criteria import Criteria, Filter, Operator

from app.application.queries.list_packages import ListPackagesQuery
from app.application.query_handlers.list_packages import ListPackagesHandler

from app.infrastructure.persistence.repository.fake.uow import FakeUnitOfWorkAdapter


class TestListPackagesHandler:
    """Clase que encapsula las pruebas unitarias para el handler ListPackagesHandler."""

    def test_list_many_packages_handler(self, base_packages: List[Package]) -> None:
        """Método que contiene la prueba unitaria del método 'handle' en el
        caso donde existe la entidad.
        
        Args:
        ----------
        base_packages: List[Package].
            Lista base de los paquetes para la prueba."""

        uow = FakeUnitOfWorkAdapter(packages = base_packages)

        criteria = Criteria(
            filters = [
                Filter(field = "driver_id", value = None, operator = Operator.NEQ)
            ]
        )

        handler = ListPackagesHandler(unit_of_work = uow)
        packages = handler.handle(query = ListPackagesQuery(criteria = criteria))

        assert len(packages) == 1, "Valide que haya obtenido la cantidad esperada de Packages."

    def test_list_no_packages_handler(self, base_packages: List[Package]) -> None:
        """Método que contiene la prueba unitaria del método 'handle' en el
        caso donde existe la entidad.
        
        Args:
        ----------
        base_packages: List[Package].
            Lista base de los paquetes para la prueba."""

        uow = FakeUnitOfWorkAdapter(packages = base_packages)

        criteria = Criteria(
            filters = [
                Filter(field = "status", value = PackageStatus.DELIVERED, operator = Operator.EQ)
            ]
        )

        handler = ListPackagesHandler(unit_of_work = uow)
        packages = handler.handle(query = ListPackagesQuery(criteria = criteria))

        assert len(packages) == 0, "Valide que haya obtenido la cantidad esperada de Packages."
