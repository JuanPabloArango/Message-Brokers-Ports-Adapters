"""Clase que define el tipo de columna custom sobre las tablas de persistencia
para hacer una representación exacta del dominio en la infraestructura."""

# Librerías Externas.
from typing import Union

from sqlalchemy import TypeDecorator, Dialect, String

# Librerías Internas.
from app.domain.value_objects.id import ID


class CustomIDType(TypeDecorator):
    """Clase que define la representación del VO ID sobre las tablas de
    persistencia."""

    cache_ok = False
    impl = String(32)

    def process_bind_param(self, value: Union[str, ID], dialect: Dialect) -> Union[str, None]:
        """Método que se encarga de indicarle al Engine cómo debe mapear
        nuestro VO a un formato que él entienda.
        
        Args:
        ----------
        value: ID.
            ID de la entidad de dominio.
        
        dialect: Dialect.
            Dialecto del Engine.
        
        Returns:
        ----------
        Union[str, None].
            ID representado como string para que se pueda persistir. A veces podrá
            ser None cuando no se haya asignado Driver a un Package."""
        
        if isinstance(value, str):
            return value
        elif isinstance(value, ID):
            return value.value
        else:
            return None
    
    def process_result_value(self, value: str, dialect: Dialect) -> Union[ID, None]:
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
        Union[ID, None].
            ID que representa la identidad de la entidad. A veces puede ser None,
            en particular, cuando un Package aún no tiene ID Driver asignado."""
        
        if not value:
            return None
        return ID(value = value)
