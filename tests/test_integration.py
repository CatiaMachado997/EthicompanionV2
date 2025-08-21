#!/usr/bin/env python3
"""
Teste da integração completa (memória + LLM)
"""

from app.core.memory import VectorMemory
from app.core.llm import get_llm_response

def test_integration():
    print("🧪 Testando integração completa...")
    vector_memory = None
    
    try:
        # Simular o que o endpoint faz
        print("1. Instanciando VectorMemory...")
        vector_memory = VectorMemory()
        
        user_input = "Olá! Como vais?"
        print(f"2. Pergunta do usuário: {user_input}")
        
        # Procurar na memória por contexto relevante
        print("3. Procurando na memória...")
        relevant_memories = vector_memory.search_memory(user_input, limit=3)
        print(f"   Encontrados {len(relevant_memories)} contextos relevantes")
        
        # Construir o prompt final com contexto
        context_section = ""
        if relevant_memories:
            context_section = "Contexto Relevante:\n"
            for i, memory in enumerate(relevant_memories, 1):
                context_section += f"{i}. {memory}\n"
            context_section += "\n"
        
        prompt_final = f"""{context_section}Nova Pergunta:
{user_input}

Por favor, responde de forma útil e contextualizada, considerando o contexto relevante se disponível."""
        
        print(f"4. Prompt final:\n{prompt_final}")
        
        # Obter resposta do LLM
        print("5. Obtendo resposta do LLM...")
        llm_response = get_llm_response(prompt_final)
        print(f"   Resposta: {llm_response}")
        
        # Guardar a nova interação na memória
        print("6. Guardando interação na memória...")
        interaction_text = f"Pergunta: {user_input} | Resposta: {llm_response}"
        vector_memory.add_memory(interaction_text)
        print("   ✅ Interação guardada!")
        
        print("\n🎉 Integração completa funcionando!")
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        if vector_memory:
            print("\n🔒 Fechando conexão...")
            vector_memory.close()

if __name__ == "__main__":
    test_integration() 