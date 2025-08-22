"""
Exemplo de Integração do Sistema de Memória Híbrida no FastAPI
Mostra como adicionar os novos endpoints ao main.py
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import logging

# Imports do sistema de memória
from backend_app.api.chat_with_memory import chat_router
from backend_app.models.database import create_tables
from backend_app.core.weaviate_client import test_weaviate_connection
from backend_app.core.ai_agent import get_ai_agent

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Criar aplicação FastAPI
app = FastAPI(
    title="Ethic Companion V2 - Hybrid Memory System",
    description="Sistema de IA com memória híbrida para questões éticas e desenvolvimento pessoal",
    version="2.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # Frontend Next.js
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicialização da aplicação
@app.on_event("startup")
async def startup_event():
    """Inicialização do sistema no arranque"""
    logger.info("🚀 Iniciando Ethic Companion V2...")
    
    # 1. Criar tabelas da base de dados
    try:
        create_tables()
        logger.info("✅ Tabelas da base de dados criadas/verificadas")
    except Exception as e:
        logger.error(f"❌ Erro ao criar tabelas: {e}")
    
    # 2. Testar ligação Weaviate
    try:
        weaviate_status = test_weaviate_connection()
        if weaviate_status["status"] == "connected":
            logger.info("✅ Weaviate conectado e operacional")
        else:
            logger.warning(f"⚠️ Weaviate: {weaviate_status.get('error', 'Estado desconhecido')}")
    except Exception as e:
        logger.warning(f"⚠️ Não foi possível verificar Weaviate: {e}")
    
    # 3. Inicializar agente AI
    try:
        ai_agent = get_ai_agent()
        agent_status = ai_agent.get_agent_status()
        logger.info(f"✅ Agente AI: {agent_status['status']} ({agent_status['llm_type']})")
    except Exception as e:
        logger.warning(f"⚠️ Agente AI limitado: {e}")
    
    logger.info("🎉 Sistema inicializado com sucesso!")

@app.on_event("shutdown")
async def shutdown_event():
    """Limpeza no encerramento"""
    logger.info("🔒 Encerrando Ethic Companion V2...")
    # Aqui podes adicionar limpeza específica se necessário
    logger.info("✅ Encerramento completo")

# Incluir routers
app.include_router(chat_router)  # Endpoints de chat com memória

# Endpoints básicos
@app.get("/")
async def root():
    """Endpoint raiz com informações básicas"""
    return {
        "message": "Ethic Companion V2 - Sistema de Memória Híbrida",
        "version": "2.0.0",
        "status": "operational",
        "endpoints": {
            "chat": "/api/chat/message",
            "memory_stats": "/api/chat/memory/stats",
            "session_context": "/api/chat/sessions/{session_id}/context",
            "health": "/health",
            "docs": "/docs"
        }
    }

@app.get("/health")
async def health_check():
    """Endpoint de verificação de saúde do sistema"""
    try:
        # Testar componentes críticos
        health_status = {
            "status": "healthy",
            "timestamp": "2024-01-01T00:00:00",  # datetime.now().isoformat()
            "components": {}
        }
        
        # Testar base de dados
        try:
            from backend_app.models.database import get_db_session
            db = get_db_session()
            db.execute("SELECT 1")
            db.close()
            health_status["components"]["database"] = "healthy"
        except Exception as e:
            health_status["components"]["database"] = f"unhealthy: {e}"
            health_status["status"] = "degraded"
        
        # Testar Weaviate
        try:
            weaviate_status = test_weaviate_connection()
            if weaviate_status["status"] == "connected":
                health_status["components"]["weaviate"] = "healthy"
            else:
                health_status["components"]["weaviate"] = f"unhealthy: {weaviate_status.get('error', 'unknown')}"
                health_status["status"] = "degraded"
        except Exception as e:
            health_status["components"]["weaviate"] = f"unhealthy: {e}"
            health_status["status"] = "degraded"
        
        # Testar agente AI
        try:
            ai_agent = get_ai_agent()
            agent_status = ai_agent.get_agent_status()
            if agent_status["status"] == "operational":
                health_status["components"]["ai_agent"] = "healthy"
            else:
                health_status["components"]["ai_agent"] = "limited"
                health_status["status"] = "degraded"
        except Exception as e:
            health_status["components"]["ai_agent"] = f"unhealthy: {e}"
            health_status["status"] = "degraded"
        
        return health_status
        
    except Exception as e:
        logger.error(f"❌ Erro no health check: {e}")
        raise HTTPException(status_code=500, detail="Erro interno no health check")

# Endpoint de debug (remover em produção)
@app.get("/debug/system-info")
async def debug_system_info():
    """Informações de debug do sistema (apenas para desenvolvimento)"""
    try:
        from backend_app.core.ai_agent import get_ai_agent
        from backend_app.core.weaviate_client import test_weaviate_connection
        
        ai_agent = get_ai_agent()
        
        return {
            "ai_agent": ai_agent.get_agent_status(),
            "weaviate": test_weaviate_connection(),
            "environment": {
                "openai_key_set": bool(os.getenv("OPENAI_API_KEY")),
                "google_key_set": bool(os.getenv("GOOGLE_API_KEY")),
                "weaviate_url": os.getenv("WEAVIATE_URL", "http://localhost:8080"),
                "database_url_set": bool(os.getenv("DATABASE_URL"))
            }
        }
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main_example:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

"""
INSTRUÇÕES PARA INTEGRAÇÃO:

1. **Copiar para main.py:**
   - Copiar as partes relevantes para o teu main.py existente
   - Especialmente: imports, router inclusion, startup/shutdown events

2. **Variáveis de Ambiente Necessárias:**
   ```bash
   # LLM APIs
   OPENAI_API_KEY=sk-...
   GOOGLE_API_KEY=AI...
   
   # Weaviate
   WEAVIATE_URL=http://localhost:8080
   WEAVIATE_API_KEY=optional_if_auth_enabled
   
   # Base de Dados
   DATABASE_URL=postgresql://user:pass@localhost/ethic_companion
   # ou para SQLite: sqlite:///./ethic_companion.db
   
   # Tavily Search (opcional)
   TAVILY_API_KEY=tvly-...
   ```

3. **Dependências pip:**
   ```bash
   pip install sqlalchemy psycopg2-binary weaviate-client
   pip install langchain langchain-openai langchain-google-genai
   pip install uvicorn fastapi
   ```

4. **Testar o Sistema:**
   ```bash
   # Executar teste
   python test_hybrid_memory.py
   
   # Executar servidor
   python main.py
   
   # Testar endpoint
   curl -X POST "http://localhost:8000/api/chat/message" \
        -H "Content-Type: application/json" \
        -d '{"message": "Olá! Como posso navegar um dilema ético?"}'
   ```

5. **Integração Frontend:**
   - Os endpoints estão prontos para integração com Next.js
   - Usar /api/chat/message para conversas
   - Usar /api/chat/memory/stats para estatísticas
   - Usar /health para monitorização
"""
