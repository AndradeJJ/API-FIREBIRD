from .base_repository import BaseRepository
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)

class ClienteRepository(BaseRepository):
    """Repositório específico para clientes"""
    
    def __init__(self):
        super().__init__("CLIENTE")
    
    def create(self, data: Dict) -> Dict:
        """Cria novo cliente"""
        # Gera próximo código se não fornecido
        if 'CODIGO' not in data:
            max_query = "SELECT MAX(CODIGO) as max_code FROM CLIENTE"
            result = self.db.execute_query(max_query)
            next_code = (result[0]['max_code'] or 0) + 1
            data['CODIGO'] = next_code
        
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['?'] * len(data))
        query = f"INSERT INTO CLIENTE ({columns}) VALUES ({placeholders})"
        
        self.db.execute_update(query, data)
        return self.get_by_id(data['CODIGO'])
    
    def update(self, id: int, data: Dict) -> bool:
        """Atualiza cliente"""
        if not data:
            return False
        
        set_clause = ', '.join([f"{k} = ?" for k in data.keys()])
        query = f"UPDATE CLIENTE SET {set_clause} WHERE CODIGO = ?"
        
        params = list(data.values())
        params.append(id)
        
        rows = self.db.execute_update(query, params)
        return rows > 0
    
    def delete(self, id: int) -> bool:
        """Exclui cliente (inativa)"""
        query = "UPDATE CLIENTE SET SITUACAO = 'I' WHERE CODIGO = ?"
        rows = self.db.execute_update(query, [id])
        return rows > 0
    
    def get_ativos(self) -> List[Dict]:
        """Busca apenas clientes ativos"""
        query = "SELECT * FROM CLIENTE WHERE SITUACAO = 'A' ORDER BY NOME"
        return self.db.execute_query(query)