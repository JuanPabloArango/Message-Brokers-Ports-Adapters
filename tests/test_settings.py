"""Módulo que contiene pruebas unitarias sobre la configuración de la app."""

# Librerías Externas
import pytest

# Librerías Internas.
from app.settings import Settings


class TestSettings:
    """Clase que encapsula las pruebas unitarias de configuración."""

    def test_development_database_url(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Método que contiene la prueba unitaria para validar la
        obtención de la URL de la base de datos a la cual
        conectarnos.
        
        Args:
        ----------
        monkeypatch: pytest.MonkeyPatch.
            Patch sobre el cual escribiremos la configuración de ambiente."""
        
        monkeypatch.setenv("ENVIRONMENT", "DEVELOPMENT")

        assert Settings.get_database_url() == "sqlite:///test.db"

    def test_production_database_url(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Método que contiene la prueba unitaria para validar la
        obtención de la URL de la base de datos a la cual
        conectarnos.
        
        Args:
        ----------
        monkeypatch: pytest.MonkeyPatch.
            Patch sobre el cual escribiremos la configuración de ambiente."""
        
        monkeypatch.setenv("ENVIRONMENT", "PRODUCTION")
        monkeypatch.setenv("USER", "random_user")
        monkeypatch.setenv("PASSWORD", "random_pass")
        monkeypatch.setenv("PORT", "1234")
        monkeypatch.setenv("HOST", "random_host")
        monkeypatch.setenv("DATABASE", "random_db")

        assert Settings.get_database_url() == "postgresql://random_user:random_pass@random_host:1234/random_db"

    