#!/usr/bin/env python3
"""
Script de teste para a função get_llm_response
"""

from app.core.llm import get_llm_response

def test_llm():
    print("🧪 Testando a função get_llm_response...")
    
    try:
        # Teste simples
        print("1. Testando com prompt simples...")
        prompt = "Olá! Podes dizer-me qual é a capital de Portugal?"
        
        print(f"📝 Prompt: {prompt}")
        print("⏳ Aguardando resposta do Gemini...")
        
        response = get_llm_response(prompt)
        
        print(f"🤖 Resposta: {response}")
        
        # Teste com pergunta mais complexa
        print("\n2. Testando com pergunta mais complexa...")
        prompt2 = "Explica-me brevemente o que é Inteligência Artificial em 2-3 frases."
        
        print(f"📝 Prompt: {prompt2}")
        print("⏳ Aguardando resposta do Gemini...")
        
        response2 = get_llm_response(prompt2)
        
        print(f"🤖 Resposta: {response2}")
        
        print("\n🎉 Teste concluído com sucesso!")
        
    except Exception as e:
        print(f"❌ Erro durante o teste: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_llm() 