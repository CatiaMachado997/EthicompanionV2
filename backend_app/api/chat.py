from fastapi import APIRouter, HTTPException, UploadFile, File
from pydantic import BaseModel
from langchain.prompts import PromptTemplate
from langchain.tools import Tool
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_tavily import TavilySearch
from langchain_core.runnables import RunnableBranch, RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

from backend_app.core.memory import VectorMemory
from backend_app.core.memory_manager import MemoryManager
from backend_app.core.config import get_api_key
import os
import logging
from datetime import datetime
import openai
import uuid
from typing import BinaryIO, Union

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
    session_id: str = None  # Optional session ID, will generate if not provided

class AppResponse(BaseModel):
    reply: str
    session_id: str = None  # Return session ID to frontend

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

# Speech-to-text function using OpenAI Whisper API
async def speech_to_text(audio_file: Union[BinaryIO, bytes]) -> str:
    """
    Convert audio file to text using OpenAI Whisper API.
    
    Args:
        audio_file: Audio file stream or bytes to transcribe
        
    Returns:
        str: Transcribed text from the audio
        
    Raises:
        HTTPException: If API key is not configured or transcription fails
    """
    try:
        # Get OpenAI API key from environment
        try:
            openai_api_key = get_api_key('OPENAI_API_KEY')
            print(f"🔑 OpenAI API Key configurada: {openai_api_key[:20] if openai_api_key else 'NÃO'}")
        except ValueError as e:
            print(f"⚠️  OpenAI API Key não configurada: {e}")
            raise HTTPException(
                status_code=500, 
                detail="OpenAI API key não configurada. Configure OPENAI_API_KEY nas variáveis de ambiente."
            )
        
        # Initialize OpenAI client
        client = openai.AsyncOpenAI(api_key=openai_api_key)
        print("✅ OpenAI client inicializado")
        
        # Prepare the audio file for transcription
        if isinstance(audio_file, bytes):
            # If audio_file is bytes, we need to create a file-like object
            import io
            audio_file = io.BytesIO(audio_file)
            audio_file.name = "audio.wav"  # Whisper needs a filename
        
        print("🎤 Enviando arquivo de áudio para transcrição...")
        
        # Send audio to Whisper API for transcription
        transcript = await client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            language="pt"  # Portuguese - adjust as needed
        )
        
        transcribed_text = transcript.text
        print(f"✅ Transcrição concluída: {len(transcribed_text)} caracteres")
        print(f"📝 Texto transcrito: {transcribed_text[:100]}...")
        
        return transcribed_text
        
    except openai.AuthenticationError:
        error_msg = "Erro de autenticação OpenAI: Verifique se a API key está correta"
        print(f"❌ {error_msg}")
        raise HTTPException(status_code=401, detail=error_msg)
        
    except openai.RateLimitError:
        error_msg = "Limite de taxa da API OpenAI excedido. Tente novamente em alguns minutos"
        print(f"❌ {error_msg}")
        raise HTTPException(status_code=429, detail=error_msg)
        
    except openai.APIError as e:
        error_msg = f"Erro da API OpenAI: {str(e)}"
        print(f"❌ {error_msg}")
        raise HTTPException(status_code=500, detail=error_msg)
        
    except Exception as e:
        error_msg = f"Erro inesperado na transcrição de áudio: {str(e)}"
        print(f"❌ {error_msg}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=error_msg)

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

# Função para obter o router LLM (lazy initialization)
def get_router_llm():
    """Get or create the router LLM instance"""
    global router_llm
    if router_llm is None:
        try:
            google_key = get_api_key('GOOGLE_API_KEY')
            router_llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0)
            print("✅ Router LLM inicializado com sucesso")
        except Exception as e:
            print(f"❌ Erro ao inicializar router LLM: {e}")
            return None
    return router_llm

router_llm = None  # Will be initialized when needed
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

# Função para obter o router chain (lazy initialization)
def get_router_chain():
    """Get or create the router chain"""
    llm = get_router_llm()
    if llm:
        return router_prompt | llm | StrOutputParser()
    return None

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

# Função para obter a cadeia completa (lazy initialization)
def get_full_chain():
    """Get or create the full chain"""
    router_chain = get_router_chain()
    if router_chain:
        return {
            "classification": router_chain, 
            "question": RunnablePassthrough()
        } | full_branch
    return None

# --- 4. Endpoints da API ---

