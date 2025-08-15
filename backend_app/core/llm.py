import os
from backend_app.core.config import get_api_key
from langchain_google_genai import ChatGoogleGenerativeAI

def get_llm_response(prompt: str, model: str = "gemini-1.5-flash") -> str:
    """
    Get a response from the Google Generative AI model
    
    Args:
        prompt: The input prompt
        model: The model to use (default: gemini-1.5-flash)
    
    Returns:
        The model's response as a string
    """
    try:
        # Get API key using the new config system
        api_key = get_api_key('GOOGLE_API_KEY')
        
        # Initialize the LLM
        llm = ChatGoogleGenerativeAI(
            model=model,
            google_api_key=api_key,
            temperature=0.7
        )
        
        # Get response
        response = llm.invoke(prompt)
        return response.content
        
    except Exception as e:
        return f"Erro ao obter resposta do LLM: {str(e)}"
