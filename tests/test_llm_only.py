#!/usr/bin/env python3
"""
Teste apenas do LLM sem memória
"""

from app.core.llm import get_llm_response

def test_llm_only():
    print("🧪 Testando apenas o LLM...")
    
    try:
        prompt = "Olá! Como vais?"
        print(f"📝 Prompt: {prompt}")
        print("⏳ Aguardando resposta...")
        
        response = get_llm_response(prompt)
        
        print(f"✅ Resposta: {response}")
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_llm_only() 