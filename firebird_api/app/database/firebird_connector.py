import fdb
from typing import Dict, List, Optional
from .base import DatabaseConnector
from app.config import settings
import logging

logger = logging.getLogger(__name__)

class FirebirdConnector(DatabaseConnector):
    """Conector específico para Firebird 2.5.9+"""
    
    def __init__(self):
        self.connection = None
        self._build_connection_string()
    
    def _build_connection_string(self) -> Dict:
        """Constrói dicionário de conexão"""
        self.conn_params = {
            'host': settings.firebird_host,
            'port': settings.firebird_port,
            'database': settings.firebird_database,
            'user': settings.firebird_user,
            'password': settings.firebird_password,
            'charset': settings.firebird_charset
        }
        logger.debug(f"Parâmetros de conexão: {self.conn_params}")
    
    def connect(self) -> fdb.Connection:
        """Estabelece conexão com Firebird"""
        try:
            if not self.connection:
                self.connection = fdb.connect(**self.conn_params)
                logger.info("Conexão com Firebird estabelecida")
            return self.connection
        except fdb.Error as e:
            logger.error(f"Erro ao conectar ao Firebird: {e}")
            raise
    
    def disconnect(self) -> None:
        """Fecha conexão"""
        if self.connection:
            self.connection.close()
            self.connection = None
            logger.info("Conexão com Firebird fechada")
    
    def execute_query(self, query: str, params: Optional[Dict] = None) -> List[Dict]:
        """Executa SELECT e retorna lista de dicionários"""
        conn = self.connect()
        cursor = conn.cursor()
        
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            # Converte resultados para dicionário
            columns = [desc[0] for desc in cursor.description]
            results = []
            
            for row in cursor.fetchall():
                results.append(dict(zip(columns, row)))
            
            return results
        except fdb.Error as e:
            logger.error(f"Erro na query: {query} - {e}")
            raise
        finally:
            cursor.close()
    
    def execute_update(self, query: str, params: Optional[Dict] = None) -> int:
        """Executa INSERT/UPDATE/DELETE e retorna linhas afetadas"""
        conn = self.connect()
        cursor = conn.cursor()
        
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            conn.commit()
            rows_affected = cursor.rowcount
            logger.debug(f"Query executada: {rows_affected} linhas afetadas")
            return rows_affected
        except fdb.Error as e:
            conn.rollback()
            logger.error(f"Erro na atualização: {query} - {e}")
            raise
        finally:
            cursor.close()