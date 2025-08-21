#!/usr/bin/env python3

import os
from app.core.memory import VectorMemory

# Configurar variáveis de ambiente
os.environ['WEAVIATE_API_KEY'] = 'minha-chave-secreta-dev'

def test_memory():
    print("🔍 Testando memória...")
    
    # Instanciar VectorMemory
    vector_memory = VectorMemory()
    
    # Adicionar uma memória de teste
    test_memory = "Pergunta: A minha cor favorita é o azul. | Resposta: Entendi, a sua cor favorita é o azul!"
    print(f"➕ Adicionando memória: {test_memory}")
    vector_memory.add_memory(test_memory)
    
    # Buscar memórias relacionadas
    query = "Qual é a minha cor favorita?"
    print(f"🔎 Buscando por: '{query}'")
    
    results = vector_memory.search_memory(query, limit=5)
    print(f"📋 Resultados encontrados: {len(results)}")
    
    for i, result in enumerate(results, 1):
        print(f"  {i}. {result}")
    
    # Fechar conexão
    vector_memory.close()
    
    return results

if __name__ == "__main__":
    test_memory()
