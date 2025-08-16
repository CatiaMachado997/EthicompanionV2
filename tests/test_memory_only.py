#!/usr/bin/env python3
"""
Teste apenas da memória sem LLM
"""

from app.core.memory import VectorMemory

def test_memory_only():
    print("🧪 Testando apenas a memória...")
    vector_memory = None
    
    try:
        print("1. Inicializando VectorMemory...")
        vector_memory = VectorMemory()
        print("✅ VectorMemory inicializado!")
        
        print("\n2. Testando adição de memória...")
        vector_memory.add_memory("Teste: Esta é uma memória de teste")
        print("✅ Memória adicionada!")
        
        print("\n3. Testando busca de memória...")
        results = vector_memory.search_memory("teste", limit=3)
        print(f"✅ Busca concluída! Encontrados {len(results)} resultados")
        
        for i, result in enumerate(results, 1):
            print(f"   {i}. {result}")
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        if vector_memory:
            print("\n🔒 Fechando conexão...")
            vector_memory.close()
            print("✅ Conexão fechada!")

if __name__ == "__main__":
    test_memory_only() 