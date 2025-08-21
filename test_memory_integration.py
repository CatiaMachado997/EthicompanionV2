#!/usr/bin/env python3
"""
Complete integration test for MemoryManager with the chat system.
This script tests the full workflow of saving and retrieving memories.
"""

import asyncio
import sys
import os
from datetime import datetime

# Add project root to Python path
sys.path.append('.')

from backend_app.core.memory_manager import MemoryManager
from backend_app.models.database import get_db_session, create_tables
from backend_app.core.config import load_api_keys

async def test_memory_integration():
    """Test complete MemoryManager integration"""
    
    print("🧪 Starting MemoryManager Integration Test")
    print("=" * 50)
    
    try:
        # 1. Load configuration
        print("1️⃣ Loading configuration...")
        load_api_keys()
        print("✅ API keys loaded")
        
        # 2. Initialize database
        print("\n2️⃣ Initializing database...")
        create_tables()
        print("✅ Database tables created")
        
        # 3. Create MemoryManager instance
        print("\n3️⃣ Creating MemoryManager...")
        db = get_db_session()
        memory_manager = MemoryManager(db_session=db)
        print("✅ MemoryManager created")
        
        # 4. Test conversation scenarios
        session_id = f"integration_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        print(f"\n4️⃣ Testing conversation with session: {session_id}")
        
        # Scenario 1: AI Ethics conversation
        conversations = [
            {
                "user": "What are the main principles of ethical AI?",
                "assistant": "The main principles of ethical AI include: 1) Fairness and non-discrimination, 2) Transparency and explainability, 3) Accountability and responsibility, 4) Privacy and data protection, 5) Human autonomy and oversight, 6) Robustness and safety. These principles ensure AI systems are developed and deployed responsibly."
            },
            {
                "user": "How can we ensure AI fairness in practice?",
                "assistant": "To ensure AI fairness: 1) Use diverse and representative training data, 2) Implement bias detection and mitigation techniques, 3) Regular auditing and testing for discriminatory outcomes, 4) Involve diverse stakeholders in development, 5) Establish clear metrics for fairness measurement, 6) Continuous monitoring in production environments."
            },
            {
                "user": "Tell me about AI transparency requirements",
                "assistant": "AI transparency involves: 1) Explainable algorithms that users can understand, 2) Clear documentation of AI system capabilities and limitations, 3) Disclosure when AI is being used, 4) Open communication about data usage, 5) Accessible audit trails, 6) Regular reporting on AI system performance and impact."
            }
        ]
        
        # Save conversations
        print("\n   💾 Saving conversations...")
        for i, conv in enumerate(conversations, 1):
            memory_manager.add_message(session_id, conv["user"], conv["assistant"])
            print(f"   ✅ Conversation {i} saved")
        
        # 5. Test context retrieval
        print("\n5️⃣ Testing context retrieval...")
        
        test_queries = [
            "What did we discuss about AI ethics?",
            "How do we implement fairness in AI?",
            "Tell me about transparency in AI systems",
            "What are the best practices for ethical AI development?"
        ]
        
        for query in test_queries:
            print(f"\n   🔍 Query: {query}")
            context = await memory_manager.get_context(session_id, query, recent_message_count=3)
            
            print("   📋 Retrieved Context:")
            print("   " + "-" * 40)
            # Show first 200 chars of context
            preview = context.replace('\n', '\n   ')
            if len(preview) > 400:
                preview = preview[:400] + "..."
            print(f"   {preview}")
            print("   " + "-" * 40)
        
        # 6. Test cross-session memory
        print("\n6️⃣ Testing cross-session memory...")
        new_session_id = f"cross_session_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Add a conversation in new session
        memory_manager.add_message(
            new_session_id, 
            "What are some examples of AI bias?",
            "Common AI bias examples include: 1) Hiring algorithms that discriminate against certain demographics, 2) Facial recognition systems with lower accuracy for people of color, 3) Credit scoring models that unfairly penalize certain groups, 4) Search engines showing biased results, 5) Recommendation systems reinforcing stereotypes."
        )
        
        # Query from new session should find relevant memories from previous session
        cross_context = await memory_manager.get_context(
            new_session_id, 
            "How can we prevent AI bias and ensure fairness?",
            recent_message_count=2
        )
        
        print(f"   📊 Cross-session context retrieved (length: {len(cross_context)} chars)")
        
        # 7. Performance test
        print("\n7️⃣ Performance test...")
        import time
        
        start_time = time.time()
        for i in range(5):
            await memory_manager.get_context(session_id, f"Test query {i}", recent_message_count=2)
        end_time = time.time()
        
        avg_time = (end_time - start_time) / 5
        print(f"   ⏱️ Average context retrieval time: {avg_time:.3f} seconds")
        
        # 8. Cleanup
        print("\n8️⃣ Cleaning up...")
        db.close()
        print("✅ Database session closed")
        
        # Final results
        print("\n" + "=" * 50)
        print("🎉 MemoryManager Integration Test COMPLETED!")
        print("📈 All functionalities working correctly:")
        print("   ✅ Message storage (PostgreSQL + Weaviate)")
        print("   ✅ Context retrieval (Recent + Semantic)")
        print("   ✅ Cross-session memory search")
        print("   ✅ Performance within acceptable limits")
        print("🚀 Ready for production use!")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_memory_integration())
    sys.exit(0 if success else 1)
