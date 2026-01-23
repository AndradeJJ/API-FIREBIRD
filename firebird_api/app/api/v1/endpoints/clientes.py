from fastapi import APIRouter, Depends, HTTPException, Query, status
from typing import List, Optional
from app.services.cliente_service import ClienteService
from app.models.cliente import ClienteCreate, ClienteUpdate, ClienteResponse
from app.api.dependencies import get_cliente_service

router = APIRouter(prefix="/clientes", tags=["clientes"])

@router.get("/", response_model=List[ClienteResponse])
async def listar_clientes(
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    service: ClienteService = Depends(get_cliente_service)
):
    """Lista todos os clientes com paginação"""
    return service.get_all_clientes(limit, offset)

@router.get("/ativos", response_model=List[ClienteResponse])
async def listar_clientes_ativos(
    service: ClienteService = Depends(get_cliente_service)
):
    """Lista apenas clientes ativos"""
    return service.get_clientes_ativos()

@router.get("/{cliente_id}", response_model=ClienteResponse)
async def buscar_cliente(
    cliente_id: int,
    service: ClienteService = Depends(get_cliente_service)
):
    """Busca cliente por ID"""
    cliente = service.get_cliente_by_id(cliente_id)
    if not cliente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cliente com ID {cliente_id} não encontrado"
        )
    return cliente

@router.post("/", response_model=ClienteResponse, status_code=status.HTTP_201_CREATED)
async def criar_cliente(
    cliente: ClienteCreate,
    service: ClienteService = Depends(get_cliente_service)
):
    """Cria novo cliente"""
    try:
        return service.create_cliente(cliente)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erro ao criar cliente: {str(e)}"
        )

@router.put("/{cliente_id}", response_model=ClienteResponse)
async def atualizar_cliente(
    cliente_id: int,
    cliente: ClienteUpdate,
    service: ClienteService = Depends(get_cliente_service)
):
    """Atualiza cliente existente"""
    updated = service.update_cliente(cliente_id, cliente)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cliente com ID {cliente_id} não encontrado"
        )
    return updated

@router.delete("/{cliente_id}", status_code=status.HTTP_204_NO_CONTENT)
async def excluir_cliente(
    cliente_id: int,
    service: ClienteService = Depends(get_cliente_service)
):
    """Exclui cliente (inativa)"""
    success = service.delete_cliente(cliente_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cliente com ID {cliente_id} não encontrado"
        )

@router.get("/buscar/{nome}", response_model=List[ClienteResponse])
async def buscar_por_nome(
    nome: str,
    service: ClienteService = Depends(get_cliente_service)
):
    """Busca clientes por nome"""
    return service.search_clientes(nome)