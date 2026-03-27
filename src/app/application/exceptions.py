"""Módulo que contiene las excepciones de aplicación."""


class ApplicationException(Exception):
    """Clase base que define la excepción base de aplicación para englobar
    todas las posibles excepciones que surjan en el mismo."""

    ...


class NotAValidAttribute(ApplicationException):
    """Clase que define errores sobre queries en nuestras entidades de
    dominio."""

    ...
    