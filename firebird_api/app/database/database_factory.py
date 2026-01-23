from .firebird_connector import FirebirdConnector
from app.config import settings
import logging

logger = logging.getLogger(__name__)

class DatabaseFactory:
    """Factory para criar instâncias de conectores de banco"""
    
    _connectors = {
        'firebird': FirebirdConnector,
        # Adicionar outros bancos no futuro:
        # 'postgresql': PostgreSQLConnector,
        # 'mysql': MySQLConnector,
        # 'sqlite': SQLiteConnector
    }
    
    @classmethod
    def get_connector(cls, db_type: str = None):
        """Retorna instância do conector baseado no tipo"""
        if not db_type:
            db_type = settings.database_type
        
        if db_type not in cls._connectors:
            raise ValueError(f"Banco de dados não suportado: {db_type}")
        
        logger.info(f"Usando conector para: {db_type}")
        return cls._connectors[db_type]()
    
    @classmethod
    def register_connector(cls, db_type: str, connector_class):
        """Registra novo tipo de conector"""
        cls._connectors[db_type] = connector_class
        logger.info(f"Novo conector registrado: {db_type}")