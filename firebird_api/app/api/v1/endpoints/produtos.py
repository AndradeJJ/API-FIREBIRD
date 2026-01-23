from fastapi import APIRouter, Depends, HTTPException, Query, status
from typing import List, Optional
from app.services.produto_service import ProdutoService
from app.models.produto import ProdutoCreate, ProdutoUpdate, ProdutoResponse
from app.api.dependencies import get_produto_service

router = APIRouter(prefix="/produtos", tags=["produtos"])

@router.get("/", response_model=List[ProdutoResponse])
async def listar_produtos(
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    service: ProdutoService = Depends(get_produto_service)
):
    """Lista todos os produtos com paginação"""
    return service.get_all_produtos(limit, offset)

@router.get("/ativos", response_model=List[ProdutoResponse])
async def listar_produtos_ativos(
    service: ProdutoService = Depends(get_produto_service)
):
    """Lista apenas produtos ativos"""
    return service.get_produtos_ativos()

@router.get("/estoque-baixo", response_model=List[ProdutoResponse])
async def listar_estoque_baixo(
    service: ProdutoService = Depends(get_produto_service)
):
    """Lista produtos com estoque abaixo do mínimo"""
    return service.get_estoque_baixo()

@router.get("/{produto_id}", response_model=ProdutoResponse)
async def buscar_produto(
    produto_id: int,
    service: ProdutoService = Depends(get_produto_service)
):
    """Busca produto por ID"""
    produto = service.get_produto_by_id(produto_id)
    if not produto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Produto com ID {produto_id} não encontrado"
        )
    return produto

@router.post("/", response_model=ProdutoResponse, status_code=status.HTTP_201_CREATED)
async def criar_produto(
    produto: ProdutoCreate,
    service: ProdutoService = Depends(get_produto_service)
):
    """Cria novo produto"""
    try:
        return service.create_produto(produto)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erro ao criar produto: {str(e)}"
        )

@router.put("/{produto_id}", response_model=ProdutoResponse)
async def atualizar_produto(
    produto_id: int,
    produto: ProdutoUpdate,
    service: ProdutoService = Depends(get_produto_service)
):
    """Atualiza produto existente"""
    updated = service.update_produto(produto_id, produto)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Produto com ID {produto_id} não encontrado"
        )
    return updated

@router.delete("/{produto_id}", status_code=status.HTTP_204_NO_CONTENT)
async def excluir_produto(
    produto_id: int,
    service: ProdutoService = Depends(get_produto_service)
):
    """Exclui produto (inativa)"""
    success = service.delete_produto(produto_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Produto com ID {produto_id} não encontrado"
        )

@router.get("/buscar/{descricao}", response_model=List[ProdutoResponse])
async def buscar_por_descricao(
    descricao: str,
    service: ProdutoService = Depends(get_produto_service)
):
    """Busca produtos por descrição"""
    return service.search_produtos(descricao)