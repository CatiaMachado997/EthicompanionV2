"""
Endpoint de Chat com Integração do Sistema de Memória Híbrida
Integra o MemoryManager com FastAPI para conversas com memória persistente
"""

# Carregar variáveis de ambiente PRIMEIRO
from dotenv import load_dotenv
load_dotenv()

from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
import weaviate
import logging
import json
import asyncio
from typing import Dict, Any, AsyncGenerator
from pydantic import BaseModel
import uuid
from datetime import datetime

# Configurar logging para ver mensagens de erro detalhadas
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from ..core.hybrid_memory_manager import MemoryManager
from ..models.database import get_db
from ..core.weaviate_client import get_weaviate_client
from ..core.ai_agent import get_ai_agent

# Router do FastAPI
chat_router = APIRouter(tags=["chat"])

# Modelos Pydantic
class ChatRequest(BaseModel):
    message: str
    session_id: str = None  # Opcional - será gerado se não fornecido
    context_mode: str = "hybrid"  # "hybrid", "recent_only", "semantic_only"

class ChatResponse(BaseModel):
    response: str
    session_id: str
    timestamp: str
    context_used: Dict[str, Any]
    memory_stats: Dict[str, Any]

class MemoryStatsResponse(BaseModel):
    stats: Dict[str, Any]
    status: str

# Dependência para obter MemoryManager
def get_memory_manager(
    db: Session = Depends(get_db),
    weaviate_client: weaviate.Client = Depends(get_weaviate_client)
) -> MemoryManager:
    """Cria uma instância do MemoryManager com as dependências necessárias"""
    try:
        return MemoryManager(db_session=db, weaviate_client=weaviate_client)
    except Exception as e:
        logger.error(f"❌ Erro ao criar MemoryManager: {e}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor de memória")

@chat_router.post("/message", response_model=ChatResponse)
async def chat_with_memory(
    request: ChatRequest,
    background_tasks: BackgroundTasks,
    memory_manager: MemoryManager = Depends(get_memory_manager),
    ai_agent = Depends(get_ai_agent)
):
    """
    Endpoint principal de chat com sistema de memória híbrida
    
    Fluxo:
    1. Gerar session_id se não fornecido
    2. Recuperar contexto do MemoryManager
    3. Processar mensagem com o agente AI
    4. Guardar conversa em background
    5. Retornar resposta com metadados
    """
    try:
        # 1. GESTÃO DE SESSÃO
        session_id = request.session_id or str(uuid.uuid4())
        timestamp = datetime.now()
        
        logger.info(f"💬 Nova mensagem recebida - Sessão: {session_id}")
        
        # 2. RECUPERAR CONTEXTO DA MEMÓRIA
        context = ""
        context_info = {"type": "none", "recent_count": 0, "semantic_count": 0}
        
        if request.context_mode in ["hybrid", "recent_only", "semantic_only"]:
            try:
                context = await memory_manager.get_context(
                    session_id=session_id,
                    query=request.message
                )
                
                # Extrair informações sobre o contexto usado
                context_info = _analyze_context(context)
                logger.info(f"🧠 Contexto recuperado: {context_info}")
                
            except Exception as e:
                logger.warning(f"⚠️ Erro ao recuperar contexto: {e}")
                context = "Contexto de memória não disponível."
        
        # 3. PREPARAR PROMPT PARA O AGENTE AI
        enhanced_prompt = _build_enhanced_prompt(request.message, context, request.context_mode)
        
        # 4. PROCESSAR COM AGENTE AI
        try:
            ai_response = await ai_agent.process_message(
                message=enhanced_prompt,
                session_id=session_id
            )
            
            if not ai_response or not ai_response.get("response"):
                raise Exception("Resposta vazia do agente AI")
                
            assistant_message = ai_response["response"]
            
        except Exception as e:
            # ADICIONAR LOGGING DETALHADO PARA DEPURAÇÃO
            logging.error(f"❌ FALHA AO PROCESSAR A MENSAGEM COM AGENTE AI: {e}", exc_info=True)
            assistant_message = "Desculpa, tive dificuldades em processar a tua mensagem. Podes tentar novamente?"
        
        # 5. GUARDAR CONVERSA EM BACKGROUND (não bloquear resposta)
        background_tasks.add_task(
            _save_conversation_background,
            memory_manager,
            session_id,
            request.message,
            assistant_message
        )
        
        # 6. OBTER ESTATÍSTICAS DE MEMÓRIA
        memory_stats = memory_manager.get_memory_stats()
        
        # 7. CONSTRUIR RESPOSTA
        response = ChatResponse(
            response=assistant_message,
            session_id=session_id,
            timestamp=timestamp.isoformat(),
            context_used=context_info,
            memory_stats=memory_stats
        )
        
        logger.info(f"✅ Resposta enviada - Sessão: {session_id}")
        return response
        
    except Exception as e:
        # ADICIONAR LOGGING DETALHADO PARA DEPURAÇÃO DO ENDPOINT PRINCIPAL
        logging.error(f"❌ FALHA CRÍTICA NO ENDPOINT DE CHAT: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Erro interno do servidor. Tenta novamente."
        )

