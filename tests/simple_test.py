#!/usr/bin/env python3
"""
Teste simples do endpoint de chat
"""

import requests

def test_simple():
    print("🧪 Teste simples do endpoint...")
    
    url = "http://127.0.0.1:8000/chat"
    data = {"text": "Olá! Como vais?"}
    
    try:
        print("📡 Enviando requisição...")
        response = requests.post(url, json=data, timeout=30)
        
        print(f"📊 Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Sucesso!")
            print(f"🤖 Resposta: {result['reply']}")
        else:
            print(f"❌ Erro: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Erro: Não foi possível conectar ao servidor")
    except requests.exceptions.Timeout:
        print("❌ Erro: Timeout na requisição")
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    test_simple() 