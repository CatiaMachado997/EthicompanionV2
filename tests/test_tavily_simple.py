#!/usr/bin/env python3
"""
Teste simples da Tavily com a nova importação
"""

import os
from langchain_tavily import TavilySearch

def test_tavily_simple():
    print("🧪 Testando Tavily com nova importação...")
    
        # Configurar API key - Load from environment
    from dotenv import load_dotenv
    load_dotenv()
    
    if not os.getenv('TAVILY_API_KEY'):
        print("❌ TAVILY_API_KEY não encontrada no .env")
        return
    
    try:
        # Criar a ferramenta de pesquisa
        search_tool = TavilySearch(max_results=3)
        
        # Testar pesquisa simples
        query = "presidente Portugal"
        print(f"🔍 Pesquisando: {query}")
        
        result = search_tool.run(query)
        print(f"✅ Resultado: {str(result)[:300]}...")
        
        print("🎉 Tavily funcionando perfeitamente!")
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_tavily_simple()
