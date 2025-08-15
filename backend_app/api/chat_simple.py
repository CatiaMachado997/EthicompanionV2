from fastapi import APIRouter
from pydantic import BaseModel
from langchain_community.tools import TavilySearchResults
import os

# Modelos Pydantic
class UserInput(BaseModel):
    text: str

class AppResponse(BaseModel):
    reply: str

router = APIRouter()

@router.post("/chat-simple", response_model=AppResponse)
async def chat_simple_endpoint(user_input: UserInput):
    """
    Endpoint POST /chat-simple que usa apenas Tavily Search (sem LLM)
    """
    try:
        # Configurar API key
        os.environ['TAVILY_API_KEY'] = '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'
        
        # Criar a ferramenta de pesquisa
        search_tool = TavilySearchResults(max_results=3)
        
        # Fazer a pesquisa
        result = search_tool.run(user_input.text)
        
        # Formatar a resposta
        if result and 'results' in result and result['results']:
            # Pegar o primeiro resultado
            first_result = result['results'][0]
            reply = f"Encontrei esta informação: {first_result.get('title', 'Sem título')}\n\n{first_result.get('content', 'Sem conteúdo')[:500]}..."
        else:
            reply = "Desculpe, não consegui encontrar informações sobre isso."
        
        return AppResponse(reply=reply)

    except Exception as e:
        print(f"Erro no endpoint /chat-simple: {e}")
        error_message = "Desculpe, ocorreu um erro ao processar sua solicitação. Tente novamente."
        return AppResponse(reply=error_message)
