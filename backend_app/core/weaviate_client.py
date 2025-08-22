"""
Cliente Weaviate Configurado
Fornece cliente Weaviate configurado para uso no sistema de memória
"""

import weaviate
import os
import logging
from typing import Optional

logger = logging.getLogger(__name__)

# Cliente Weaviate global
_weaviate_client: Optional[weaviate.Client] = None

def create_weaviate_client() -> weaviate.Client:
    """
    Cria e configura cliente Weaviate com autenticação
    
    Returns:
        weaviate.Client: Cliente configurado e autenticado
    """
    global _weaviate_client
    
    if _weaviate_client is not None:
        return _weaviate_client
    
    try:
        # Configuração baseada em variáveis de ambiente
        weaviate_url = os.getenv("WEAVIATE_URL", "http://localhost:8080")
        weaviate_api_key = os.getenv("WEAVIATE_API_KEY")
        openai_api_key = os.getenv("OPENAI_API_KEY")
        
        # Configurar autenticação se API key estiver disponível
        auth_config = None
        if weaviate_api_key:
            auth_config = weaviate.AuthApiKey(api_key=weaviate_api_key)
        
        # Configurar cabeçalhos para OpenAI (para vetorização)
        additional_headers = {}
        if openai_api_key:
            additional_headers["X-OpenAI-Api-Key"] = openai_api_key
        
        # Criar cliente
        _weaviate_client = weaviate.Client(
            url=weaviate_url,
            auth_client_secret=auth_config,
            additional_headers=additional_headers,
            timeout_config=(5, 60)  # connect timeout, read timeout
        )
        
        # Testar ligação
        if _weaviate_client.is_ready():
            logger.info(f"✅ Cliente Weaviate conectado: {weaviate_url}")
        else:
            raise Exception("Weaviate não está pronto")
            
        return _weaviate_client
        
    except Exception as e:
        logger.error(f"❌ Erro ao conectar Weaviate: {e}")
        raise

def get_weaviate_client() -> weaviate.Client:
    """
    Dependência FastAPI para obter cliente Weaviate
    
    Returns:
        weaviate.Client: Cliente Weaviate configurado
    """
    global _weaviate_client
    
    if _weaviate_client is None:
        _weaviate_client = create_weaviate_client()
    
    return _weaviate_client

def close_weaviate_client():
    """Fecha cliente Weaviate se existir"""
    global _weaviate_client
    
    if _weaviate_client is not None:
        try:
            # Weaviate client não tem método close explícito
            # mas podemos limpar a referência
            _weaviate_client = None
            logger.info("🔒 Cliente Weaviate fechado")
        except Exception as e:
            logger.error(f"❌ Erro ao fechar cliente Weaviate: {e}")

def test_weaviate_connection() -> dict:
    """
    Testa ligação ao Weaviate e retorna informações de estado
    
    Returns:
        dict: Informações sobre o estado da ligação
    """
    try:
        client = get_weaviate_client()
        
        # Testar ligação básica
        is_ready = client.is_ready()
        
        # Obter metadados se possível
        meta_info = {}
        if is_ready:
            try:
                meta_info = client.get_meta()
            except Exception as e:
                logger.warning(f"⚠️ Não foi possível obter metadados: {e}")
        
        return {
            "status": "connected" if is_ready else "disconnected",
            "url": os.getenv("WEAVIATE_URL", "http://localhost:8080"),
            "ready": is_ready,
            "meta": meta_info,
            "timestamp": client._connection.get_current_time() if hasattr(client, '_connection') else None
        }
        
    except Exception as e:
        logger.error(f"❌ Erro no teste de ligação Weaviate: {e}")
        return {
            "status": "error",
            "error": str(e),
            "url": os.getenv("WEAVIATE_URL", "http://localhost:8080")
        }
