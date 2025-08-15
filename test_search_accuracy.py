#!/usr/bin/env python3
"""
Teste de precisão da pesquisa Tavily
"""

import os
import requests
import json
from datetime import datetime

def test_search_accuracy():
    print("🧪 Testando precisão da pesquisa Tavily...")
    
    # Configurar API key
    os.environ['TAVILY_API_KEY'] = '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'
    
    # Perguntas de teste com respostas conhecidas
    test_cases = [
        {
            "question": "Quem é o presidente dos Estados Unidos?",
            "expected_keywords": ["Joe Biden", "Biden", "presidente"],
            "search_queries": [
                "current president of the United States 2024",
                "Joe Biden president United States",
                "presidente Estados Unidos atual"
            ]
        },
        {
            "question": "Quem é o presidente de Portugal?",
            "expected_keywords": ["Marcelo", "Rebelo", "Sousa"],
            "search_queries": [
                "presidente Portugal atual",
                "Marcelo Rebelo de Sousa",
                "current president Portugal"
            ]
        }
    ]
    
    for test_case in test_cases:
        print(f"\n🔍 Testando: {test_case['question']}")
        print(f"📅 Data/Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        for i, query in enumerate(test_case['search_queries'], 1):
            print(f"\n  {i}. Query: {query}")
            
            try:
                # Fazer pesquisa via API
                response = requests.post(
                    "http://localhost:8000/chat-simple",
                    headers={'Content-Type': 'application/json'},
                    json={'text': query}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    result = data.get('reply', '')
                    
                    # Verificar se contém palavras-chave esperadas
                    found_keywords = []
                    for keyword in test_case['expected_keywords']:
                        if keyword.lower() in result.lower():
                            found_keywords.append(keyword)
                    
                    print(f"    ✅ Resultado: {result[:200]}...")
                    print(f"    🎯 Keywords encontradas: {found_keywords}")
                    
                    if found_keywords:
                        print(f"    ✅ Precisão: BOA")
                    else:
                        print(f"    ⚠️  Precisão: BAIXA - Keywords não encontradas")
                        
                else:
                    print(f"    ❌ Erro HTTP: {response.status_code}")
                    
            except Exception as e:
                print(f"    ❌ Erro: {e}")
    
    print("\n🎉 Teste de precisão concluído!")

if __name__ == "__main__":
    test_search_accuracy()
