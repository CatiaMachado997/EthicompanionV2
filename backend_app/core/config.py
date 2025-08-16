"""
Configuração de carregamento de API keys para o Ethic Companion V2.
Suporta tanto desenvolvimento local (.env) quanto produção (Google Secret Manager).
"""

import os
from dotenv import load_dotenv
import logging

# Import Secret Manager apenas quando necessário
try:
    from google.cloud import secretmanager
    SECRETMANAGER_AVAILABLE = True
except ImportError:
    SECRETMANAGER_AVAILABLE = False
    secretmanager = None

# Setup logging
logger = logging.getLogger(__name__)

def load_api_keys():
    """
    Carrega as chaves de API do Secret Manager (em produção)
    ou de um ficheiro .env (em desenvolvimento).
    
    A função detecta automaticamente o ambiente:
    - Se K_SERVICE existe -> Google Cloud Run (produção)
    - Caso contrário -> Desenvolvimento local
    """
    try:
        if os.getenv("K_SERVICE"):  
            # Estamos na cloud, vamos buscar ao Secret Manager
            logger.info("🌐 Ambiente Cloud Run detectado - carregando do Secret Manager")
            _load_from_secret_manager()
        else:
            # Estamos a correr localmente, vamos buscar ao .env
            logger.info("🏠 Ambiente local detectado - carregando do ficheiro .env")
            _load_from_env_file()
            
    except Exception as e:
        logger.error(f"❌ Erro ao carregar API keys: {e}")
        raise

def _load_from_secret_manager():
    """
    Carrega as API keys do Google Secret Manager.
    """
    if not SECRETMANAGER_AVAILABLE:
        raise ImportError("Google Cloud Secret Manager não está disponível. Execute: pip install google-cloud-secret-manager")
    
    try:
        client = secretmanager.SecretManagerServiceClient()
        project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
        
        if not project_id:
            raise ValueError("GOOGLE_CLOUD_PROJECT environment variable não encontrada")

        # Mapeamento dos nomes dos segredos
        secrets_to_fetch = {
            "GOOGLE_API_KEY": f"projects/{project_id}/secrets/ethic-companion-google-api-key/versions/latest",
            "TAVILY_API_KEY": f"projects/{project_id}/secrets/ethic-companion-tavily-api-key/versions/latest", 
            "WEAVIATE_API_KEY": f"projects/{project_id}/secrets/ethic-companion-weaviate-api-key/versions/latest",
            "OPENAI_API_KEY": f"projects/{project_id}/secrets/ethic-companion-openai-api-key/versions/latest",
        }

        # Buscar cada segredo
        for key, secret_path in secrets_to_fetch.items():
            try:
                response = client.access_secret_version(request={"name": secret_path})
                secret_value = response.payload.data.decode("UTF-8")
                os.environ[key] = secret_value
                logger.info(f"✅ {key} carregada do Secret Manager")
            except Exception as e:
                logger.warning(f"⚠️  Erro ao carregar {key}: {e}")
                # Continuar com outras chaves mesmo se uma falhar
                
        logger.info("✅ Chaves de API carregadas do Secret Manager")
        
    except Exception as e:
        logger.error(f"❌ Erro ao conectar com Secret Manager: {e}")
        raise

def _load_from_env_file():
    """
    Carrega as API keys do ficheiro .env local.
    """
    try:
        # Carregar variáveis do .env
        load_dotenv()
        
        # Verificar se as chaves necessárias estão presentes
        required_keys = ["GOOGLE_API_KEY", "TAVILY_API_KEY", "WEAVIATE_API_KEY"]
        missing_keys = []
        
        for key in required_keys:
            value = os.getenv(key)
            if not value or value == f"your_{key.lower()}_here":
                missing_keys.append(key)
            else:
                logger.info(f"✅ {key} carregada do .env")
        
        if missing_keys:
            logger.warning(f"⚠️  Chaves em falta ou não configuradas: {missing_keys}")
            logger.warning("📝 Verifique o seu ficheiro .env")
        
        logger.info("✅ Chaves de API carregadas do ficheiro .env local")
        
    except Exception as e:
        logger.error(f"❌ Erro ao carregar ficheiro .env: {e}")
        raise

def get_api_key(key_name: str) -> str:
    """
    Obtém uma API key específica do ambiente.
    
    Args:
        key_name: Nome da chave (ex: 'GOOGLE_API_KEY')
        
    Returns:
        Valor da API key
        
    Raises:
        ValueError: Se a chave não estiver configurada
    """
    value = os.getenv(key_name)
    if not value or value == f"your_{key_name.lower()}_here":
        raise ValueError(f"API key {key_name} não está configurada")
    return value

def validate_api_keys() -> dict:
    """
    Valida se todas as API keys necessárias estão configuradas.
    
    Returns:
        Dict com status de cada chave
    """
    required_keys = ["GOOGLE_API_KEY", "TAVILY_API_KEY", "WEAVIATE_API_KEY", "OPENAI_API_KEY"]
    status = {}
    
    for key in required_keys:
        try:
            value = get_api_key(key)
            status[key] = "✅ Configurada"
        except ValueError:
            status[key] = "❌ Não configurada"
    
    return status

# Configuração adicional para Weaviate
def get_weaviate_config() -> dict:
    """
    Retorna configuração do Weaviate baseada no ambiente.
    """
    if os.getenv("K_SERVICE"):
        # Produção - usar URL do Cloud Run ou serviço externo
        return {
            "host": os.getenv("WEAVIATE_HOST", "localhost"),
            "port": int(os.getenv("WEAVIATE_PORT", "8080")),
            "scheme": "https" if os.getenv("WEAVIATE_HTTPS", "false").lower() == "true" else "http",
            "api_key": get_api_key("WEAVIATE_API_KEY")
        }
    else:
        # Desenvolvimento local
        return {
            "host": os.getenv("WEAVIATE_HOST", "localhost"),
            "port": int(os.getenv("WEAVIATE_PORT", "8080")),
            "scheme": "http",
            "api_key": None  # Sem autenticação no desenvolvimento
        }
