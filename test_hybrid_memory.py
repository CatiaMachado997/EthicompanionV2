"""
Teste Completo do Sistema de Memória Híbrida
Demonstra como usar o MemoryManager com PostgreSQL + Weaviate
"""

import asyncio
import logging
import sys
import os
from datetime import datetime

# Adicionar o diretório backend ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend_app.core.hybrid_memory_manager import MemoryManager
from backend_app.core.weaviate_client import get_weaviate_client, test_weaviate_connection
from backend_app.core.ai_agent import get_ai_agent
from backend_app.models.database import get_db_session, create_tables

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def test_hybrid_memory_system():
    """Teste completo do sistema de memória híbrida"""
    
    print("🧠 === TESTE DO SISTEMA DE MEMÓRIA HÍBRIDA ===")
    print()
    
    # 1. TESTAR LIGAÇÕES
    print("1️⃣ **Testando Ligações...**")
    
    # Testar Weaviate
    try:
        weaviate_status = test_weaviate_connection()
        if weaviate_status["status"] == "connected":
            print("✅ Weaviate: Conectado")
            weaviate_client = get_weaviate_client()
        else:
            print(f"❌ Weaviate: {weaviate_status['error']}")
            return
    except Exception as e:
        print(f"❌ Erro Weaviate: {e}")
        return
    
    # Testar PostgreSQL
    try:
        create_tables()  # Criar tabelas se não existirem
        db_session = get_db_session()
        print("✅ PostgreSQL: Conectado")
    except Exception as e:
        print(f"❌ Erro PostgreSQL: {e}")
        return
    
    # Testar Agente AI
    try:
        ai_agent = get_ai_agent()
        agent_status = ai_agent.get_agent_status()
        print(f"✅ Agente AI: {agent_status['status']} ({agent_status['llm_type']})")
    except Exception as e:
        print(f"❌ Erro Agente AI: {e}")
        ai_agent = None
    
    print()
    
    # 2. INICIALIZAR MEMORY MANAGER
    print("2️⃣ **Inicializando MemoryManager...**")
    try:
        memory_manager = MemoryManager(
            db_session=db_session,
            weaviate_client=weaviate_client
        )
        print("✅ MemoryManager inicializado")
    except Exception as e:
        print(f"❌ Erro ao inicializar MemoryManager: {e}")
        return
    
    print()
    
    # 3. TESTAR CICLO COMPLETO DE CONVERSA
    print("3️⃣ **Testando Ciclo Completo de Conversa...**")
    
    session_id = f"test_session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    print(f"Sessão de teste: {session_id}")
    print()
    
    # Conversas de teste
    test_conversations = [
        {
            "user": "Olá! Estou a enfrentar um dilema ético no trabalho. Como devo abordar uma situação onde vejo um colega a fazer algo incorreto?",
            "expected_context": "primeira_conversa"
        },
        {
            "user": "O que significa exatamente 'fazer a coisa certa' numa situação como esta?",
            "expected_context": "segunda_conversa"  
        },
        {
            "user": "Podes dar-me alguns passos práticos para lidar com isto?",
            "expected_context": "terceira_conversa"
        }
    ]
    
    for i, conv in enumerate(test_conversations, 1):
        print(f"**Conversa {i}:**")
        user_message = conv["user"]
        print(f"🙋 **Utilizador:** {user_message}")
        
        # 3a. Recuperar contexto
        try:
            context = await memory_manager.get_context(
                session_id=session_id,
                query=user_message
            )
            print(f"🧠 **Contexto recuperado:** {len(context)} caracteres")
        except Exception as e:
            print(f"❌ Erro ao recuperar contexto: {e}")
            context = ""
        
        # 3b. Processar com agente AI (se disponível)
        if ai_agent:
            try:
                # Construir prompt com contexto
                enhanced_prompt = f"""CONTEXTO DE MEMÓRIA:
{context}

---

MENSAGEM ATUAL:
{user_message}"""

                ai_response = await ai_agent.process_message(
                    message=enhanced_prompt,
                    session_id=session_id
                )
                assistant_message = ai_response["response"]
                print(f"🤖 **Assistente:** {assistant_message[:200]}{'...' if len(assistant_message) > 200 else ''}")
                
            except Exception as e:
                print(f"❌ Erro no agente AI: {e}")
                assistant_message = f"Obrigado pela tua pergunta sobre ética. Esta é uma área complexa que requer reflexão cuidadosa sobre valores e consequências."
        else:
            assistant_message = f"Resposta simulada para: {user_message[:50]}..."
            print(f"🤖 **Assistente (simulado):** {assistant_message}")
        
        # 3c. Guardar na memória
        try:
            success = memory_manager.add_message(
                session_id=session_id,
                user_message=user_message,
                assistant_message=assistant_message
            )
            
            if success:
                print("✅ Conversa guardada na memória")
            else:
                print("❌ Falha ao guardar conversa")
                
        except Exception as e:
            print(f"❌ Erro ao guardar: {e}")
        
        print()
        
        # Pequena pausa entre conversas
        await asyncio.sleep(1)
    
    # 4. TESTAR RECUPERAÇÃO DE MEMÓRIA
    print("4️⃣ **Testando Recuperação de Memória...**")
    
    test_queries = [
        "dilema ético trabalho",
        "fazer a coisa certa",
        "passos práticos"
    ]
    
    for query in test_queries:
        print(f"**Query:** '{query}'")
        try:
            context = await memory_manager.get_context(
                session_id=session_id,
                query=query,
                recent_limit=3,
                semantic_limit=2
            )
            
            print(f"📄 **Contexto ({len(context)} chars):**")
            print(context[:500] + ("..." if len(context) > 500 else ""))
            print()
            
        except Exception as e:
            print(f"❌ Erro na query '{query}': {e}")
            print()
    
    # 5. ESTATÍSTICAS DO SISTEMA
    print("5️⃣ **Estatísticas do Sistema...**")
    try:
        stats = memory_manager.get_memory_stats()
        print("📊 **Estatísticas da Memória:**")
        print(f"PostgreSQL - Mensagens: {stats['postgresql']['total_messages']}")
        print(f"PostgreSQL - Sessões: {stats['postgresql']['unique_sessions']}")
        print(f"Weaviate - Vetores: {stats['weaviate']['total_vectors']}")
        print(f"Status: {stats['status']}")
    except Exception as e:
        print(f"❌ Erro ao obter estatísticas: {e}")
    
    print()
    
    # 6. LIMPEZA
    print("6️⃣ **Limpeza...**")
    try:
        memory_manager.close()
        db_session.close()
        print("✅ Recursos fechados")
    except Exception as e:
        print(f"❌ Erro na limpeza: {e}")
    
    print()
    print("🎉 **TESTE COMPLETO!**")
    print()
    print("**Próximos Passos:**")
    print("1. Integrar com frontend Next.js")
    print("2. Configurar variáveis de ambiente")
    print("3. Testar com dados reais")
    print("4. Otimizar performance")

