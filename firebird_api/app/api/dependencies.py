from app.services.cliente_service import ClienteService
from app.services.produto_service import ProdutoService

def get_cliente_service() -> ClienteService:
    """Dependency injection para ClienteService"""
    return ClienteService()

def get_produto_service() -> ProdutoService:
    """Dependency injection para ProdutoService"""
    return ProdutoService()