"""Módulo que contiene pruebas unitarias de DTOs para transderencia de
data de dominio a componentes externos."""

# Librerías Externas.
from dataclasses import asdict

# Librerías Internas.
from app.domain.entities.sender import Sender

from app.application.dtos.sender import SenderDTO


class TestSenderDTO:
    """Clase que encapsula las pruebas unitarias de DTOs."""

    def test_basic_init(self) -> None:
        """Método que contiene la prueba unitaria de instanciación
        de un DTO de data cruda."""

        dto = SenderDTO(id = "123", status = "VERIFIED",
                        created_at = "2026-04-02 07:45:15", updated_at = "2026-04-02 07:45:15")
        
        assert asdict(dto) == {"id": "123", "status": "VERIFIED",
                               "created_at": "2026-04-02 07:45:15", "updated_at": "2026-04-02 07:45:15"}, "Valide que la información se conserva."
        
    def test_init_from_entity(self) -> None:
        """Método que contiene la prueba unitaria de instanciación desde
        una entidad."""

        sender = Sender()

        dto = SenderDTO.from_entity(sender = sender)

        assert isinstance(dto.id, str), "Valide que se mapean elementos de dominio a datos transferibles al exterior."
        assert len(dto.id) == 32, "Valide que se mapean elementos de dominio a datos transferibles al exterior."

        assert isinstance(dto.status, str), "Valide que se mapean elementos de dominio a datos transferibles al exterior."
        assert dto.status == "UNVERIFIED", "Valide que se mapean elementos de dominio a datos transferibles al exterior."
