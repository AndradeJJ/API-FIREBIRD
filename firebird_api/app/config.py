from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Configurações do Banco
    database_type: str = "firebird"
    
    # Firebird
    firebird_host: str = "localhost"
    firebird_port: int = 3050
    firebird_database: str = "C:\\Ganso\\Dados\\Validacao\\Constru.IB"  
    firebird_user: str = "SYSDBA"
    firebird_password: str = "1652498327"
    firebird_charset: str = "UTF8"
    
    # API
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    debug: bool = True
    
    class Config:
        env_file = ".env"

settings = Settings()