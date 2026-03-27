"""Módulo que define la implementación de VO de tal manera que las tablas de
persistencia entiendan esta sintaxis de dominio."""

# Librerías Externas.
from typing import Union

import datetime as dt

from sqlalchemy import TypeDecorator, Dialect, DateTime

# Librerías Internas.
from app.domain.value_objects.delivery_date import DeliveryDate


class CustomDeliveryDate(TypeDecorator):
    """Clase que define el mapping de VOs a tablas de persistencia de tal
    manera que el interprete sepa cómo mapear valores de dominio."""

    cache_ok = True
    impl = DateTime()

    def process_bind_param(self, value: DeliveryDate, dialect: Dialect) -> Union[dt.datetime, None]:
        """Método que se encarga de indicarle al Engine cómo debe mapear
        nuestro VO a un formato que él entienda.
        
        Args:
        ----------
        value: DeliveryDate.
            Momento del último envío del conductor.
        
        dialect: Dialect.
            Dialecto del Engine.
        
        Returns:
        ----------
        Union[dt.datetime, None].
            Fecha del último envío del Driver."""
        
        return value.last_delivery
    
    def process_result_value(self, value: Union[dt.datetime, None], dialect: Dialect) -> DeliveryDate:
        """Método que nos permite, a la hora de cargar, registros de tabla
        a entidades de dominio, mapear lo que dice la tabla con lo que tiene
        sentido para el dominio.
        
        Args:
        ----------
        value: Union[dt.datetime, None].
            Valor persistido en la tabla.
        
        dialect: Dialect.
            Dialecto del Engine.
        
        Returns:
        ----------
        DeliveryDate.
            Fecha del último envío."""
        
        if value:
            value = dt.datetime.strftime(value, format = "%Y-%m-%d %H:%M:%S")
        return DeliveryDate(last_delivery = value)
