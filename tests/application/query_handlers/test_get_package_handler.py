"""Módulo que contiene las pruebas unitarias para el handler GetPackageHandler."""

# Librerías Externas.
from typing import List

import pytest

# Librerías Internas.
from app.domain.entities.package import Package
from app.domain.value_objects.package_status import PackageStatus

from app.application.dtos.package import PackageDTO

from app.application.queries.get_package_by_id import GetPackageQuery
from app.application.query_handlers.get_package import GetPackageHandler

from app.application.exceptions import PackageNotFound

from app.infrastructure.persistence.repository.fake.uow import FakeUnitOfWorkAdapter


class TestGetPackageHandler:
    """Módulo que encapsula las pruebas unitarias del handler."""

    def test_package_found_handler(self, base_packages: List[Package]) -> None:
        """Método que contiene la prueba unitaria del método 'handle' en el
        caso donde existe la entidad.
        
        Args:
        ----------
        base_packages: List[Package].
            Lista base de los packages para la prueba."""
        
        unit_of_work = FakeUnitOfWorkAdapter(packages = base_packages)

        handler = GetPackageHandler(unit_of_work = unit_of_work)
        package = handler.handle(query = GetPackageQuery(package_id = "2"))

        assert isinstance(package, PackageDTO), "Valide que la entidad obtenida sea del tipo correcto."
        assert package.status == "ASSIGNED", "Valide que haya obtenido la entidad esperada."

    def test_package_not_found_handler(self, base_packages: List[Package]) -> None:
        """Método que contiene la prueba unitaria del método 'handle' en el
        caso donde existe la entidad.
        
        Args:
        ----------
        base_packages: List[Package].
            Lista base de los packages para la prueba."""

        uow = FakeUnitOfWorkAdapter(packages = base_packages)

        handler = GetPackageHandler(unit_of_work = uow)

        with pytest.raises(PackageNotFound):
            handler.handle(query = GetPackageQuery(package_id = "42"))
