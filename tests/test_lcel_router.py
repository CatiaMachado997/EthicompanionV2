#!/usr/bin/env python3
"""
Teste da nova arquitetura LCEL Router
"""

import requests
import json

def test_lcel_router():
    print("🧪 Testando LCEL Router com especialistas...")
    
    # Perguntas de teste para diferentes especialistas
    test_cases = [
        {
            "question": "Quem é o presidente dos Estados Unidos?",
            "expected_expert": "web_search",
            "description": "Pergunta sobre fatos atuais"
        },
        {
            "question": "Lembras-te do que falámos antes?",
            "expected_expert": "memory_search",
            "description": "Pergunta sobre conversas anteriores"
        },
        {
            "question": "Qual é a capital de França?",
            "expected_expert": "web_search",
            "description": "Pergunta sobre conhecimento geral"
        },
        {
            "question": "Do que falámos na última vez?",
            "expected_expert": "memory_search",
            "description": "Pergunta sobre memória"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{i}. Testando: {test_case['question']}")
        print(f"   Descrição: {test_case['description']}")
        print(f"   Especialista esperado: {test_case['expected_expert']}")
        print("-" * 50)
        
        try:
            # Fazer a requisição
            response = requests.post(
                "http://localhost:8000/chat",
                headers={'Content-Type': 'application/json'},
                json={'text': test_case['question']}
            )
            
            if response.status_code == 200:
                data = response.json()
                reply = data.get('reply', 'Sem resposta')
                print(f"✅ Resposta: {reply[:200]}...")
                
                # Verificar se a resposta parece correta
                if "erro" in reply.lower():
                    print("⚠️  Resposta indica erro")
                elif "não encontrei" in reply.lower() and test_case['expected_expert'] == "memory_search":
                    print("✅ Resposta apropriada para memória vazia")
                else:
                    print("✅ Resposta parece correta")
                    
            else:
                print(f"❌ Erro HTTP: {response.status_code}")
                print(f"   Detalhes: {response.text}")
                
        except Exception as e:
            print(f"❌ Erro: {e}")
    
    print("\n🎉 Teste do LCEL Router concluído!")

if __name__ == "__main__":
    test_lcel_router()
