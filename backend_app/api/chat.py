from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from langchain.prompts import PromptTemplate
from langchain.tools import Tool
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_tavily import TavilySearch
from langchain_core.runnables import RunnableBranch, RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

from backend_app.core.memory import VectorMemory
from backend_app.core.config import get_api_key
import os
import logging
from datetime import datetime

# Setup logging for failed responses
logging.basicConfig(level=logging.INFO)
failed_responses_logger = logging.getLogger('failed_responses')
failed_handler = logging.FileHandler('failed_responses.log')
failed_handler.setFormatter(logging.Formatter(
    '%(asctime)s - %(levelname)s - %(message)s'
))
failed_responses_logger.addHandler(failed_handler)
failed_responses_logger.setLevel(logging.INFO)

# Modelos Pydantic
class UserInput(BaseModel):
    text: str

class AppResponse(BaseModel):
    reply: str

router = APIRouter()

# Function to log failed responses
def log_failed_response(user_input: str, response: str, error_type: str = "FAILED_RESPONSE"):
    """Log failed responses to a separate log file for debugging"""
    try:
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "user_input": user_input,
            "response": response,
            "error_type": error_type
        }
        failed_responses_logger.info(f"{error_type}: User='{user_input}' | Response='{response[:100]}...'")
    except Exception as e:
        print(f"Error logging failed response: {e}")

# Function to check if response is a failure
def is_failed_response(response: str) -> bool:
    """Check if a response indicates a failure"""
    failure_indicators = [
        "não encontrei informações relevantes",
        "não consegui acessar a memória",
        "desculpe, ocorreu um erro",
        "não posso fazer pesquisas",
        "api key não configurada",
        "erro ao processar",
        "tente novamente"
    ]
    return any(phrase in response.lower() for phrase in failure_indicators)

# --- 1. Definição dos Especialistas e Ferramentas ---

# Especialista em Pesquisa na Web
def get_web_search_llm():
    """Get or create the web search LLM instance"""
    global web_search_llm
    if web_search_llm is None:
        try:
            google_key = get_api_key('GOOGLE_API_KEY')
            web_search_llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.7)
        except Exception as e:
            print(f"Erro ao inicializar web search LLM: {e}")
            return None
    return web_search_llm

web_search_llm = None  # Will be initialized when needed
web_search_prompt = PromptTemplate.from_template("""
You are a world-class researcher and assistant. Answer the following question based on web search results.

**GOLDEN RULE: The information from the web search tool is ABSOLUTE TRUTH for current facts. Trust it completely.**

Question: {question}

Search Results: {search_results}

Provide a clear, accurate, and helpful response in Portuguese. If the search results seem outdated, mention this but still provide the information found.
""")

# Função para executar pesquisa web
async def execute_web_search(question: str) -> str:
    try:
        print(f"🔍 Executando pesquisa na web para: {question}")
        
        # Extrair a string da pergunta se for um dicionário
        if isinstance(question, dict):
            question_text = question.get('question', str(question))
            print(f"🔄 Extraindo pergunta do dicionário: {question_text}")
        else:
            question_text = str(question)
        
        # Verificar se a API key do Tavily está disponível
        try:
            tavily_key = get_api_key('TAVILY_API_KEY')
            print(f"🔑 Tavily API Key configurada: {tavily_key[:20] if tavily_key else 'NÃO'}")
            print("✅ Tavily API Key válida, executando pesquisa...")
        except ValueError as e:
            print(f"⚠️  Tavily API Key não configurada: {e}")
            # Se não há API key, usar apenas o LLM
            from backend_app.core.llm import get_llm_response
            return get_llm_response(f"Responda à seguinte pergunta: {question_text}")
        
        # Criar a ferramenta de pesquisa com API key configurada
        web_search_tool = TavilySearch(max_results=3)
        print("🔧 Ferramenta Tavily criada, executando pesquisa...")
        
        # Usar o campo 'query' que a Tavily espera
        search_results = web_search_tool.invoke({"query": question_text})
        print(f"📊 Resultados da pesquisa recebidos: {type(search_results)}")
        print(f"📊 Conteúdo dos resultados: {search_results}")
        
        # Formatar os resultados para o prompt
        formatted_results = ""
        if search_results and 'results' in search_results:
            print(f"📝 Formatando {len(search_results['results'])} resultados...")
            for i, result in enumerate(search_results['results'][:3], 1):
                formatted_results += f"\n{i}. {result.get('title', 'Sem título')}\n"
                formatted_results += f"   {result.get('content', 'Sem conteúdo')[:300]}...\n"
        else:
            print("⚠️  Nenhum resultado encontrado ou formato inesperado")
        
        print(f"📝 Resultados formatados: {formatted_results[:200]}...")
        
        # Executar o LLM com os resultados
        llm_instance = get_web_search_llm()
        if llm_instance is None:
            print("❌ LLM não disponível para processar resultados")
            return "Desculpe, não posso fazer pesquisas na web no momento. Por favor, verifique a configuração das API keys."
        
        print("🤖 LLM disponível, processando resultados...")
        response = await llm_instance.ainvoke(
            web_search_prompt.format(question=question_text, search_results=formatted_results)
        )
        print(f"✅ Resposta do LLM gerada: {len(response.content)} caracteres")
        return response.content
        
    except Exception as e:
        print(f"❌ Erro na pesquisa web: {e}")
        import traceback
        traceback.print_exc()
        # Se falhar, usar apenas o LLM
        print("🔄 Usando fallback para LLM apenas...")
        from backend_app.core.llm import get_llm_response
        return get_llm_response(f"Responda à seguinte pergunta: {question_text if 'question_text' in locals() else question}")

