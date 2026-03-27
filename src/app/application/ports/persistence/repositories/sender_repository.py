"""Módulo que contiene la definición del puerto para el repositorio del Aggregate
Root Sender."""

# Librerías Externas.
from typing import List, Union
from abc import ABC, abstractmethod

# Librerías Internas.
from app.domain.entities.sender import Sender

from app.application.ports.persistence.criteria import Criteria


class SenderRepositoryPort(ABC):
    """Clase que define el contrato nominal para el puerto del repositorio
    de Sender."""

    @abstractmethod
    def get(self, sender_id: str) -> Union[Sender, None]:
        """Método abstracto que define parte del contrato nominal enfocado
        en la obtención de entidades según su primery key.
        
        Args:
        ----------
        sender_id: str.
            ID de la entidad a obtener de la BD.
            
        Returns:
        ----------
        Union[Sender, None].
            Entidad de dominio."""
        
        raise NotImplementedError("Si tu clase es una realización de 'SenderRepositoryPort', debes implementar el método 'get'.")
    
    @abstractmethod
    def save(self, sender: Sender) -> None:
        """Método abstracto que define parte del contrato nominal enfocado en el
        almacenamiento de entidades.
        
        Args:
        ----------
        sender: Sender.
            Entidad de dominio que desea almacenar."""
        
        raise NotImplementedError("Si tu clase es una realización de 'SenderRepositoryPort', debes implementar el método 'save'.")
    
    @abstractmethod
    def list_all(self, criteria: Criteria) -> List[Sender]:
        """Método abstracto que define parte del contrato nominal enfocado en la
        obtención de entidades Sender de acuerdo a criterios de filtro.

        Args:
        ----------
        criteria: Criteria.
            Objeto que contiene los filtros de búsqueda sobre las entidades.
        
        Returns:
        ----------
        List[Sender].
            Entidades de dominio que cumplen con los criterios de búsqueda."""
        
        raise NotImplementedError("Si tu clase es una realización de 'SenderRepositoryPort', debes implementar el método 'list_all'.")
