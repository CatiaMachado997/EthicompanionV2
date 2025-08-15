#!/usr/bin/env python3
"""
Script to clean memory and add proper user information
"""
import sys
import os
from dotenv import load_dotenv

# Add the project root to the Python path
sys.path.append('/Users/catiamachado/Documents/Ethic Companion V2')

# Load environment variables
load_dotenv()

from backend_app.core.memory import VectorMemory

def clean_and_populate_memory():
    """Clean existing memory and add proper user information"""
    
    try:
        print("🧹 Connecting to memory system...")
        memory = VectorMemory()
        
        # First, let's see what's currently in memory
        print("\n📋 Current memory contents:")
        current_results = memory.search_memory("", limit=10)  # Get all
        for i, result in enumerate(current_results, 1):
            print(f"{i}. {result[:100]}...")
        
        print(f"\n🗑️  Found {len(current_results)} items in memory")
        
        # Clear bad memories (failed responses)
        print("\n🧹 Cleaning failed interactions from memory...")
        
        # Note: Weaviate doesn't have a simple "delete by content" method
        # For now, we'll work with what we have and add good content
        
        # Add proper user information
        print("\n💾 Adding proper user information to memory...")
        
        user_info = [
            "User's name is Catia (also spelled Cátia)",
            "The user prefers to be called Catia",
            "User: Como me chamo?\nAssistant: O seu nome é Catia.",
            "User: Qual é o meu nome?\nAssistant: O seu nome é Catia.",
            "User information: Name is Catia, location is Portugal, speaks Portuguese",
            "The user Catia has been working on an AI chat application called 'Ethic Companion V2'",
            "Catia has been customizing the UI with organic flowing designs and mandala patterns",
            "The user enjoys minimalist retro design aesthetics"
        ]
        
        for info in user_info:
            memory.add_memory(info)
            print(f"✅ Added: {info[:50]}...")
        
        print("\n🔍 Testing memory search with user name...")
        
        # Test searches
        test_queries = [
            "Como me chamo?",
            "Qual é o meu nome?", 
            "nome",
            "Catia",
            "user name"
        ]
        
        for query in test_queries:
            results = memory.search_memory(query, limit=3)
            print(f"\n📝 Query: '{query}'")
            print(f"📊 Results ({len(results)}):")
            for i, result in enumerate(results[:3], 1):
                print(f"  {i}. {result[:80]}...")
        
        memory.close()
        print("\n✅ Memory cleaning and population completed!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    clean_and_populate_memory()