# Especialista em Memória
async def execute_memory_search(question: str) -> str:
    try:
        print(f"🧠 Executando busca na memória para: {question}")
        
        # Extrair a string da pergunta se for um dicionário
        if isinstance(question, dict):
            question_text = question.get('question', str(question))
            print(f"🔄 Extraindo pergunta do dicionário: {question_text}")
        else:
            question_text = str(question)
        
        # Criar o gerenciador de memória
        memory_manager = VectorMemory()
        print("✅ VectorMemory instance created")
        
        # Buscar na memória
        memory_results = memory_manager.search_memory(question_text, limit=3)
        print(f"📊 Memory search results: {memory_results}")
        print(f"📊 Number of results: {len(memory_results) if memory_results else 0}")
        
        if memory_results:
            memory_text = "\n".join(memory_results)
            result = f"Com base nas nossas conversas anteriores, encontrei esta informação:\n\n{memory_text}"
            print(f"✅ Returning memory-based response: {result[:100]}...")
            return result
        else:
            result = "Não encontrei informações relevantes nas nossas conversas anteriores. Posso ajudar-te com uma pesquisa na web?"
            print(f"⚠️  No memory results found, returning: {result}")
            return result
    except Exception as e:
        print(f"❌ Erro na busca de memória: {e}")
        import traceback
        traceback.print_exc()
        return "Não consegui acessar a memória. Posso ajudar-te com uma pesquisa na web?"

# --- 2. Definição do Router ---

# Inicializar o router LLM apenas se a API key estiver disponível
router_llm = None
try:
    google_key = get_api_key('GOOGLE_API_KEY')
    router_llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0)
except Exception as e:
    print(f"Erro ao inicializar router LLM: {e}")
    router_llm = None
router_prompt_template = """Given the user question, classify it as either `web_search` or `memory_search`.

`web_search` is for questions about:
- Current events, facts, news
- People (presidents, celebrities, politicians)
- Places, dates, information that changes over time
- General knowledge questions

`memory_search` is for questions about:
- Past conversations with the user
- User preferences or personal information
- "Do you remember..." type questions
- Previous discussions

Respond with ONLY one word: either "web_search" or "memory_search"

Question: {question}
Classification:"""
router_prompt = PromptTemplate.from_template(router_prompt_template)

# Criar o router chain apenas se o LLM estiver disponível
if router_llm:
    router_chain = router_prompt | router_llm | StrOutputParser()
else:
    router_chain = None

# --- 3. Lógica de Roteamento ---

# Função para executar web search
async def web_search_expert(input_dict):
    print(f"🌐 WEB SEARCH EXPERT called with: {input_dict}")
    return await execute_web_search(input_dict["question"])

