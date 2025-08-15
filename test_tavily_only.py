#!/usr/bin/env python3
"""
Teste apenas da ferramenta Tavily sem LLM
"""

import os
from langchain_community.tools.tavily_search import TavilySearchResults

def test_tavily_only():
    print("🧪 Testando apenas Tavily Search...")
    
    # Configurar API key
    os.environ['TAVILY_API_KEY'] = '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'
    
    try:
        # Criar a ferramenta de pesquisa
        search_tool = TavilySearchResults(max_results=3)
        
        # Testar várias pesquisas
        queries = [
            "presidente Portugal 2024",
            "capital França",
            "população Lisboa",
            "tempo atual Lisboa"
        ]
        
        for query in queries:
            print(f"\n🔍 Pesquisando: {query}")
            result = search_tool.run(query)
            print(f"✅ Resultado: {result[:200]}...")
            
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_tavily_only()
