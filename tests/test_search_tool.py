#!/usr/bin/env python3
"""
Teste da ferramenta de pesquisa DuckDuckGo
"""

from langchain_community.tools import DuckDuckGoSearchRun

def test_search():
    print("🧪 Testando DuckDuckGo Search...")
    
    try:
        # Criar a ferramenta de pesquisa
        search_tool = DuckDuckGoSearchRun()
        
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
    test_search()