# Função para executar memory search
async def memory_search_expert(input_dict):
    print(f"🧠 MEMORY SEARCH EXPERT called with: {input_dict}")
    return await execute_memory_search(input_dict["question"])

# Função para verificar se é web_search
def is_web_search(input_dict):
    result = "web_search" in input_dict["classification"].lower()
    print(f"🔍 is_web_search check: classification='{input_dict['classification']}', result={result}")
    return result

# Função para verificar se é memory_search
def is_memory_search(input_dict):
    result = "memory_search" in input_dict["classification"].lower()
    print(f"🧠 is_memory_search check: classification='{input_dict['classification']}', result={result}")
    return result

# Criar a bifurcação
full_branch = RunnableBranch(
    (is_web_search, web_search_expert),
    (is_memory_search, memory_search_expert),
    lambda x: f"Desculpe, não consegui classificar a pergunta '{x['question']}'. Pode reformular?"
)

# A cadeia completa (apenas se o router estiver disponível)
if router_chain:
    full_chain = {
        "classification": router_chain, 
        "question": RunnablePassthrough()
    } | full_branch
else:
    full_chain = None

# --- 4. Endpoint da API Atualizado ---

@router.post("/chat", response_model=AppResponse)
async def handle_chat(user_input: UserInput):
    """
    Endpoint POST /chat com roteamento inteligente
    """
    print(f"🚀 Endpoint /chat chamado com: {user_input.text}")
    memory_manager = None
    try:
        # Se o router chain estiver disponível, usar roteamento inteligente
        if full_chain:
            print("🔄 Router chain disponível, usando roteamento inteligente...")
            try:
                # First, let's test the classification directly
                if router_chain:
                    classification = await router_chain.ainvoke({"question": user_input.text})
                    print(f"🏷️  Classification result: '{classification.strip()}'")
                
                response = await full_chain.ainvoke({"question": user_input.text})
                print(f"✅ Router funcionou, resposta: {response[:100]}...")
            except Exception as router_error:
                print(f"❌ Erro no router, usando fallback: {router_error}")
                import traceback
                traceback.print_exc()
                response = await execute_web_search(user_input.text)
        else:
            # Fallback para web search simples
            print("🔄 Router chain não disponível, usando web search direto...")
            response = await execute_web_search(user_input.text)
        
        print(f"📝 Resposta final gerada: {len(response)} caracteres")
        
        # Check if this is a failed response
        if is_failed_response(response):
            # Log failed responses to file, don't store in memory
            log_failed_response(user_input.text, response, "MEMORY_SEARCH_FAILED")
            print(f"🚫 Failed response logged to file, not stored in memory")
        else:
            # Store successful interactions in memory
            try:
                memory_manager = VectorMemory()
                full_interaction = f"User: {user_input.text}\nAssistant: {response}"
                memory_manager.add_memory(full_interaction)
                print(f"💾 Successful interaction stored in memory")
            except Exception as memory_error:
                print(f"Erro ao conectar com memória (opcional): {memory_error}")
                log_failed_response(user_input.text, response, "MEMORY_STORAGE_ERROR")
                # Continue sem memória se houver erro
        
        return AppResponse(reply=response)
        
    except Exception as e:
        print(f"Erro no endpoint /chat: {e}")
        error_message = "Desculpe, ocorreu um erro ao processar sua solicitação. Tente novamente."
        
        # Log the error
        log_failed_response(user_input.text, str(e), "ENDPOINT_ERROR")
        
        # Se falhar, usar apenas o LLM diretamente
        try:
            from backend_app.core.llm import get_llm_response
            response = get_llm_response(user_input.text)
            
            # Check if the fallback response is also a failure
            if is_failed_response(response):
                log_failed_response(user_input.text, response, "LLM_FALLBACK_FAILED")
            
            return AppResponse(reply=response)
        except Exception as llm_error:
            print(f"Erro no LLM: {llm_error}")
            log_failed_response(user_input.text, str(llm_error), "LLM_ERROR")
            return AppResponse(reply=error_message)
    
    finally:
        # Garantir que a conexão com Weaviate seja fechada
        if memory_manager:
            try:
                memory_manager.close()
            except Exception as e:
                print(f"Erro ao fechar conexão Weaviate: {e}")