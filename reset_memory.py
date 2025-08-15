#!/usr/bin/env python3
"""
Script to completely reset the memory collection and add fresh user data
"""
import sys
import os
from dotenv import load_dotenv

# Add the project root to the Python path
sys.path.append('/Users/catiamachado/Documents/Ethic Companion V2')

# Load environment variables
load_dotenv()

from backend_app.core.memory import VectorMemory
import weaviate

def reset_memory_collection():
    """Completely reset the memory collection"""
    
    try:
        print("🧹 Connecting to Weaviate to reset memory...")
        
        # Connect directly to Weaviate to delete the collection (v4 syntax)
        client = weaviate.connect_to_local(host="localhost", port=8080)
        
        # Check if collection exists and delete it
        try:
            if client.collections.exists("MemoryItem"):
                print("🗑️  Deleting existing MemoryItem collection...")
                client.collections.delete("MemoryItem")
                print("✅ Collection deleted successfully!")
            else:
                print("ℹ️  No existing collection found.")
        except Exception as e:
            print(f"⚠️  Error deleting collection: {e}")
        finally:
            client.close()
        
        # Now create a fresh memory instance (this will recreate the collection)
        print("🆕 Creating fresh memory collection...")
        memory = VectorMemory()
        
        # Add proper user information
        print("💾 Adding fresh user information...")
        
        user_info = [
            "O nome da utilizadora é Catia (também escrito Cátia)",
            "A utilizadora prefere ser chamada Catia",
            "User: Como me chamo?\nAssistant: O seu nome é Catia.",
            "User: Qual é o meu nome?\nAssistant: O seu nome é Catia.",
            "Informação da utilizadora: Nome é Catia, localização é Portugal, fala português",
            "A utilizadora Catia tem trabalhado numa aplicação de chat AI chamada 'Ethic Companion V2'",
            "Catia tem personalizado a interface com designs orgânicos fluidos e padrões mandala",
            "A utilizadora gosta de estética de design minimalista retro",
            "Catia é programadora e desenvolvedora",
            "A Catia está a trabalhar num projeto com FastAPI backend e Next.js frontend"
        ]
        
        for info in user_info:
            memory.add_memory(info)
            print(f"✅ Added: {info[:50]}...")
        
        print("\n🔍 Testing memory search with user name...")
        
        # Test searches
        test_queries = [
            "Como me chamo?",
            "Qual é o meu nome?", 
            "nome da utilizadora",
            "Catia",
            "quem sou eu"
        ]
        
        for query in test_queries:
            results = memory.search_memory(query, limit=3)
            print(f"\n📝 Query: '{query}'")
            print(f"📊 Results ({len(results)}):")
            for i, result in enumerate(results[:3], 1):
                print(f"  {i}. {result[:80]}...")
        
        memory.close()
        print("\n✅ Memory reset and population completed!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    reset_memory_collection()
