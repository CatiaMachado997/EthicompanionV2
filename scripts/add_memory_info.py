#!/usr/bin/env python3
"""
Add proper information to memory
"""
import sys
sys.path.append('/Users/catiamachado/Documents/Ethic Companion V2')

from dotenv import load_dotenv
from backend_app.core.memory import VectorMemory

def add_useful_memory():
    """Add useful information to memory"""
    
    load_dotenv()
    
    try:
        memory = VectorMemory()
        print("✅ Connected to memory")
        
        # Add useful information about the user
        useful_info = [
            "O nome da usuária é Catia Machado.",
            "User: Eu sou a Catia\nAssistant: Olá Catia! É um prazer conhecê-la.",
            "User: Como posso me apresentar?\nAssistant: Você é a Catia Machado, uma pessoa incrível!",
            "A usuária se chama Catia e gosta de tecnologia e design.",
            "Catia está trabalhando no projeto Ethic Companion V2.",
        ]
        
        print("📝 Adding useful information to memory...")
        for info in useful_info:
            memory.add_memory(info)
            print(f"   ✅ Added: {info[:50]}...")
        
        print("\n🔍 Testing memory search...")
        results = memory.search_memory("Como me chamo?", limit=5)
        print(f"📊 Found {len(results)} results:")
        for i, result in enumerate(results, 1):
            print(f"   {i}. {result[:100]}...")
        
        memory.close()
        print("✅ Memory updated successfully!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    add_useful_memory()
