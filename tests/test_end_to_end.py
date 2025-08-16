#!/usr/bin/env python3
"""
Teste end-to-end completo do Ethic Companion V2
"""

import requests
import json
import time

def test_backend_health():
    """Testa a saúde do backend"""
    print("🏥 Testando saúde do backend...")
    
    try:
        response = requests.get("http://localhost:8000/docs")
        if response.status_code == 200:
            print("✅ Backend está saudável e acessível")
            return True
        else:
            print(f"❌ Backend retornou status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erro ao conectar com backend: {e}")
        return False

def test_frontend_health():
    """Testa a saúde do frontend"""
    print("🏥 Testando saúde do frontend...")
    
    try:
        response = requests.get("http://localhost:3000")
        if response.status_code == 200:
            print("✅ Frontend está saudável e acessível")
            return True
        else:
            print(f"❌ Frontend retornou status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erro ao conectar com frontend: {e}")
        return False

def test_chat_functionality():
    """Testa a funcionalidade de chat"""
    print("\n💬 Testando funcionalidade de chat...")
    
    test_messages = [
        "Hello, how are you?",
        "What can you help me with?",
        "Tell me a joke",
        "What's the weather like?"
    ]
    
    success_count = 0
    
    for i, message in enumerate(test_messages, 1):
        print(f"\n  {i}. Enviando: '{message}'")
        
        try:
            # Testar backend diretamente
            backend_response = requests.post(
                "http://localhost:8000/chat",
                json={"text": message},
                headers={"Content-Type": "application/json"}
            )
            
            if backend_response.status_code == 200:
                backend_data = backend_response.json()
                print(f"     ✅ Backend: {backend_data.get('reply', 'No reply')[:80]}...")
                
                # Testar frontend API
                frontend_response = requests.post(
                    "http://localhost:3000/api/chat",
                    json={"text": message},
                    headers={"Content-Type": "application/json"}
                )
                
                if frontend_response.status_code == 200:
                    frontend_data = frontend_response.json()
                    print(f"     ✅ Frontend: {frontend_data.get('response', 'No response')[:80]}...")
                    success_count += 1
                else:
                    print(f"     ❌ Frontend API falhou: {frontend_response.status_code}")
                    
            else:
                print(f"     ❌ Backend falhou: {backend_response.status_code}")
                
        except Exception as e:
            print(f"     ❌ Erro: {e}")
        
        # Pequena pausa entre mensagens
        time.sleep(1)
    
    return success_count, len(test_messages)

def test_memory_functionality():
    """Testa a funcionalidade de memória"""
    print("\n🧠 Testando funcionalidade de memória...")
    
    try:
        # Adicionar uma memória de teste
        test_memory = "Teste de memória: O usuário gosta de programação Python"
        
        # Usar o backend para adicionar memória (se houver endpoint)
        print(f"  📝 Adicionando memória de teste...")
        
        # Buscar na memória
        search_query = "programação Python"
        response = requests.post(
            "http://localhost:8000/chat",
            json={"text": f"Do you remember anything about {search_query}?"},
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            reply = data.get('reply', '')
            if "memória" in reply.lower() or "conversas anteriores" in reply.lower():
                print("✅ Sistema de memória funcionando")
                return True
            else:
                print("⚠️  Sistema de memória pode não estar funcionando como esperado")
                return False
        else:
            print(f"❌ Erro ao testar memória: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao testar memória: {e}")
        return False

def main():
    print("🚀 Teste End-to-End Completo do Ethic Companion V2\n")
    
    # Testar saúde dos serviços
    backend_healthy = test_backend_health()
    frontend_healthy = test_frontend_health()
    
    if not backend_healthy or not frontend_healthy:
        print("\n❌ Serviços não estão saudáveis. Verifique se estão rodando.")
        return
    
    # Testar funcionalidade de chat
    chat_success, chat_total = test_chat_functionality()
    
    # Testar funcionalidade de memória
    memory_working = test_memory_functionality()
    
    # Resultado final
    print("\n📊 Resultado dos Testes:")
    print(f"   Backend: {'✅ Saudável' if backend_healthy else '❌ Não saudável'}")
    print(f"   Frontend: {'✅ Saudável' if frontend_healthy else '❌ Não saudável'}")
    print(f"   Chat: {chat_success}/{chat_total} mensagens processadas com sucesso")
    print(f"   Memória: {'✅ Funcionando' if memory_working else '❌ Com problemas'}")
    
    # Calcular score geral
    total_tests = 4  # backend, frontend, chat, memory
    passed_tests = sum([backend_healthy, frontend_healthy, chat_success > 0, memory_working])
    score = (passed_tests / total_tests) * 100
    
    print(f"\n🎯 Score Geral: {score:.1f}% ({passed_tests}/{total_tests})")
    
    if score >= 90:
        print("🎉 Excelente! O sistema está funcionando perfeitamente!")
    elif score >= 70:
        print("✅ Bom! O sistema está funcionando com pequenos problemas.")
    elif score >= 50:
        print("⚠️  Regular. O sistema tem alguns problemas que precisam ser resolvidos.")
    else:
        print("❌ Problemas significativos detectados. Verifique a configuração.")

if __name__ == "__main__":
    main()

