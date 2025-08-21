#!/usr/bin/env python3
"""
Verificar variáveis de ambiente
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def check_env():
    print("🔍 Verificando variáveis de ambiente...")
    
    # Verificar WEAVIATE_API_KEY
    weaviate_key = os.getenv('WEAVIATE_API_KEY')
    print(f"WEAVIATE_API_KEY: {'✅ Definida' if weaviate_key else '❌ Não definida'}")
    if weaviate_key:
        print(f"   Valor: {weaviate_key[:10]}...")
    
    # Verificar GOOGLE_API_KEY
    google_key = os.getenv('GOOGLE_API_KEY')
    print(f"GOOGLE_API_KEY: {'✅ Definida' if google_key else '❌ Não definida'}")
    if google_key:
        print(f"   Valor: {google_key[:10]}...")
    
    # Verificar TAVILY_API_KEY
    tavily_key = os.getenv('TAVILY_API_KEY')
    print(f"TAVILY_API_KEY: {'✅ Definida' if tavily_key else '❌ Não definida'}")
    if tavily_key:
        print(f"   Valor: {tavily_key[:10]}...")
    
    print("\n🧪 Testando importações...")
    
    try:
        from backend_app.core.memory import VectorMemory
        print("✅ VectorMemory importado com sucesso")
    except Exception as e:
        print(f"❌ Erro ao importar VectorMemory: {e}")
    
    try:
        from backend_app.core.llm import get_llm_response
        print("✅ get_llm_response importado com sucesso")
    except Exception as e:
        print(f"❌ Erro ao importar get_llm_response: {e}")

if __name__ == "__main__":
    check_env() 