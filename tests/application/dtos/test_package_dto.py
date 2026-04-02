"""Módulo que contiene pruebas unitarias de DTOs para transderencia de
data de dominio a componentes externos."""

# Librerías Externas.
from dataclasses import asdict

# Librerías Internas.
from app.domain.entities.package import Package
from app.domain.value_objects.id import ID

from app.application.dtos.package import PackageDTO


class TestPackageDTO:
    """Clase que encapsula las pruebas unitarias de DTOs."""

    def test_basic_init(self) -> None:
        """Método que contiene la prueba unitaria de instanciación
        de un DTO de data cruda."""

        dto = PackageDTO(id = "123", sender_id = "43", driver_id = None, status = "ASSIGNED",
                        created_at = "2026-04-02 07:45:15", updated_at = "2026-04-02 07:45:15")
        
        assert asdict(dto) == {"id": "123", "sender_id": "43", "driver_id": None, "status": "ASSIGNED",
                               "created_at": "2026-04-02 07:45:15", "updated_at": "2026-04-02 07:45:15"}, "Valide que la información se conserva."
        
    def test_init_from_entity(self) -> None:
        """Método que contiene la prueba unitaria de instanciación desde
        una entidad."""

        package = Package(sender_id = ID("43"))

        dto = PackageDTO.from_entity(package = package)

        assert isinstance(dto.id, str), "Valide que se mapean elementos de dominio a datos transferibles al exterior."
        assert len(dto.id) == 32, "Valide que se mapean elementos de dominio a datos transferibles al exterior."

        assert isinstance(dto.sender_id, str), "Valide que se mapean elementos de dominio a datos transferibles al exterior."
        assert dto.sender_id == "43", "Valide que se mapean elementos de dominio a datos transferibles al exterior."

        assert not dto.driver_id, "Valide que se mapean elementos de dominio a datos transferibles al exterior."

        assert isinstance(dto.status, str), "Valide que se mapean elementos de dominio a datos transferibles al exterior."
        assert dto.status == "PENDING", "Valide que se mapean elementos de dominio a datos transferibles al exterior."
