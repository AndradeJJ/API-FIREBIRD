from .base_model import BaseDBModel
from typing import Optional
from datetime import datetime

class ClienteBase(BaseDBModel):
    codigo: int
    nome: str
    tipo: Optional[str] = "F"  # F=Física, J=Jurídica
    cpf_cnpj: Optional[str] = None
    telefone: Optional[str] = None
    email: Optional[str] = None
    endereco: Optional[str] = None
    cidade: Optional[str] = None
    estado: Optional[str] = None
    cep: Optional[str] = None
    situacao: Optional[str] = "A"  # A=Ativo, I=Inativo
    data_cadastro: Optional[datetime] = None
    limite_credito: Optional[float] = 0.0
    observacao: Optional[str] = None

class ClienteCreate(ClienteBase):
    pass

class ClienteUpdate(BaseDBModel):
    nome: Optional[str] = None
    telefone: Optional[str] = None
    email: Optional[str] = None
    endereco: Optional[str] = None
    situacao: Optional[str] = None

class ClienteResponse(ClienteBase):
    pass