from pydantic import BaseModel, ConfigDict
from typing import Optional, Any
from datetime import datetime

class BaseDBModel(BaseModel):
    """Modelo base com configurações padrão"""
    model_config = ConfigDict(from_attributes=True)
    
    @classmethod
    def from_dict(cls, data: dict):
        """Cria instância do modelo a partir de dicionário"""
        return cls(**data)
    
    def to_dict(self) -> dict:
        """Converte modelo para dicionário"""
        return self.model_dump()