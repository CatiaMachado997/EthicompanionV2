#!/usr/bin/env python3
"""
Teste do AgentExecutor completo com LLM
"""

import os
import requests
import json

def test_full_agent():
    print("🧪 Testando AgentExecutor completo com LLM...")
    
    # Verificar se a Google API Key está configurada
    google_api_key = os.getenv('GOOGLE_API_KEY')
    if not google_api_key or google_api_key == "your-google-api-key-here":
        print("❌ Google API Key não configurada ou inválida!")
        print("🔑 Por favor, configura a GOOGLE_API_KEY com uma chave válida")
        return
    
    # URL do endpoint completo
    url = "http://localhost:8000/chat"
    
    # Perguntas de teste que devem usar diferentes ferramentas
    test_questions = [
        "Olá! Como vais?",
        "Quem é o presidente de Portugal?",
        "Lembras-te do que falámos antes?",
        "Qual é a capital de França?",
        "Conta-me uma piada"
    ]
    
    for i, question in enumerate(test_questions, 1):
        print(f"\n{i}. Testando: {question}")
        
        try:
            # Fazer a requisição
            response = requests.post(
                url,
                headers={'Content-Type': 'application/json'},
                json={'text': question}
            )
            
            if response.status_code == 200:
                data = response.json()
                reply = data.get('reply', 'Sem resposta')
                print(f"✅ Resposta: {reply[:300]}...")
            else:
                print(f"❌ Erro HTTP: {response.status_code}")
                print(f"   Detalhes: {response.text}")
                
        except Exception as e:
            print(f"❌ Erro: {e}")
    
    print("\n🎉 Teste do AgentExecutor completo concluído!")

if __name__ == "__main__":
    test_full_agent()
