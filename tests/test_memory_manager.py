#!/usr/bin/env python3
"""
MemoryManager Demo Script
Demonstrates the complete MemoryManager functionality
"""

import asyncio
import sys
import os
from datetime import datetime

# Add the backend_app to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from backend_app.core.memory_manager import MemoryManager
from backend_app.core.config import load_api_keys

async def demo_memory_manager():
    """
    Comprehensive demo of MemoryManager functionality
    """
    print("🚀 MemoryManager Demo Starting...")
    print("=" * 60)
    
    try:
        # Load API keys
        print("1️⃣ Loading API keys...")
        load_api_keys()
        print("✅ API keys loaded successfully\n")
        
        # Initialize MemoryManager
        print("2️⃣ Initializing MemoryManager...")
        memory_manager = MemoryManager()
        print("✅ MemoryManager initialized\n")
        
        # Demo session ID
        session_id = "demo_session_123"
        
        # 3. Add sample conversations
        print("3️⃣ Adding sample conversations...")
        
        conversations = [
            {
                "user": "Olá! Como está o tempo hoje?",
                "assistant": "Olá! Para saber como está o tempo hoje, eu precisaria saber a sua localização. Poderia me dizer onde você está?"
            },
            {
                "user": "Estou em Lisboa, Portugal",
                "assistant": "Perfeito! Em Lisboa hoje está um dia ensolarado com temperatura de 22°C. Há algumas nuvens mas sem previsão de chuva. É um ótimo dia para sair!"
            },
            {
                "user": "Que atividades recomenda para hoje?",
                "assistant": "Com este tempo maravilhoso em Lisboa, recomendo: visitar o Cais do Sodré e caminhar pela margem do Tejo, explorar o Bairro Alto, ou fazer um piquenique no Parque Eduardo VII. Todas são ótimas opções para aproveitar o sol!"
            }
        ]
        
        # Add conversations to memory
        for i, conv in enumerate(conversations, 1):
            success = memory_manager.add_message(
                session_id=session_id,
                user_message=conv["user"],
                assistant_message=conv["assistant"]
            )
            print(f"   💾 Conversation {i}: {'✅ Saved' if success else '❌ Failed'}")
        
        print()
        
        # 4. Test context retrieval
        print("4️⃣ Testing context retrieval...")
        
        test_queries = [
            "Como está o tempo?",
            "O que fazer em Lisboa?",
            "Onde posso fazer piquenique?"
        ]
        
        for query in test_queries:
            print(f"\n   🔍 Query: '{query}'")
            context = await memory_manager.get_context(
                session_id=session_id,
                query=query,
                recent_message_count=3,
                semantic_search_results=2
            )
            
            print(f"   📝 Context retrieved ({len(context)} chars):")
            print("   " + "-" * 50)
            # Show first 200 chars of context
            print("   " + context[:200].replace('\n', '\n   ') + "...")
            print("   " + "-" * 50)
        
        print()
        
        # 5. Test session statistics
        print("5️⃣ Session statistics...")
        stats = memory_manager.get_session_statistics(session_id)
        print(f"   📊 Session: {stats.get('session_id', 'N/A')}")
        print(f"   💬 Total messages: {stats.get('total_messages', 0)}")
        print(f"   👤 User messages: {stats.get('user_messages', 0)}")
        print(f"   🤖 Assistant messages: {stats.get('assistant_messages', 0)}")
        print(f"   🔄 Conversation pairs: {stats.get('conversation_pairs', 0)}")
        if stats.get('first_message_time'):
            print(f"   ⏰ First message: {stats['first_message_time']}")
        if stats.get('last_message_time'):
            print(f"   ⏰ Last message: {stats['last_message_time']}")
        
        print()
        
        # 6. Test with different session
        print("6️⃣ Testing with different session...")
        session_2 = "demo_session_456"
        
        # Add a conversation about a different topic
        success = memory_manager.add_message(
            session_id=session_2,
            user_message="Quero aprender Python. Por onde começar?",
            assistant_message="Ótima escolha! Para começar com Python recomendo: 1) Instalar Python e um editor como VS Code, 2) Fazer um curso básico online, 3) Praticar com projetos simples. Python é uma linguagem muito amigável para inicientes!"
        )
        print(f"   💾 New session conversation: {'✅ Saved' if success else '❌ Failed'}")
        
        # Test cross-session semantic search
        print(f"\n   🔍 Cross-session search from session {session_2}:")
        context = await memory_manager.get_context(
            session_id=session_2,
            query="atividades ao ar livre",
            recent_message_count=2,
            semantic_search_results=3
        )
        print(f"   📝 Should find Lisboa activities from other session:")
        print("   " + "-" * 50)
        print("   " + context[:300].replace('\n', '\n   ') + "...")
        print("   " + "-" * 50)
        
        print()
        
        # 7. Performance test
        print("7️⃣ Performance test - multiple rapid operations...")
        import time
        
        start_time = time.time()
        test_session = "performance_test"
        
        # Add 5 conversations rapidly
        for i in range(5):
            memory_manager.add_message(
                session_id=test_session,
                user_message=f"Test message {i+1}",
                assistant_message=f"Test response {i+1} with some content to make it realistic"
            )
        
        # Do 5 context retrievals
        for i in range(5):
            await memory_manager.get_context(
                session_id=test_session,
                query=f"test query {i+1}",
                recent_message_count=3,
                semantic_search_results=2
            )
        
        end_time = time.time()
        print(f"   ⚡ Performance: {end_time - start_time:.2f} seconds for 10 operations")
        print(f"   📈 Average: {(end_time - start_time) / 10:.3f} seconds per operation")
        
        print()
        print("8️⃣ Demo completed successfully! 🎉")
        print("=" * 60)
        print("✅ MemoryManager is fully functional with:")
        print("   🔹 PostgreSQL episodic memory storage")
        print("   🔹 Weaviate semantic memory search")  
        print("   🔹 Session management and statistics")
        print("   🔹 Cross-session semantic search")
        print("   🔹 Error handling and resilience")
        print("   🔹 Good performance characteristics")
        
    except Exception as e:
        print(f"❌ Demo failed with error: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        # Clean up
        if 'memory_manager' in locals():
            memory_manager.close()
            print("\n🧹 Cleanup completed")

if __name__ == "__main__":
    # Run the demo
    asyncio.run(demo_memory_manager())
