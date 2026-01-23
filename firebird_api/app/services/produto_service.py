from app.repositories.produto_repository import ProdutoRepository
from app.models.produto import ProdutoCreate, ProdutoUpdate, ProdutoResponse
from typing import List, Optional, Dict
import logging

logger = logging.getLogger(__name__)

class ProdutoService:
    """Serviço de lógica de negócio para produtos"""
    
    def __init__(self):
        self.repository = ProdutoRepository()
    
    def get_all_produtos(self, limit: int = 100, offset: int = 0) -> List[ProdutoResponse]:
        """Busca todos os produtos"""
        data = self.repository.get_all(limit, offset)
        return [ProdutoResponse.from_dict(item) for item in data]
    
    def get_produto_by_id(self, produto_id: int) -> Optional[ProdutoResponse]:
        """Busca produto por ID"""
        data = self.repository.get_by_id(produto_id)
        return ProdutoResponse.from_dict(data) if data else None
    
    def create_produto(self, produto: ProdutoCreate) -> ProdutoResponse:
        """Cria novo produto"""
        produto_dict = produto.to_dict()
        result = self.repository.create(produto_dict)
        return ProdutoResponse.from_dict(result)
    
    def update_produto(self, produto_id: int, produto: ProdutoUpdate) -> Optional[ProdutoResponse]:
        """Atualiza produto"""
        update_data = produto.to_dict(exclude_unset=True)
        
        if not update_data:
            return None
        
        success = self.repository.update(produto_id, update_data)
        if success:
            return self.get_produto_by_id(produto_id)
        return None
    
    def delete_produto(self, produto_id: int) -> bool:
        """Exclui produto"""
        return self.repository.delete(produto_id)
    
    def search_produtos(self, descricao: str) -> List[ProdutoResponse]:
        """Busca produtos por descrição"""
        data = self.repository.search('DESCRICAO', descricao)
        return [ProdutoResponse.from_dict(item) for item in data]
    
    def get_produtos_ativos(self) -> List[ProdutoResponse]:
        """Busca apenas produtos ativos"""
        data = self.repository.get_ativos()
        return [ProdutoResponse.from_dict(item) for item in data]
    
    def get_estoque_baixo(self) -> List[ProdutoResponse]:
        """Busca produtos com estoque abaixo do mínimo"""
        data = self.repository.get_estoque_baixo()
        return [ProdutoResponse.from_dict(item) for item in data]