from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.config import settings
from app.api.v1.endpoints import clientes, produtos
import logging
import sys

# Configuração de logging
logging.basicConfig(
    level=logging.DEBUG if settings.debug else logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('api.log')
    ]
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gerencia ciclo de vida da aplicação"""
    # Startup
    logger.info("Iniciando API Firebird Sync")
    logger.info(f"Conectando ao banco: {settings.database_type}")
    
    yield
    
    # Shutdown
    logger.info("Encerrando API Firebird Sync")

# Cria aplicação FastAPI
app = FastAPI(
    title="API Firebird Sync",
    description="API REST para sincronização com banco Firebird",
    version="1.0.0",
    lifespan=lifespan
)

# Configura CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especificar origens
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclui rotas
app.include_router(clientes.router)
app.include_router(produtos.router)

@app.get("/")
async def root():
    """Endpoint raiz da API"""
    return {
        "message": "API Firebird Sync - Online",
        "version": "1.0.0",
        "database": settings.database_type,
        "docs": "/docs",
        "redoc": "/redoc"
    }

@app.get("/health")
async def health_check():
    """Endpoint de verificação de saúde"""
    return {
        "status": "healthy",
        "database": settings.database_type
    }

@app.get("/config")
async def show_config():
    """Exibe configurações (apenas em debug)"""
    if not settings.debug:
        raise HTTPException(status_code=403, detail="Acesso negado")
    
    return {
        "database": {
            "type": settings.database_type,
            "host": settings.firebird_host,
            "port": settings.firebird_port,
            "database": settings.firebird_database,
            "user": settings.firebird_user
        },
        "api": {
            "host": settings.api_host,
            "port": settings.api_port,
            "debug": settings.debug
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.debug
    )