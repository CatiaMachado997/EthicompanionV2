#!/usr/bin/env python3
"""
Script para testar o endpoint de chat atualizado
"""

import requests
import json
import time

def test_chat_endpoint():
    print("🧪 Testando o endpoint de chat atualizado...")
    
    # URL do endpoint
    url = "http://127.0.0.1:8000/chat"
    
    # Teste 1: Primeira interação
    print("\n1. Teste - Primeira interação:")
    data1 = {"text": "Olá! Como vais?"}
    
    try:
        response1 = requests.post(url, json=data1)
        if response1.status_code == 200:
            result1 = response1.json()
            print(f"✅ Status: {response1.status_code}")
            print(f"📝 Pergunta: {data1['text']}")
            print(f"🤖 Resposta: {result1['reply']}")
        else:
            print(f"❌ Erro: {response1.status_code} - {response1.text}")
    except Exception as e:
        print(f"❌ Erro na requisição: {e}")
    
    # Aguardar um pouco
    time.sleep(2)
    
    # Teste 2: Segunda interação (deve usar memória)
    print("\n2. Teste - Segunda interação (com memória):")
    data2 = {"text": "Lembras-te do que acabámos de falar?"}
    
    try:
        response2 = requests.post(url, json=data2)
        if response2.status_code == 200:
            result2 = response2.json()
            print(f"✅ Status: {response2.status_code}")
            print(f"📝 Pergunta: {data2['text']}")
            print(f"🤖 Resposta: {result2['reply']}")
        else:
            print(f"❌ Erro: {response2.status_code} - {response2.text}")
    except Exception as e:
        print(f"❌ Erro na requisição: {e}")
    
    # Aguardar um pouco
    time.sleep(2)
    
    # Teste 3: Pergunta sobre contexto
    print("\n3. Teste - Pergunta sobre contexto:")
    data3 = {"text": "Qual foi a nossa conversa anterior?"}
    
    try:
        response3 = requests.post(url, json=data3)
        if response3.status_code == 200:
            result3 = response3.json()
            print(f"✅ Status: {response3.status_code}")
            print(f"📝 Pergunta: {data3['text']}")
            print(f"🤖 Resposta: {result3['reply']}")
        else:
            print(f"❌ Erro: {response3.status_code} - {response3.text}")
    except Exception as e:
        print(f"❌ Erro na requisição: {e}")
    
    print("\n🎉 Teste do endpoint concluído!")

if __name__ == "__main__":
    test_chat_endpoint() 