#!/usr/bin/env python3
"""
Script simples para testar a classe VectorMemory
"""

from backend_app.core.memory import VectorMemory

def main():
    print("🧪 Testando VectorMemory com memórias de exemplo...")
    vector_memory = None
    
    try:
        # Instanciar a classe VectorMemory
        print("1. Inicializando VectorMemory...")
        vector_memory = VectorMemory()
        print("✅ VectorMemory inicializado!")
        
        # Adicionar três memórias de exemplo
        print("\n2. Adicionando memórias de exemplo...")
        memories = [
            "Lembrete: comprar pão",
            "Ideia: A app Ethic Companion pode ter notificações por push",
            "Facto: A reunião de projeto é amanhã às 10h"
        ]
        
        for memory in memories:
            vector_memory.add_memory(memory)
        
        print("✅ Memórias adicionadas com sucesso!")
        
        # Fazer pesquisa
        print("\n3. Pesquisando por 'o que tenho de fazer amanhã?'...")
        query = "o que tenho de fazer amanhã?"
        results = vector_memory.search_memory(query, limit=3)
        
        print(f"\n🔍 Resultados da pesquisa para: '{query}'")
        if results:
            for i, result in enumerate(results, 1):
                print(f"   {i}. {result}")
        else:
            print("   Nenhum resultado encontrado.")
        
        print("\n🎉 Teste concluído com sucesso!")
        
    except Exception as e:
        print(f"❌ Erro durante o teste: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Fechar conexão
        if vector_memory:
            print("\n🔒 Fechando conexão...")
            vector_memory.close()
            print("✅ Conexão fechada!")

if __name__ == "__main__":
    main() 