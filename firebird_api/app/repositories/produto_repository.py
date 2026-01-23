from .base_repository import BaseRepository
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)

class ProdutoRepository(BaseRepository):
    """Repositório específico para produtos"""
    
    def __init__(self):
        super().__init__("PRODUTO")
    
    def create(self, data: Dict) -> Dict:
        """Cria novo produto"""
        if 'CODIGO' not in data:
            max_query = "SELECT MAX(CODIGO) as max_code FROM PRODUTO"
            result = self.db.execute_query(max_query)
            next_code = (result[0]['max_code'] or 0) + 1
            data['CODIGO'] = next_code
        
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['?'] * len(data))
        query = f"INSERT INTO PRODUTO ({columns}) VALUES ({placeholders})"
        
        self.db.execute_update(query, data)
        return self.get_by_id(data['CODIGO'])
    
    def update(self, id: int, data: Dict) -> bool:
        """Atualiza produto"""
        if not data:
            return False
        
        set_clause = ', '.join([f"{k} = ?" for k in data.keys()])
        query = f"UPDATE PRODUTO SET {set_clause} WHERE CODIGO = ?"
        
        params = list(data.values())
        params.append(id)
        
        rows = self.db.execute_update(query, params)
        return rows > 0
    
    def delete(self, id: int) -> bool:
        """Exclui produto (inativa)"""
        query = "UPDATE PRODUTO SET SITUACAO = 'I' WHERE CODIGO = ?"
        rows = self.db.execute_update(query, [id])
        return rows > 0
    
    def get_ativos(self) -> List[Dict]:
        """Busca apenas produtos ativos"""
        query = "SELECT * FROM PRODUTO WHERE SITUACAO = 'A' ORDER BY DESCRICAO"
        return self.db.execute_query(query)
    
    def get_estoque_baixo(self, min_estoque: float = 0) -> List[Dict]:
        """Busca produtos com estoque abaixo do mínimo"""
        query = """
            SELECT * FROM PRODUTO 
            WHERE ESTOQUE_ATUAL <= ESTOQUE_MINIMO 
            AND SITUACAO = 'A'
            ORDER BY ESTOQUE_ATUAL ASC
        """
        return self.db.execute_query(query)