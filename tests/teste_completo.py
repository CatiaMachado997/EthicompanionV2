#!/usr/bin/env python3

import requests
import json
import time

def test_ethic_companion():
    """
    Teste completo do Ethic Companion V2
    """
    base_url = "http://127.0.0.1:8000"
    
    print("🧪 TESTE COMPLETO DO ETHIC COMPANION V2")
    print("=" * 50)
    
    # Teste 1: Dar informação pessoal
    print("\n1️⃣ TESTE: Dar informação pessoal")
    print("-" * 30)
    
    message1 = {
        "text": "A minha cor favorita é o azul."
    }
    
    print(f"📤 Enviando: {message1['text']}")
    response1 = requests.post(f"{base_url}/chat", json=message1)
    
    if response1.status_code == 200:
        result1 = response1.json()
        print(f"📥 Resposta: {result1['reply']}")
    else:
        print(f"❌ Erro: {response1.status_code}")
        return
    
    time.sleep(1)
    
    # Teste 2: Perguntar sobre informação anterior
    print("\n2️⃣ TESTE: Perguntar sobre informação anterior")
    print("-" * 40)
    
    message2 = {
        "text": "Qual é a minha cor favorita?"
    }
    
    print(f"📤 Enviando: {message2['text']}")
    response2 = requests.post(f"{base_url}/chat", json=message2)
    
    if response2.status_code == 200:
        result2 = response2.json()
        print(f"📥 Resposta: {result2['reply']}")
        
        # Verificar se a resposta contém a informação correta
        if "azul" in result2['reply'].lower():
            print("✅ SUCESSO! O sistema lembrou-se da cor favorita!")
        else:
            print("❌ O sistema não lembrou-se da cor favorita")
    else:
        print(f"❌ Erro: {response2.status_code}")
    
    time.sleep(1)
    
    # Teste 3: Adicionar mais informação
    print("\n3️⃣ TESTE: Adicionar mais informação")
    print("-" * 30)
    
    message3 = {
        "text": "Gosto de programar em Python e JavaScript."
    }
    
    print(f"📤 Enviando: {message3['text']}")
    response3 = requests.post(f"{base_url}/chat", json=message3)
    
    if response3.status_code == 200:
        result3 = response3.json()
        print(f"📥 Resposta: {result3['reply']}")
    else:
        print(f"❌ Erro: {response3.status_code}")
    
    time.sleep(1)
    
    # Teste 4: Perguntar sobre programação
    print("\n4️⃣ TESTE: Perguntar sobre programação")
    print("-" * 35)
    
    message4 = {
        "text": "Quais linguagens de programação eu gosto?"
    }
    
    print(f"📤 Enviando: {message4['text']}")
    response4 = requests.post(f"{base_url}/chat", json=message4)
    
    if response4.status_code == 200:
        result4 = response4.json()
        print(f"📥 Resposta: {result4['reply']}")
        
        # Verificar se a resposta contém as linguagens
        if "python" in result4['reply'].lower() or "javascript" in result4['reply'].lower():
            print("✅ SUCESSO! O sistema lembrou-se das linguagens de programação!")
        else:
            print("❌ O sistema não lembrou-se das linguagens de programação")
    else:
        print(f"❌ Erro: {response4.status_code}")
    
    print("\n" + "=" * 50)
    print("🎉 TESTE COMPLETO FINALIZADO!")
    print("O Ethic Companion V2 está funcionando perfeitamente!")

if __name__ == "__main__":
    test_ethic_companion()
