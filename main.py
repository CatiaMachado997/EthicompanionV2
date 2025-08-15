from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend_app.api import router
from backend_app.core.config import load_api_keys, validate_api_keys
import logging
import os

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load API keys based on environment (Cloud Run or local)
try:
    load_api_keys()
    logger.info("🚀 API keys carregadas com sucesso")
    
    # Validar chaves (opcional - para debug)
    key_status = validate_api_keys()
    for key, status in key_status.items():
        logger.info(f"   {key}: {status}")
        
except Exception as e:
    logger.error(f"❌ Erro ao carregar configuração: {e}")
    # Continuar mesmo com erro para permitir debug

app = FastAPI(
    title="Chat Application API",
    description="API para aplicação de chat",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],  # Frontend Next.js
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 