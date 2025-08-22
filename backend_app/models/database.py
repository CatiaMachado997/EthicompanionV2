"""
Database models for Ethic Companion V2
SQLAlchemy models for PostgreSQL database
"""

from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
import os

Base = declarative_base()

class ChatHistory(Base):
    """
    Model for storing chat history in PostgreSQL
    Compatible with hybrid memory system - stores individual messages
    """
    __tablename__ = "chat_history"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(255), nullable=False, index=True)
    message_type = Column(String(50), nullable=False)  # 'user' or 'assistant'
    user_message = Column(Text, nullable=True)  # For user messages
    assistant_message = Column(Text, nullable=True)  # For assistant responses
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    processed = Column(Boolean, default=False)  # For tracking if stored in vector DB
    
    def __repr__(self):
        return f"<ChatHistory(id={self.id}, session={self.session_id}, type={self.message_type})>"

# Database configuration
def get_database_url():
    """
    Get database URL from environment variables
    Supports both development (SQLite) and production (PostgreSQL)
    """
    # Check for production PostgreSQL URL first
    db_url = os.getenv("DATABASE_URL")
    if db_url:
        return db_url
    
    # Development fallback to SQLite
    return "sqlite:///./ethic_companion.db"

# Create engine and session factory
engine = create_engine(
    get_database_url(),
    echo=False,  # Set to True for SQL debugging
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_tables():
    """Create all database tables"""
    Base.metadata.create_all(bind=engine)

def get_db():
    """
    FastAPI dependency to get database session
    Ensures proper session management and cleanup
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_db_session():
    """
    Direct method to get database session (for non-FastAPI usage)
    Remember to close the session manually
    """
    return SessionLocal()

def close_db_session(db):
    """Close database session"""
    db.close()
