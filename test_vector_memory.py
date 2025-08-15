#!/usr/bin/env python3
"""
Script de teste para a classe VectorMemory
"""

from app.core.memory import VectorMemory

def test_vector_memory():
    print("🧪 Testando a classe VectorMemory...")
    vector_memory = None
    
    try:
        # Inicializar o VectorMemory
        print("1. Inicializando VectorMemory...")
        vector_memory = VectorMemory()
        print("✅ VectorMemory inicializado com sucesso!")
        
        # Testar adição de memórias
        print("\n2. Testando adição de memórias...")
        test_texts = [
            "O Python é uma linguagem de programação muito popular",
            "FastAPI é um framework web moderno para Python",
            "Weaviate é uma base de dados vetorial open-source",
            "Machine Learning é uma área da Inteligência Artificial",
            "Docker é uma plataforma para containerização"
        ]
        
        for text in test_texts:
            vector_memory.add_memory(text)
        
        # Testar pesquisa de memórias
        print("\n3. Testando pesquisa de memórias...")
        
        # Pesquisa por "Python"
        print("\n   Pesquisando por 'Python':")
        results = vector_memory.search_memory("Python", limit=3)
        for i, result in enumerate(results, 1):
            print(f"   {i}. {result}")
        
        # Pesquisa por "web"
        print("\n   Pesquisando por 'web':")
        results = vector_memory.search_memory("web", limit=2)
        for i, result in enumerate(results, 1):
            print(f"   {i}. {result}")
        
        # Pesquisa por "dados"
        print("\n   Pesquisando por 'dados':")
        results = vector_memory.search_memory("dados", limit=2)
        for i, result in enumerate(results, 1):
            print(f"   {i}. {result}")
        
        print("\n🎉 Todos os testes passaram com sucesso!")
        
    except Exception as e:
        print(f"❌ Erro durante o teste: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Sempre fechar a conexão
        if vector_memory:
            print("\n🔒 Fechando conexão com Weaviate...")
            vector_memory.close()
            print("✅ Conexão fechada!")

if __name__ == "__main__":
    test_vector_memory() 