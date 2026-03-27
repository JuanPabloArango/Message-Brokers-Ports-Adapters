"""Módulo que define la implementación de VO de tal manera que las tablas de
persistencia entiendan esta sintaxis de dominio."""

# Librerías Externas.
from typing import Union

from sqlalchemy import TypeDecorator, Dialect, Enum

# Librerías Internas.
from app.domain.value_objects.sender_status import SenderStatus


class CustomSenderStatus(TypeDecorator):
    """Clase que define el mapping de VOs a tablas de persistencia de tal
    manera que el interprete sepa cómo mapear valores de dominio."""

    cache_ok = True
    impl = Enum(SenderStatus)

    def process_bind_param(self, value: Union[SenderStatus, str], dialect: Dialect) -> str:
        """Método que se encarga de indicarle al Engine cómo debe mapear
        nuestro VO a un formato que él entienda.
        
        Args:
        ----------
        value: Union[SenderStatus, str].
            Estado actual del Sender.
        
        dialect: Dialect.
            Dialecto del Engine.
        
        Returns:
        ----------
        str.
            Estado del Sender a persistir."""
        
        if isinstance(value, str):
            return value
        return value.value
    
    def process_result_value(self, value: str, dialect: Dialect) -> SenderStatus:
        """Método que nos permite, a la hora de cargar, registros de tabla
        a entidades de dominio, mapear lo que dice la tabla con lo que tiene
        sentido para el dominio.
        
        Args:
        ----------
        value: str.
            Valor persistido en la tabla.
        
        dialect: Dialect.
            Dialecto del Engine.
        
        Returns:
        ----------
        SenderStatus.
            Estado del Sender."""
        
        return SenderStatus(value = value)
