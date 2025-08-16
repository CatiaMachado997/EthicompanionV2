#!/usr/bin/env python3
"""
Teste da ferramenta de pesquisa Tavily
"""

import os
from langchain_community.tools.tavily_search import TavilySearchResults

def test_tavily():
    print("🧪 Testando Tavily Search...")
    
    # Configurar temporariamente
    os.environ['TAVILY_API_KEY'] = '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'
    
    try:
        # Criar a ferramenta de pesquisa
        search_tool = TavilySearchResults(max_results=3)
        
        # Testar pesquisa
        query = "presidente Portugal 2024"
        print(f"🔍 Pesquisando: {query}")
        
        result = search_tool.run(query)
        print(f"✅ Resultado: {result}")
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_tavily()