async def test_simple_memory_operations():
    """Teste mais simples apenas das operações básicas"""
    print("🔍 === TESTE SIMPLES DAS OPERAÇÕES BÁSICAS ===")
    print()
    
    try:
        # Setup básico
        create_tables()
        db_session = get_db_session()
        
        # Teste sem Weaviate se não estiver disponível
        try:
            weaviate_client = get_weaviate_client()
            print("✅ Weaviate disponível")
        except:
            print("⚠️ Weaviate não disponível - teste limitado")
            return
        
        memory_manager = MemoryManager(db_session, weaviate_client)
        
        # Teste básico
        session_id = "simple_test"
        
        print("💾 Guardando mensagem de teste...")
        success = memory_manager.add_message(
            session_id=session_id,
            user_message="Teste de memória",
            assistant_message="Resposta de teste"
        )
        
        if success:
            print("✅ Mensagem guardada")
            
            print("🔍 Recuperando contexto...")
            context = await memory_manager.get_context(
                session_id=session_id,
                query="teste"
            )
            
            print(f"📄 Contexto: {len(context)} caracteres")
            print("✅ Teste básico completo")
        else:
            print("❌ Falha ao guardar mensagem")
        
        memory_manager.close()
        
    except Exception as e:
        print(f"❌ Erro no teste simples: {e}")

if __name__ == "__main__":
    print("Escolhe o tipo de teste:")
    print("1. Teste completo do sistema")
    print("2. Teste simples das operações básicas")
    
    choice = input("Opção (1 ou 2): ").strip()
    
    if choice == "1":
        asyncio.run(test_hybrid_memory_system())
    elif choice == "2":
        asyncio.run(test_simple_memory_operations())
    else:
        print("Opção inválida. A executar teste simples...")
        asyncio.run(test_simple_memory_operations())
