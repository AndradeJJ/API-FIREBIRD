from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
import logging

logger = logging.getLogger(__name__)

class DatabaseConnector(ABC):
    """Interface para diferentes conectores de banco"""
    
    @abstractmethod
    def connect(self) -> Any:
        """Estabelece conexão com o banco"""
        pass
    
    @abstractmethod
    def disconnect(self) -> None:
        """Fecha conexão com o banco"""
        pass
    
    @abstractmethod
    def execute_query(self, query: str, params: Optional[Dict] = None) -> List[Dict]:
        """Executa query e retorna resultados"""
        pass
    
    @abstractmethod
    def execute_update(self, query: str, params: Optional[Dict] = None) -> int:
        """Executa INSERT/UPDATE/DELETE"""
        pass