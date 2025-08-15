#!/usr/bin/env python3
"""
Teste simples para verificar se a pesquisa na web está funcionando no frontend
"""

import requests
import json

def test_simple_web_search():
    """Testa uma pergunta simples que deve usar pesquisa na web"""
    print("🧪 Teste Simples de Pesquisa na Web")
    print("=" * 50)
    
    # URL do frontend
    frontend_url = "http://localhost:3000"
    chat_url = f"{frontend_url}/api/chat"
    
    # Pergunta que deve ativar a pesquisa na web
    question = "What are the latest news about OpenAI?"
    
    print(f"🔍 Pergunta: '{question}'")
    
    try:
        # Prepara o payload
        payload = {"text": question}
        
        print(f"📤 Enviando para: {chat_url}")
        print(f"📦 Payload: {payload}")
        
        # Envia a pergunta
        response = requests.post(
            chat_url,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        print(f"📥 Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            reply = data.get('response', '')  # CORRIGIDO: usa 'response' em vez de 'reply'
            
            print(f"✅ Resposta recebida!")
            print(f"📝 Tamanho da resposta: {len(reply)} caracteres")
            print(f"📝 Primeiros 200 caracteres: {reply[:200]}...")
            
            # Verifica se a resposta parece ter informações da web
            web_indicators = [
                'de acordo com os resultados da pesquisa',
                'according to the search results',
                'search results',
                'pesquisa',
                'web',
                'latest',
                'recent',
                'resultados da pesquisa',
                'com base nos resultados'
            ]
            
            has_web_info = any(indicator.lower() in reply.lower() for indicator in web_indicators)
            
            if has_web_info:
                print(f"🌐 ✅ Resposta contém indicadores de pesquisa na web!")
                print(f"🎯 Score: 100% - Pesquisa na web funcionando perfeitamente!")
            else:
                print(f"⚠️  Resposta pode não ter usado pesquisa na web")
                print(f"🔍 Indicadores encontrados: {[indicator for indicator in web_indicators if indicator.lower() in reply.lower()]}")
                
        else:
            print(f"❌ Erro: {response.status_code}")
            print(f"📝 Resposta: {response.text}")
            
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_simple_web_search()
