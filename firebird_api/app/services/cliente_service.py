from app.repositories.cliente_repository import ClienteRepository
from app.models.cliente import ClienteCreate, ClienteUpdate, ClienteResponse
from typing import List, Optional, Dict
import logging

logger = logging.getLogger(__name__)

class ClienteService:
    """Serviço de lógica de negócio para clientes"""
    
    def __init__(self):
        self.repository = ClienteRepository()
    
    def get_all_clientes(self, limit: int = 100, offset: int = 0) -> List[ClienteResponse]:
        """Busca todos os clientes"""
        data = self.repository.get_all(limit, offset)
        return [ClienteResponse.from_dict(item) for item in data]
    
    def get_cliente_by_id(self, cliente_id: int) -> Optional[ClienteResponse]:
        """Busca cliente por ID"""
        data = self.repository.get_by_id(cliente_id)
        return ClienteResponse.from_dict(data) if data else None
    
    def create_cliente(self, cliente: ClienteCreate) -> ClienteResponse:
        """Cria novo cliente"""
        cliente_dict = cliente.to_dict()
        result = self.repository.create(cliente_dict)
        return ClienteResponse.from_dict(result)
    
    def update_cliente(self, cliente_id: int, cliente: ClienteUpdate) -> Optional[ClienteResponse]:
        """Atualiza cliente"""
        update_data = cliente.to_dict(exclude_unset=True)
        
        if not update_data:
            return None
        
        success = self.repository.update(cliente_id, update_data)
        if success:
            return self.get_cliente_by_id(cliente_id)
        return None
    
    def delete_cliente(self, cliente_id: int) -> bool:
        """Exclui cliente"""
        return self.repository.delete(cliente_id)
    
    def search_clientes(self, nome: str) -> List[ClienteResponse]:
        """Busca clientes por nome"""
        data = self.repository.search('NOME', nome)
        return [ClienteResponse.from_dict(item) for item in data]
    
    def get_clientes_ativos(self) -> List[ClienteResponse]:
        """Busca apenas clientes ativos"""
        data = self.repository.get_ativos()
        return [ClienteResponse.from_dict(item) for item in data]