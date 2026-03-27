"""Módulo que contiene la definición del puerto para el repositorio del Aggregate
Root Package."""

# Librerías Externas.
from typing import List, Union
from abc import ABC, abstractmethod

# Librerías Internas.
from app.domain.entities.package import Package

from app.application.ports.persistence.criteria import Criteria


class PackageRepositoryPort(ABC):
    """Clase que define el contrato nominal para el puerto del repositorio
    de Package."""

    @abstractmethod
    def get(self, package_id: str) -> Union[Package, None]:
        """Método abstracto que define parte del contrato nominal enfocado
        en la obtención de entidades según su primery key.
        
        Args:
        ----------
        package_id: str.
            ID de la entidad a obtener de la BD.
            
        Returns:
        ----------
        Union[Package, None].
            Entidad de dominio."""
        
        raise NotImplementedError("Si tu clase es una realización de 'PackageRepositoryPort', debes implementar el método 'get'.")
    
    @abstractmethod
    def save(self, package: Package) -> None:
        """Método abstracto que define parte del contrato nominal enfocado en el
        almacenamiento de entidades.
        
        Args:
        ----------
        package: Package.
            Entidad de dominio que desea almacenar."""
        
        raise NotImplementedError("Si tu clase es una realización de 'PackageRepositoryPort', debes implementar el método 'save'.")
    
    @abstractmethod
    def list_all(self, criteria: Criteria) -> List[Package]:
        """Método abstracto que define parte del contrato nominal enfocado en la
        obtención de entidades Package de acuerdo a criterios de filtro.

        Args:
        ----------
        criteria: Criteria.
            Objeto que contiene los filtros de búsqueda sobre las entidades.
        
        Returns:
        ----------
        List[Package].
            Entidades de dominio que cumplen con los criterios de búsqueda."""
        
        raise NotImplementedError("Si tu clase es una realización de 'PackageRepositoryPort', debes implementar el método 'list_all'.")