@chat_router.post("/message/stream")
async def chat_with_memory_stream(
    request: ChatRequest,
    background_tasks: BackgroundTasks,
    memory_manager: MemoryManager = Depends(get_memory_manager),
    ai_agent = Depends(get_ai_agent)
):
    """
    Endpoint de chat com streaming para respostas em tempo real
    Retorna chunks de resposta conforme são gerados pelo AI
    """
    
    async def generate_stream() -> AsyncGenerator[str, None]:
        try:
            # 1. GESTÃO DE SESSÃO
            session_id = request.session_id or str(uuid.uuid4())
            timestamp = datetime.now()
            
            logger.info(f"🌊 Nova mensagem streaming - Sessão: {session_id}")
            
            # Enviar metadata inicial
            metadata = {
                "type": "metadata",
                "session_id": session_id,
                "timestamp": timestamp.isoformat(),
                "status": "processing"
            }
            yield f"data: {json.dumps(metadata)}\n\n"
            
            # 2. RECUPERAR CONTEXTO DA MEMÓRIA
            context = ""
            context_info = {"type": "none", "recent_count": 0, "semantic_count": 0}
            
            if request.context_mode in ["hybrid", "recent_only", "semantic_only"]:
                try:
                    context = await memory_manager.get_context(
                        session_id=session_id,
                        query=request.message
                    )
                    context_info = _analyze_context(context)
                    logger.info(f"🧠 Contexto recuperado para stream: {context_info}")
                    
                    # Enviar info do contexto
                    context_data = {
                        "type": "context",
                        "context_info": context_info
                    }
                    yield f"data: {json.dumps(context_data)}\n\n"
                    
                except Exception as e:
                    logger.warning(f"⚠️ Erro ao recuperar contexto: {e}")
                    context = "Contexto de memória não disponível."
            
            # 3. PREPARAR PROMPT
            enhanced_prompt = _build_enhanced_prompt(request.message, context, request.context_mode)
            
            # 4. PROCESSAR COM AGENTE AI E STREAM
            try:
                # Simular streaming por agora (mais tarde integrar com streaming real do LLM)
                ai_response = await ai_agent.process_message(
                    message=enhanced_prompt,
                    session_id=session_id
                )
                
                if not ai_response or not ai_response.get("response"):
                    raise Exception("Resposta vazia do agente AI")
                
                assistant_message = ai_response["response"]
                
                # Simular streaming dividindo a resposta em chunks
                words = assistant_message.split()
                chunk_size = 3  # palavras por chunk
                
                accumulated_response = ""
                
                for i in range(0, len(words), chunk_size):
                    chunk_words = words[i:i + chunk_size]
                    chunk_text = " ".join(chunk_words)
                    accumulated_response += chunk_text + " "
                    
                    chunk_data = {
                        "type": "content",
                        "chunk": chunk_text + " ",
                        "accumulated": accumulated_response.strip()
                    }
                    yield f"data: {json.dumps(chunk_data)}\n\n"
                    
                    # Pequena pausa para simular processamento
                    await asyncio.sleep(0.1)
                
                # 5. GUARDAR CONVERSA EM BACKGROUND
                background_tasks.add_task(
                    _save_conversation_background,
                    memory_manager,
                    session_id,
                    request.message,
                    assistant_message
                )
                
                # 6. OBTER ESTATÍSTICAS FINAIS
                memory_stats = memory_manager.get_memory_stats()
                
                # Enviar dados finais
                final_data = {
                    "type": "complete",
                    "session_id": session_id,
                    "timestamp": datetime.now().isoformat(),
                    "context_used": context_info,
                    "memory_stats": memory_stats,
                    "final_response": assistant_message
                }
                yield f"data: {json.dumps(final_data)}\n\n"
                
            except Exception as e:
                logging.error(f"❌ ERRO NO STREAMING: {e}", exc_info=True)
                error_data = {
                    "type": "error",
                    "message": "Desculpa, tive dificuldades em processar a tua mensagem. Podes tentar novamente?"
                }
                yield f"data: {json.dumps(error_data)}\n\n"
                
        except Exception as e:
            logging.error(f"❌ ERRO CRÍTICO NO STREAMING: {e}", exc_info=True)
            error_data = {
                "type": "error",
                "message": "Erro interno do servidor. Tenta novamente."
            }
            yield f"data: {json.dumps(error_data)}\n\n"
    
    return StreamingResponse(
        generate_stream(),
        media_type="text/plain",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Content-Type": "text/plain; charset=utf-8"
        }
    )

@chat_router.get("/memory/stats", response_model=MemoryStatsResponse)
async def get_memory_statistics(
    memory_manager: MemoryManager = Depends(get_memory_manager)
):
    """Endpoint para obter estatísticas do sistema de memória"""
    try:
        stats = memory_manager.get_memory_stats()
        
        return MemoryStatsResponse(
            stats=stats,
            status="success"
        )
        
    except Exception as e:
        logger.error(f"❌ Erro ao obter estatísticas: {e}")
        raise HTTPException(
            status_code=500,
            detail="Erro ao obter estatísticas de memória"
        )

