"""Módulo que define la implementación de VO de tal manera que las tablas de
persistencia entiendan esta sintaxis de dominio."""

# Librerías Externas.
from typing import Union

from sqlalchemy import TypeDecorator, Dialect, Enum

# Librerías Internas.
from app.domain.value_objects.driver_status import DriverStatus


class CustomDriverStatus(TypeDecorator):
    """Clase que define el mapping de VOs a tablas de persistencia de tal
    manera que el interprete sepa cómo mapear valores de dominio."""

    cache_ok = True
    impl = Enum(DriverStatus)

    def process_bind_param(self, value: Union[DriverStatus, str], dialect: Dialect) -> str:
        """Método que se encarga de indicarle al Engine cómo debe mapear
        nuestro VO a un formato que él entienda.
        
        Args:
        ----------
        value: Union[DriverStatus, str].
            Estado actual del Driver.
        
        dialect: Dialect.
            Dialecto del Engine.
        
        Returns:
        ----------
        str.
            ID representado como string para que se pueda persistir."""
        
        if isinstance(value, str):
            return value
        return value.value
    
    def process_result_value(self, value: str, dialect: Dialect) -> DriverStatus:
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
        DriverStatus.
            Estado del Driver."""
        
        return DriverStatus(value = value)
