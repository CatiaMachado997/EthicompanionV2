"""
MemoryManager Integration Example
Shows how to use the MemoryManager in the FastAPI chat endpoint
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import uuid
from datetime import datetime

from backend_app.core.memory_manager import MemoryManager

# Example models
class ChatMessage(BaseModel):
    text: str
    session_id: str = None  # Optional, will be generated if not provided

class ChatResponse(BaseModel):
    response: str
    session_id: str

# Example router
router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def handle_chat_with_memory(message: ChatMessage):
    """
    Example implementation of /chat endpoint using MemoryManager
    
    Complete workflow:
    1. Get or generate session_id
    2. Initialize MemoryManager
    3. Retrieve context from both memory systems
    4. Process with LangChain agent
    5. Save successful conversation
    6. Return response
    """
    # 1. Get or generate session_id
    session_id = message.session_id or str(uuid.uuid4())
    
    # 2. Initialize MemoryManager
    with MemoryManager() as memory_manager:
        try:
            # 3. Get context from both memory systems
            context = await memory_manager.get_context(
                session_id=session_id,
                query=message.text,
                recent_message_count=5,     # Last 5 message pairs from this session
                semantic_search_results=3   # Top 3 semantic matches from any session
            )
            
            # 4. Call agent with context (your LangChain implementation)
            agent_input = {
                "input": message.text,
                "context": context,
                "session_id": session_id
            }
            
            # Your agent executor call would go here
            # agent_response = await agent_executor.ainvoke(agent_input)
            # response_text = agent_response.get("output", "")
            
            # For demo purposes, simulating agent response
            response_text = f"I understand your message: '{message.text}'. Based on our conversation history, I can provide a contextual response."
            
            # 5. Save the new conversation turn
            save_success = memory_manager.add_message(
                session_id=session_id,
                user_message=message.text,
                assistant_message=response_text
            )
            
            if save_success:
                print(f"✅ Conversation saved for session {session_id}")
            else:
                print(f"⚠️ Failed to save conversation for session {session_id}")
            
            # 6. Return response
            return ChatResponse(
                response=response_text,
                session_id=session_id
            )
            
        except Exception as e:
            print(f"❌ Error in chat endpoint: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")

# Additional utility endpoints

@router.get("/session/{session_id}/stats")
async def get_session_stats(session_id: str):
    """Get statistics for a specific session"""
    with MemoryManager() as memory_manager:
        stats = memory_manager.get_session_statistics(session_id)
        return stats

@router.get("/session/{session_id}/history")
async def get_session_history(session_id: str, limit: int = 10):
    """Get recent conversation history for a session"""
    with MemoryManager() as memory_manager:
        # This would be a method you'd add to MemoryManager
        history = memory_manager._get_recent_history(session_id, limit)
        return {
            "session_id": session_id,
            "messages": [
                {
                    "type": msg[0],
                    "text": msg[1], 
                    "timestamp": msg[2].isoformat()
                }
                for msg in history
            ]
        }

@router.post("/admin/cleanup")
async def cleanup_old_sessions(days_to_keep: int = 30):
    """Admin endpoint to clean up old conversation data"""
    with MemoryManager() as memory_manager:
        deleted_count = memory_manager.cleanup_old_sessions(days_to_keep)
        return {
            "message": f"Cleaned up {deleted_count} old conversation records",
            "days_kept": days_to_keep
        }

# Example of how to test the integration
async def test_memory_integration():
    """
    Test function showing the complete workflow
    """
    print("🧪 Testing MemoryManager integration...")
    
    # Simulate a conversation
    messages = [
        "Hello, I'm interested in learning about machine learning",
        "Can you explain what neural networks are?", 
        "What's the difference between supervised and unsupervised learning?",
        "How do I get started with TensorFlow?"
    ]
    
    session_id = str(uuid.uuid4())
    
    with MemoryManager() as memory_manager:
        for i, msg in enumerate(messages):
            print(f"\n--- Message {i+1} ---")
            
            # Get context
            context = await memory_manager.get_context(
                session_id=session_id,
                query=msg,
                recent_message_count=3,
                semantic_search_results=2
            )
            
            print(f"Context length: {len(context)} characters")
            
            # Simulate agent response
            response = f"Response to: {msg}. Based on our conversation about machine learning..."
            
            # Save conversation
            success = memory_manager.add_message(
                session_id=session_id,
                user_message=msg,
                assistant_message=response
            )
            
            print(f"Saved: {'✅' if success else '❌'}")
        
        # Check final statistics
        stats = memory_manager.get_session_statistics(session_id)
        print(f"\n📊 Final stats: {stats}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_memory_integration())
