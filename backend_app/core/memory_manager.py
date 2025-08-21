"""
Comprehensive MemoryManager Class
Orchestrates both PostgreSQL (episodic) and Weaviate (semantic) memory operations
"""

import weaviate
from sqlalchemy.orm import Session
from sqlalchemy import desc
from datetime import datetime, timezone
from typing import List, Optional, Tuple
import uuid
import logging

from backend_app.models.database import ChatHistory, get_db_session, close_db_session, create_tables
from backend_app.core.memory import VectorMemory
from backend_app.core.config import get_weaviate_config

logger = logging.getLogger(__name__)

class MemoryManager:
    """
    Orchestrates memory operations between PostgreSQL (episodic) and Weaviate (semantic).
    
    Features:
    - Dual storage: Recent conversation history + Long-term semantic memory
    - Intelligent context retrieval combining both sources
    - Session-based organization with cross-session semantic search
    - Portuguese language optimization
    """
    
    def __init__(self, db_session: Session, weaviate_client=None):
        self.db = db_session
        
        # Initialize Weaviate client
        if weaviate_client:
            self.weaviate = weaviate_client
        else:
            self.weaviate = create_weaviate_client()
            
        # Ensure collection exists
        self._ensure_collection_exists()
    
    def close(self):
        """Close Weaviate connection properly"""
        if hasattr(self.weaviate, 'close'):
            self.weaviate.close()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
    
    def add_message(self, session_id: str, user_message: str, assistant_message: str, 
                   timestamp: Optional[datetime] = None) -> bool:
        """
        Saves a conversation turn to both PostgreSQL and Weaviate
        
        Args:
            session_id: Unique session identifier
            user_message: User's input message
            assistant_message: Assistant's response
            timestamp: Optional timestamp (defaults to now)
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if timestamp is None:
                timestamp = datetime.now(timezone.utc)
            
            # --- PostgreSQL: Save individual messages ---
            success_db = self._save_to_postgresql(session_id, user_message, assistant_message, timestamp)
            
            # --- Weaviate: Save combined conversation ---
            success_vector = self._save_to_weaviate(session_id, user_message, assistant_message, timestamp)
            
            if success_db and success_vector:
                logger.info(f"✅ Conversation saved successfully to both stores (session: {session_id})")
                return True
            elif success_db:
                logger.warning(f"⚠️ Conversation saved to PostgreSQL only (session: {session_id})")
                return True
            else:
                logger.error(f"❌ Failed to save conversation (session: {session_id})")
                return False
                
        except Exception as e:
            logger.error(f"❌ Error in add_message: {e}")
            return False
    
    def _save_to_postgresql(self, session_id: str, user_message: str, 
                          assistant_message: str, timestamp: datetime) -> bool:
        """
        Save messages to PostgreSQL database
        
        Args:
            session_id: Session identifier
            user_message: User's message
            assistant_message: Assistant's response  
            timestamp: Message timestamp
            
        Returns:
            bool: Success status
        """
        try:
            # Create user message entry
            user_entry = ChatHistory(
                session_id=session_id,
                message_type="user",
                message_text=user_message,
                timestamp=timestamp,
                processed=False
            )
            
            # Create assistant message entry
            assistant_entry = ChatHistory(
                session_id=session_id,
                message_type="assistant", 
                message_text=assistant_message,
                timestamp=timestamp,
                processed=False
            )
            
            # Add to database
            self.db.add(user_entry)
            self.db.add(assistant_entry)
            self.db.commit()
            
            logger.info(f"✅ Messages saved to PostgreSQL (session: {session_id})")
            return True
            
        except Exception as e:
            logger.error(f"❌ PostgreSQL save error: {e}")
            self.db.rollback()
            return False
    
    def _save_to_weaviate(self, session_id: str, user_message: str, 
                         assistant_message: str, timestamp: datetime) -> bool:
        """
        Save combined conversation to Weaviate for semantic search
        
        Args:
            session_id: Session identifier
            user_message: User's message
            assistant_message: Assistant's response
            timestamp: Message timestamp
            
        Returns:
            bool: Success status
        """
        try:
            if not self.weaviate and not self.vector_memory:
                logger.warning("⚠️ Weaviate not available, skipping vector storage")
                return False
            
            # Create combined document for semantic search
            combined_text = f"User: {user_message}\nAssistant: {assistant_message}"
            
            # Prepare metadata
            metadata = {
                "session_id": session_id,
                "timestamp": timestamp.isoformat(),
                "user_message": user_message,
                "assistant_message": assistant_message,
                "conversation_id": str(uuid.uuid4())
            }
            
            # Use VectorMemory if available, otherwise direct Weaviate client
            if self.vector_memory:
                self.vector_memory.add_memory(combined_text)
            else:
                # Direct Weaviate storage with metadata
                data = {
                    "text": combined_text,
                    **metadata
                }
                self.weaviate.collections.get("MemoryItem").data.insert(data)
            
            logger.info(f"✅ Conversation saved to Weaviate (session: {session_id})")
            return True
            
        except Exception as e:
            logger.error(f"❌ Weaviate save error: {e}")
            return False
    
    async def get_context(self, session_id: str, query: str, 
                          recent_message_count: int = 5, 
                          semantic_search_results: int = 3) -> str:
        """
        Retrieves and combines context from both memory systems
        
        Args:
            session_id: Current session identifier
            query: User's latest query for semantic search
            recent_message_count: Number of recent messages to retrieve
            semantic_search_results: Number of semantic results to find
            
        Returns:
            str: Formatted context string combining both memory sources
        """
        try:
            # --- Retrieve Recent History (PostgreSQL) ---
            recent_history = self._get_recent_history(session_id, recent_message_count)
            
            # --- Retrieve Relevant Memories (Weaviate) ---
            long_term_memories = self._get_semantic_memories(query, semantic_search_results, session_id)
            
            # --- Format and Combine Context ---
            formatted_context = self._format_context(recent_history, long_term_memories)
            
            logger.info(f"✅ Context retrieved for session {session_id}: "
                       f"{len(recent_history)} recent + {len(long_term_memories)} semantic results")
            
            return formatted_context
            
        except Exception as e:
            logger.error(f"❌ Error retrieving context: {e}")
            return ""
    
    def _get_recent_history(self, session_id: str, limit: int) -> List[Tuple[str, str, datetime]]:
        """
        Fetch recent conversation history from PostgreSQL
        
        Args:
            session_id: Session to retrieve from
            limit: Maximum number of message pairs to return
            
        Returns:
            List of (message_type, message_text, timestamp) tuples
        """
        try:
            # Get recent messages for this session, ordered by timestamp
            recent_messages = (
                self.db.query(ChatHistory)
                .filter(ChatHistory.session_id == session_id)
                .order_by(desc(ChatHistory.timestamp))
                .limit(limit * 2)  # *2 because we have user + assistant pairs
                .all()
            )
            
            # Reverse to get chronological order
            recent_messages.reverse()
            
            # Convert to tuples
            history = [
                (msg.message_type, msg.message_text, msg.timestamp)
                for msg in recent_messages
            ]
            
            logger.info(f"📚 Retrieved {len(history)} recent messages from PostgreSQL")
            return history
            
        except Exception as e:
            logger.error(f"❌ Error retrieving recent history: {e}")
            return []
    
    def _get_semantic_memories(self, query: str, limit: int, 
                              exclude_session: Optional[str] = None) -> List[str]:
        """
        Perform semantic search in Weaviate for relevant past conversations
        
        Args:
            query: Search query text
            limit: Maximum results to return
            exclude_session: Session ID to exclude from results
            
        Returns:
            List of relevant conversation texts
        """
        try:
            if not self.weaviate and not self.vector_memory:
                logger.warning("⚠️ Weaviate not available for semantic search")
                return []
            
            # Use VectorMemory if available
            if self.vector_memory:
                results = self.vector_memory.search_memory(query, limit=limit)
                logger.info(f"🔍 Retrieved {len(results)} semantic results from VectorMemory")
                return results
            
            # Direct Weaviate search as fallback
            response = (
                self.weaviate.collections.get("MemoryItem")
                .query
                .near_text(query=query, limit=limit)
            )
            
            results = []
            for obj in response.objects:
                text = obj.properties["text"]
                # Filter out current session if specified
                if exclude_session and "session_id" in obj.properties:
                    if obj.properties["session_id"] == exclude_session:
                        continue
                results.append(text)
            
            logger.info(f"🔍 Retrieved {len(results)} semantic results from Weaviate")
            return results
            
        except Exception as e:
            logger.error(f"❌ Error in semantic search: {e}")
            return []
    
    def _format_context(self, recent_history: List[Tuple[str, str, datetime]], 
                       long_term_memories: List[str]) -> str:
        """
        Format retrieved information into a single context string
        
        Args:
            recent_history: List of recent message tuples
            long_term_memories: List of relevant memory texts
            
        Returns:
            str: Formatted context for LLM
        """
        context_parts = []
        
        # Add recent conversation history
        if recent_history:
            context_parts.append("[Recent Conversation History]")
            for msg_type, msg_text, timestamp in recent_history:
                # Format timestamp for readability
                time_str = timestamp.strftime("%H:%M")
                context_parts.append(f"{time_str} {msg_type.title()}: {msg_text}")
            context_parts.append("")  # Empty line separator
        
        # Add relevant long-term memories
        if long_term_memories:
            context_parts.append("[Relevant Long-Term Memories]")
            for i, memory in enumerate(long_term_memories, 1):
                context_parts.append(f"{i}. {memory}")
            context_parts.append("")  # Empty line separator
        
        # If no context available
        if not context_parts:
            return "[No previous context available]"
        
        return "\n".join(context_parts)
    
    def get_session_statistics(self, session_id: str) -> dict:
        """
        Get statistics for a specific session
        
        Args:
            session_id: Session to analyze
            
        Returns:
            dict: Session statistics
        """
        try:
            # Count messages in session
            total_messages = (
                self.db.query(ChatHistory)
                .filter(ChatHistory.session_id == session_id)
                .count()
            )
            
            user_messages = (
                self.db.query(ChatHistory)
                .filter(ChatHistory.session_id == session_id)
                .filter(ChatHistory.message_type == "user")
                .count()
            )
            
            assistant_messages = (
                self.db.query(ChatHistory)
                .filter(ChatHistory.session_id == session_id)
                .filter(ChatHistory.message_type == "assistant")
                .count()
            )
            
            # Get session timespan
            first_message = (
                self.db.query(ChatHistory)
                .filter(ChatHistory.session_id == session_id)
                .order_by(ChatHistory.timestamp)
                .first()
            )
            
            last_message = (
                self.db.query(ChatHistory)
                .filter(ChatHistory.session_id == session_id)
                .order_by(desc(ChatHistory.timestamp))
                .first()
            )
            
            return {
                "session_id": session_id,
                "total_messages": total_messages,
                "user_messages": user_messages,
                "assistant_messages": assistant_messages,
                "first_message_time": first_message.timestamp if first_message else None,
                "last_message_time": last_message.timestamp if last_message else None,
                "conversation_pairs": min(user_messages, assistant_messages)
            }
            
        except Exception as e:
            logger.error(f"❌ Error getting session statistics: {e}")
            return {"error": str(e)}
    
    def cleanup_old_sessions(self, days_to_keep: int = 30) -> int:
        """
        Clean up old conversation data
        
        Args:
            days_to_keep: Number of days of data to retain
            
        Returns:
            int: Number of records deleted
        """
        try:
            from datetime import timedelta
            cutoff_date = datetime.now(timezone.utc) - timedelta(days=days_to_keep)
            
            # Delete old records
            deleted_count = (
                self.db.query(ChatHistory)
                .filter(ChatHistory.timestamp < cutoff_date)
                .delete()
            )
            
            self.db.commit()
            logger.info(f"🧹 Cleaned up {deleted_count} old conversation records")
            return deleted_count
            
        except Exception as e:
            logger.error(f"❌ Error cleaning up old sessions: {e}")
            self.db.rollback()
            return 0
    
    def close(self):
        """
        Close all connections and clean up resources
        """
        try:
            # Close database session if we own it
            if self._own_db_session and self.db:
                close_db_session(self.db)
            
            # Close Weaviate connection
            if self.vector_memory:
                self.vector_memory.close()
            elif self.weaviate:
                self.weaviate.close()
            
            logger.info("✅ MemoryManager connections closed")
            
        except Exception as e:
            logger.error(f"❌ Error closing MemoryManager: {e}")
    
    def __enter__(self):
        """Context manager entry"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()