# Speech-to-text endpoint with file upload
@router.post("/speech-to-text")
async def transcribe_audio(audio_file: UploadFile = File(...)):
    """
    Endpoint POST /speech-to-text para transcrever áudio em texto
    
    Args:
        audio_file: Arquivo de áudio enviado via upload
        
    Returns:
        dict: Dicionário com o texto transcrito
    """
    try:
        print(f"🎤 Endpoint /speech-to-text chamado com arquivo: {audio_file.filename}")
        print(f"📄 Tipo de conteúdo: {audio_file.content_type}")
        
        # Validate file type
        allowed_types = [
            "audio/wav", "audio/mp3", "audio/mpeg", "audio/mp4", 
            "audio/webm", "audio/ogg", "audio/flac", "audio/m4a"
        ]
        
        if audio_file.content_type and audio_file.content_type not in allowed_types:
            raise HTTPException(
                status_code=400, 
                detail=f"Tipo de arquivo não suportado: {audio_file.content_type}. "
                       f"Tipos permitidos: {', '.join(allowed_types)}"
            )
        
        # Read file content
        audio_content = await audio_file.read()
        print(f"📊 Tamanho do arquivo: {len(audio_content)} bytes")
        
        # Create a file-like object with proper filename
        import io
        audio_stream = io.BytesIO(audio_content)
        audio_stream.name = audio_file.filename or "audio.wav"
        
        # Transcribe audio
        transcribed_text = await speech_to_text(audio_stream)
        
        return {
            "text": transcribed_text,
            "filename": audio_file.filename,
            "content_type": audio_file.content_type,
            "size_bytes": len(audio_content)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Erro no endpoint de transcrição: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Erro interno do servidor")

# Voice chat endpoint - combines speech-to-text with chat
@router.post("/voice-chat", response_model=AppResponse)
async def handle_voice_chat(audio_file: UploadFile = File(...)):
    """
    Endpoint POST /voice-chat que transcreve áudio e processa através do chat
    
    Args:
        audio_file: Arquivo de áudio enviado via upload
        
    Returns:
        AppResponse: Resposta do chat baseada no áudio transcrito
    """
    try:
        print(f"🎙️ Endpoint /voice-chat chamado com arquivo: {audio_file.filename}")
        
        # First, transcribe the audio
        audio_content = await audio_file.read()
        
        import io
        audio_stream = io.BytesIO(audio_content)
        audio_stream.name = audio_file.filename or "audio.wav"
        
        # Transcribe speech to text
        transcribed_text = await speech_to_text(audio_stream)
        print(f"🎤➡️📝 Texto transcrito: {transcribed_text}")
        
        # Process the transcribed text through the chat system
        user_input = UserInput(text=transcribed_text)
        chat_response = await handle_chat(user_input)
        
        return chat_response
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Erro no endpoint de voice chat: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Erro interno do servidor")

@router.post("/chat", response_model=AppResponse)
async def handle_chat(user_input: UserInput):
    """
    Enhanced /chat endpoint with MemoryManager integration
    
    Flow:
    1. Generate or use provided session_id
    2. Retrieve context from MemoryManager (recent + semantic)
    3. Process message through LangChain agent with context
    4. Save successful conversation to MemoryManager
    5. Return response with session_id
    """
    print(f"� Enhanced /chat endpoint called with: {user_input.text}")
    
    # Generate session_id if not provided
    session_id = user_input.session_id or str(uuid.uuid4())
    print(f"📝 Session ID: {session_id}")
    
    memory_manager = None
    try:
        # 1. Initialize MemoryManager
        memory_manager = MemoryManager()
        print("✅ MemoryManager initialized")
        
        # 2. Get context from both memory systems
        context = await memory_manager.get_context(
            session_id=session_id,
            query=user_input.text,
            recent_message_count=5,
            semantic_search_results=3
        )
        print(f"🧠 Context retrieved: {len(context)} characters")
        
        # 3. Process message with context through LangChain agent
        response = await process_with_context(user_input.text, context)
        print(f"🤖 Agent response generated: {len(response)} characters")
        
        # 4. Save successful conversation to memory
        if not is_failed_response(response):
            success = memory_manager.add_message(
                session_id=session_id,
                user_message=user_input.text,
                assistant_message=response
            )
            if success:
                print("💾 Conversation saved to both PostgreSQL and Weaviate")
            else:
                print("⚠️ Conversation save partially failed but continuing")
        else:
            # Log failed responses but don't store in memory
            log_failed_response(user_input.text, response, "FAILED_AGENT_RESPONSE")
            print("🚫 Failed response logged, not stored in memory")
        
        # 5. Return response with session_id
        return AppResponse(reply=response, session_id=session_id)
        
    except Exception as e:
        print(f"❌ Error in enhanced chat endpoint: {e}")
        import traceback
        traceback.print_exc()
        
        error_message = "Desculpe, ocorreu um erro ao processar sua solicitação. Tente novamente."
        log_failed_response(user_input.text, str(e), "ENDPOINT_ERROR")
        
        # Fallback to simple LLM response
        try:
            from backend_app.core.llm import get_llm_response
            response = get_llm_response(user_input.text)
            
            # Don't save fallback responses to memory
            if is_failed_response(response):
                log_failed_response(user_input.text, response, "LLM_FALLBACK_FAILED")
            
            return AppResponse(reply=response, session_id=session_id)
            
        except Exception as llm_error:
            print(f"❌ LLM fallback also failed: {llm_error}")
            log_failed_response(user_input.text, str(llm_error), "LLM_ERROR")
            return AppResponse(reply=error_message, session_id=session_id)
    
    finally:
        # Clean up MemoryManager connections
        if memory_manager:
            try:
                memory_manager.close()
            except Exception as e:
                print(f"❌ Error closing MemoryManager: {e}")

async def process_with_context(user_message: str, context: str) -> str:
    """
    Process user message with context through the LangChain routing system
    
    Args:
        user_message: The user's input
        context: Combined context from MemoryManager
        
    Returns:
        str: Agent's response
    """
    try:
        # Enhanced prompt that includes context
        contextual_message = f"""
        Context from previous conversations:
        {context}
        
        Current user message: {user_message}
        
        Please provide a helpful response considering both the current message and the conversation context.
        """
        
        # Try to use the full chain with routing
        full_chain = get_full_chain()
        if full_chain:
            print("🔄 Using intelligent routing with context...")
            try:
                response = await full_chain.ainvoke({"question": contextual_message})
                print("✅ Routing with context successful")
                return response
            except Exception as router_error:
                print(f"❌ Router with context failed: {router_error}")
                # Fallback to web search with context
                return await execute_web_search(contextual_message)
        else:
            # Direct web search with context
            print("🔄 Using direct web search with context...")
            return await execute_web_search(contextual_message)
            
    except Exception as e:
        print(f"❌ Error processing with context: {e}")
        # Final fallback without context
        return await execute_web_search(user_message)