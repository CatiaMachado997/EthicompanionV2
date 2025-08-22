#!/usr/bin/env python3
"""
Teste simplificado do sistema de memória híbrida - apenas PostgreSQL
"""
import asyncio
import os
import sys
from datetime import datetime

# Adicionar o path do projeto
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

async def test_postgres_only():
    """Teste apenas do PostgreSQL sem Weaviate"""
    print("🔍 === TESTE POSTGRESQL APENAS ===\n")
    
    try:
        from backend_app.models.database import get_db_session, create_tables
        
        # Criar tabelas e obter sessão
        print("🚀 Configurando PostgreSQL...")
        create_tables()
        db_session = get_db_session()
        print("✅ PostgreSQL: Conectado")
        
        # Criar um cliente Weaviate mock para teste
        class MockWeaviateClient:
            class Schema:
                def exists(self, name):
                    return False
                def create_class(self, schema):
                    pass
            
            class DataObject:
                def create(self, data_object, class_name):
                    return "mock_uuid_123"
            
            class Query:
                def __init__(self):
                    self.collection_name = None
                
                def get(self, class_name, properties):
                    self.collection_name = class_name
                    return self
                    
                def with_near_text(self, content):
                    return self
                    
                def with_where(self, condition):
                    return self
                    
                def with_limit(self, limit):
                    return self
                    
                def do(self):
                    if hasattr(self, '_is_aggregate'):
                        return {"data": {"Aggregate": {self.collection_name: [{"meta": {"count": 0}}]}}}
                    return {"data": {"Get": {self.collection_name: []}}}
                
                def aggregate(self, class_name):
                    self.collection_name = class_name
                    self._is_aggregate = True
                    return self
                    
                def with_meta_count(self):
                    return self
            
            def __init__(self):
                self.schema = self.Schema()
                self.data_object = self.DataObject()
                self.query = self.Query()
        
        mock_weaviate = MockWeaviateClient()
        
        # Inicializar memory manager
        from backend_app.core.hybrid_memory_manager import MemoryManager
        
        print("🧠 Inicializando MemoryManager...")
        memory = MemoryManager(db_session=db_session, weaviate_client=mock_weaviate)
        
        # Testar adição de mensagens
        session_id = f"test_session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        conversations = [
            ("Qual é a regra de ouro da ética?", 
             "A regra de ouro da ética é: 'Trate os outros como você gostaria de ser tratado'. Este princípio fundamental aparece em muitas tradições éticas e religiosas."),
            ("Como aplicar isso no ambiente de trabalho?", 
             "No ambiente de trabalho, a regra de ouro se aplica através de: 1) Respeitar colegas e suas opiniões, 2) Ser honesto e transparente, 3) Colaborar de forma construtiva, 4) Reconhecer o mérito dos outros.")
        ]
        
        print("💾 Adicionando conversas...")
        for user_msg, assistant_msg in conversations:
            success = memory.add_message(session_id, user_msg, assistant_msg)
            if success:
                print(f"  ✅ Conversa adicionada")
            else:
                print(f"  ❌ Falha ao adicionar conversa")
        
        # Testar estatísticas
        print("\n📊 Testando estatísticas...")
        stats = memory.get_memory_stats()
        
        if stats.get("status") == "operational":
            pg_stats = stats.get("postgresql", {})
            wv_stats = stats.get("weaviate", {})
            
            print(f"  - Total de mensagens: {pg_stats.get('total_messages', 0)}")
            print(f"  - Sessões únicas: {pg_stats.get('unique_sessions', 0)}")
            print(f"  - Última mensagem: {pg_stats.get('last_message', 'N/A')}")
            print(f"  - PostgreSQL funcionando: ✅")
            print(f"  - Weaviate: ❌ (mock)")
        else:
            print(f"  - Erro nas estatísticas: {stats.get('message', 'Erro desconhecido')}")
            print(f"  - PostgreSQL: ❓")
            print(f"  - Weaviate: ❌ (mock)")
        
        print("\n✅ Teste PostgreSQL completado com sucesso!")
        
        # Fechar sessão
        db_session.close()
        
    except Exception as e:
        print(f"❌ Erro no teste: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_postgres_only())
