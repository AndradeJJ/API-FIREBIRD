from .base_model import BaseDBModel
from typing import Optional
from datetime import datetime

class ProdutoBase(BaseDBModel):
    codigo: int
    descricao: str
    codigo_barra: Optional[str] = None
    unidade: Optional[str] = "UN"
    preco_custo: Optional[float] = 0.0
    preco_venda: Optional[float] = 0.0
    estoque_atual: Optional[float] = 0.0
    estoque_minimo: Optional[float] = 0.0
    cod_grupo: Optional[int] = None
    cod_subgrupo: Optional[int] = None
    cod_secao: Optional[int] = None
    cod_marca: Optional[int] = None
    situacao: Optional[str] = "A"  # A=Ativo, I=Inativo
    data_cadastro: Optional[datetime] = None
    peso: Optional[float] = 0.0
    ncm: Optional[str] = None
    cest: Optional[str] = None
    observacao: Optional[str] = None

class ProdutoCreate(ProdutoBase):
    pass

class ProdutoUpdate(BaseDBModel):
    descricao: Optional[str] = None
    preco_venda: Optional[float] = None
    estoque_atual: Optional[float] = None
    situacao: Optional[str] = None

class ProdutoResponse(ProdutoBase):
    pass