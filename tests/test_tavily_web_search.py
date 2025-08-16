#!/usr/bin/env python3
"""
Teste específico para verificar se a Tavily API está funcionando
"""

import os
from dotenv import load_dotenv
from langchain_tavily import TavilySearch

def test_tavily_search():
    """Testa a funcionalidade de pesquisa da Tavily"""
    print("🔍 Testando Tavily Web Search...")
    
    # Carrega variáveis de ambiente
    load_dotenv()
    
    # Verifica se a API key está configurada
    tavily_key = os.getenv('TAVILY_API_KEY')
    if not tavily_key or tavily_key == 'your_tavily_api_key_here':
        print("❌ TAVILY_API_KEY não configurada!")
        return False
    
    print(f"✅ TAVILY_API_KEY configurada: {tavily_key[:20]}...")
    
    try:
        # Cria o objeto de pesquisa
        search_tool = TavilySearch(max_results=3)
        print("✅ Objeto TavilySearch criado com sucesso")
        
        # Testa uma pesquisa simples
        query = "OpenAI latest news"
        print(f"🔎 Testando pesquisa: '{query}'")
        
        results = search_tool.invoke(query)
        print(f"✅ Pesquisa realizada com sucesso!")
        
        # Debug: mostra a estrutura dos resultados
        print(f"📊 Tipo de resultado: {type(results)}")
        print(f"📊 Conteúdo do resultado: {results}")
        
        # Verifica se há resultados
        if results:
            print(f"📊 Resultados encontrados!")
            
            # Se for uma lista
            if isinstance(results, list) and len(results) > 0:
                first_result = results[0]
                print(f"\n📰 Primeiro resultado:")
                print(f"   Título: {first_result.get('title', 'N/A')}")
                print(f"   URL: {first_result.get('url', 'N/A')}")
                print(f"   Conteúdo: {first_result.get('content', 'N/A')[:200]}...")
            # Se for um dicionário
            elif isinstance(results, dict):
                print(f"\n📰 Resultado em formato de dicionário:")
                for key, value in results.items():
                    if key == 'content' and isinstance(value, str):
                        print(f"   {key}: {value[:200]}...")
                    else:
                        print(f"   {key}: {value}")
            else:
                print(f"⚠️  Formato de resultado inesperado: {type(results)}")
        else:
            print("⚠️  Nenhum resultado encontrado")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao testar Tavily: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Função principal"""
    print("🚀 Teste da Tavily API para Web Search")
    print("=" * 50)
    
    success = test_tavily_search()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 Tavily Web Search está funcionando perfeitamente!")
        print("✅ O sistema agora pode fazer pesquisas na web!")
    else:
        print("❌ Tavily Web Search não está funcionando")
        print("🔧 Verifique a configuração da API key")

if __name__ == "__main__":
    main()