@chat_router.get("/sessions/{session_id}/context")
async def get_session_context(
    session_id: str,
    query: str = "conversa geral",
    memory_manager: MemoryManager = Depends(get_memory_manager)
):
    """Endpoint para testar a recuperação de contexto para uma sessão específica"""
    try:
        context = await memory_manager.get_context(
            session_id=session_id,
            query=query
        )
        
        return {
            "session_id": session_id,
            "query": query,
            "context": context,
            "context_analysis": _analyze_context(context)
        }
        
    except Exception as e:
        logger.error(f"❌ Erro ao obter contexto da sessão: {e}")
        raise HTTPException(
            status_code=500,
            detail="Erro ao recuperar contexto da sessão"
        )

@chat_router.delete("/sessions/{session_id}")
async def clear_session_memory(
    session_id: str,
    memory_manager: MemoryManager = Depends(get_memory_manager)
):
    """Endpoint para limpar memória de uma sessão específica (opcional)"""
    try:
        # Implementar limpeza se necessário
        return {
            "message": f"Funcionalidade de limpeza de sessão {session_id} não implementada ainda",
            "status": "info"
        }
        
    except Exception as e:
        logger.error(f"❌ Erro ao limpar sessão: {e}")
        raise HTTPException(
            status_code=500,
            detail="Erro ao limpar memória da sessão"
        )

# FUNÇÕES AUXILIARES

def _build_enhanced_prompt(user_message: str, context: str, context_mode: str) -> str:
    """Constrói o prompt melhorado com contexto de memória"""
    
    if not context or context_mode == "none":
        return user_message
    
    enhanced_prompt = f"""CONTEXTO DE MEMÓRIA:
{context}

---

MENSAGEM ATUAL DO UTILIZADOR:
{user_message}

---

INSTRUÇÕES:
- Usa o contexto de memória acima para fornecer respostas mais personalizadas e consistentes
- Se houver informações relevantes no histórico, refere-te a elas de forma natural
- Mantém a continuidade das conversas anteriores quando apropriado
- Se não houver contexto relevante, responde normalmente à mensagem atual"""

    return enhanced_prompt

def _analyze_context(context: str) -> Dict[str, Any]:
    """Analisa o contexto retornado para extrair metadados"""
    analysis = {
        "type": "unknown",
        "recent_count": 0,
        "semantic_count": 0,
        "has_recent": False,
        "has_semantic": False
    }
    
    if not context:
        analysis["type"] = "none"
        return analysis
    
    # Contar secções
    if "HISTÓRICO RECENTE" in context:
        analysis["has_recent"] = True
        # Contar mensagens do utilizador no histórico recente
        recent_section = context.split("MEMÓRIAS RELEVANTES")[0]
        analysis["recent_count"] = recent_section.count("🙋 **Utilizador:**")
    
    if "MEMÓRIAS RELEVANTES" in context:
        analysis["has_semantic"] = True
        # Contar memórias relevantes
        semantic_section = context.split("MEMÓRIAS RELEVANTES")[1] if "MEMÓRIAS RELEVANTES" in context else ""
        analysis["semantic_count"] = semantic_section.count("**Memória")
    
    # Determinar tipo
    if analysis["has_recent"] and analysis["has_semantic"]:
        analysis["type"] = "hybrid"
    elif analysis["has_recent"]:
        analysis["type"] = "recent_only"
    elif analysis["has_semantic"]:
        analysis["type"] = "semantic_only"
    
    return analysis

async def _save_conversation_background(
    memory_manager: MemoryManager,
    session_id: str,
    user_message: str,
    assistant_message: str
):
    """Função para guardar conversa em background sem bloquear a resposta"""
    try:
        success = memory_manager.add_message(
            session_id=session_id,
            user_message=user_message,
            assistant_message=assistant_message
        )
        
        if success:
            logger.info(f"📝 Conversa guardada em background - Sessão: {session_id}")
        else:
            logger.error(f"❌ Falha ao guardar conversa - Sessão: {session_id}")
            
    except Exception as e:
        logger.error(f"❌ Erro crítico ao guardar conversa: {e}")

# Criar a aplicação FastAPI
app = FastAPI(
    title="Ethic Companion API",
    description="API para chat com sistema de memória híbrida",
    version="2.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware de limpeza (opcional)
@app.middleware("http")
async def cleanup_memory_manager(request, call_next):
    """Middleware para garantir limpeza do MemoryManager"""
    response = await call_next(request)
    
    # Aqui poderias adicionar limpeza se necessário
    # Por exemplo, fechar ligações não utilizadas
    
    return response

# Incluir routers
app.include_router(chat_router, prefix="/api")

# Endpoint raiz para teste
@app.get("/")
async def root():
    return {
        "message": "Ethic Companion API v2.0",
        "status": "operational",
        "features": ["hybrid_memory", "ai_agent", "ethics_guidance"]
    }
