#!/usr/bin/env python3
"""
Teste da funcionalidade de pesquisa na web através do frontend
"""

import requests
import json
import time

def test_web_search_frontend():
    """Testa a funcionalidade de pesquisa na web via frontend"""
    print("🌐 Testando Pesquisa na Web via Frontend...")
    
    # URL do frontend
    frontend_url = "http://localhost:3000"
    
    # Testa se o frontend está acessível
    try:
        response = requests.get(frontend_url, timeout=5)
        if response.status_code == 200:
            print("✅ Frontend acessível")
        else:
            print(f"⚠️  Frontend retornou status: {response.status_code}")
    except Exception as e:
        print(f"❌ Erro ao acessar frontend: {e}")
        return False
    
    # Testa a API de chat do frontend
    chat_url = f"{frontend_url}/api/chat"
    
    # Perguntas que devem ativar a pesquisa na web
    web_search_questions = [
        "What are the latest news about OpenAI?",
        "What's the current weather in São Paulo?",
        "Who won the last World Cup?",
        "What are the latest developments in AI technology?",
        "What happened in the tech world this week?"
    ]
    
    print(f"\n🔍 Testando {len(web_search_questions)} perguntas que devem ativar pesquisa na web...")
    
    for i, question in enumerate(web_search_questions, 1):
        print(f"\n{i}. Pergunta: '{question}'")
        
        try:
            # Prepara o payload - CORRIGIDO: usa 'text' em vez de 'message'
            payload = {
                "text": question
            }
            
            # Envia a pergunta
            response = requests.post(
                chat_url,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                reply = data.get('reply', '')
                
                print(f"   ✅ Status: {response.status_code}")
                print(f"   📝 Resposta: {reply[:150]}...")
                
                # Verifica se a resposta parece ter informações da web
                web_indicators = ['recent', 'latest', 'current', 'today', 'this week', 'news', 'update']
                has_web_info = any(indicator in reply.lower() for indicator in web_indicators)
                
                if has_web_info:
                    print(f"   🌐 ✅ Resposta parece conter informações da web!")
                else:
                    print(f"   ⚠️  Resposta pode não ter usado pesquisa na web")
                
            else:
                print(f"   ❌ Status: {response.status_code}")
                print(f"   📝 Erro: {response.text[:100]}...")
                
        except Exception as e:
            print(f"   ❌ Erro: {e}")
        
        # Pausa entre as perguntas para não sobrecarregar
        time.sleep(2)
    
    return True

def test_specific_web_search():
    """Testa uma pesquisa específica que deve usar a Tavily"""
    print("\n🎯 Teste Específico de Pesquisa na Web...")
    
    chat_url = "http://localhost:3000/api/chat"
    
    # Pergunta específica que deve ativar a pesquisa
    question = "What are the top 3 AI companies in 2024 and what are they working on?"
    
    print(f"🔍 Pergunta: '{question}'")
    
    try:
        # CORRIGIDO: usa 'text' em vez de 'message'
        payload = {
            "text": question
        }
        
        response = requests.post(
            chat_url,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            reply = data.get('reply', '')
            
            print(f"✅ Status: {response.status_code}")
            print(f"📝 Resposta completa:")
            print(f"{'='*50}")
            print(reply)
            print(f"{'='*50}")
            
            # Análise da resposta
            if len(reply) > 200:
                print(f"📊 Resposta detalhada ({len(reply)} caracteres) - ✅ Provavelmente usou pesquisa na web")
            else:
                print(f"📊 Resposta curta ({len(reply)} caracteres) - ⚠️  Pode não ter usado pesquisa na web")
                
        else:
            print(f"❌ Status: {response.status_code}")
            print(f"📝 Erro: {response.text}")
            
    except Exception as e:
        print(f"❌ Erro: {e}")

def main():
    """Função principal"""
    print("🚀 Teste de Pesquisa na Web via Frontend")
    print("=" * 60)
    
    # Teste geral
    test_web_search_frontend()
    
    # Teste específico
    test_specific_web_search()
    
    print("\n" + "=" * 60)
    print("🎯 Teste de Pesquisa na Web Concluído!")
    print("💡 Dica: Verifique se as respostas contêm informações atualizadas da web")

if __name__ == "__main__":
    main()
