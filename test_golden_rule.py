#!/usr/bin/env python3
"""
Teste da Regra de Ouro - verificar se o agente confia na ferramenta de pesquisa
"""

import requests
import json

def test_golden_rule():
    print("🧪 Testando a Regra de Ouro...")
    
    # Perguntas que devem ativar a Regra de Ouro
    test_questions = [
        "Quem é o presidente dos Estados Unidos?",
        "Quem é o presidente de Portugal?",
        "Qual é a capital de França?",
        "Quem é o primeiro-ministro do Reino Unido?"
    ]
    
    for i, question in enumerate(test_questions, 1):
        print(f"\n{i}. Testando: {question}")
        print("=" * 50)
        
        try:
            # Fazer a requisição
            response = requests.post(
                "http://localhost:8000/chat",
                headers={'Content-Type': 'application/json'},
                json={'text': question}
            )
            
            if response.status_code == 200:
                data = response.json()
                reply = data.get('reply', 'Sem resposta')
                print(f"✅ Resposta: {reply}")
                
                # Verificar se a resposta parece confiar na ferramenta
                if "desculpe" in reply.lower() or "não consegui" in reply.lower():
                    print("⚠️  Resposta indica que não confiou na ferramenta")
                else:
                    print("✅ Resposta parece confiar na ferramenta (Regra de Ouro ativa)")
                    
            else:
                print(f"❌ Erro HTTP: {response.status_code}")
                print(f"   Detalhes: {response.text}")
                
        except Exception as e:
            print(f"❌ Erro: {e}")
    
    print("\n🎉 Teste da Regra de Ouro concluído!")

if __name__ == "__main__":
    test_golden_rule()
