from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any, Type
from app.database.database_factory import DatabaseFactory
import logging

logger = logging.getLogger(__name__)

class BaseRepository(ABC):
    """Repositório base para operações CRUD"""
    
    def __init__(self, table_name: str):
        self.table_name = table_name
        self.db = DatabaseFactory.get_connector()
        self._initialize()
    
    def _initialize(self):
        """Inicializa repositório"""
        logger.info(f"Repositório inicializado para tabela: {self.table_name}")
    
    def get_all(self, limit: int = 100, offset: int = 0) -> List[Dict]:
        """Busca todos os registros com paginação"""
        query = f"SELECT FIRST {limit} SKIP {offset} * FROM {self.table_name} ORDER BY CODIGO"
        return self.db.execute_query(query)
    
    def get_by_id(self, id: int) -> Optional[Dict]:
        """Busca registro por ID"""
        query = f"SELECT * FROM {self.table_name} WHERE CODIGO = ?"
        results = self.db.execute_query(query, {'CODIGO': id})
        return results[0] if results else None
    
    def search(self, field: str, value: Any) -> List[Dict]:
        """Busca por campo específico"""
        query = f"SELECT * FROM {self.table_name} WHERE {field} LIKE ?"
        return self.db.execute_query(query, {field: f'%{value}%'})
    
    def count(self) -> int:
        """Conta total de registros"""
        query = f"SELECT COUNT(*) as total FROM {self.table_name}"
        result = self.db.execute_query(query)
        return result[0]['total'] if result else 0
    
    @abstractmethod
    def create(self, data: Dict) -> Dict:
        """Cria novo registro"""
        pass
    
    @abstractmethod
    def update(self, id: int, data: Dict) -> bool:
        """Atualiza registro"""
        pass
    
    @abstractmethod
    def delete(self, id: int) -> bool:
        """Exclui registro"""
        pass