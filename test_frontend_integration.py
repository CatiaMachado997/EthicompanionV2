#!/usr/bin/env python3
"""
Teste de integração entre frontend e backend
"""

import requests
import json

def test_backend_direct():
    """Testa o backend diretamente"""
    print("🧪 Testando backend diretamente...")
    
    try:
        response = requests.post(
            "http://localhost:8000/chat",
            json={"text": "Hello, can you help me?"},
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Backend funcionando: {data.get('reply', 'No reply')[:100]}...")
            return True
        else:
            print(f"❌ Backend retornou status {response.status_code}: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao conectar com backend: {e}")
        return False

def test_frontend_api():
    """Testa a API do frontend"""
    print("\n🧪 Testando API do frontend...")
    
    try:
        response = requests.post(
            "http://localhost:3000/api/chat",
            json={"text": "Hello, can you help me?"},
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Frontend API funcionando: {data.get('response', 'No response')[:100]}...")
            return True
        else:
            print(f"❌ Frontend API retornou status {response.status_code}: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao conectar com frontend API: {e}")
        return False

def main():
    print("🚀 Teste de Integração Frontend-Backend\n")
    
    # Testar backend
    backend_ok = test_backend_direct()
    
    # Testar frontend API
    frontend_ok = test_frontend_api()
    
    # Resultado final
    print("\n📊 Resultado dos Testes:")
    print(f"   Backend: {'✅ OK' if backend_ok else '❌ FALHOU'}")
    print(f"   Frontend API: {'✅ OK' if frontend_ok else '❌ FALHOU'}")
    
    if backend_ok and frontend_ok:
        print("\n🎉 Integração funcionando perfeitamente!")
    elif backend_ok and not frontend_ok:
        print("\n⚠️  Backend OK, mas frontend API com problemas")
    elif not backend_ok and frontend_ok:
        print("\n⚠️  Frontend API OK, mas backend com problemas")
    else:
        print("\n❌ Ambos com problemas")

if __name__ == "__main__":
    main()
