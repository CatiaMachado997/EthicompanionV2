#!/usr/bin/env python3
"""
Direct test of the routing system to debug memory issues
"""
import asyncio
import os
import sys
from dotenv import load_dotenv

# Add the project root to the path
sys.path.append('/Users/catiamachado/Documents/Ethic Companion V2')

from backend_app.core.memory import VectorMemory

async def test_memory_directly():
    """Test the memory system directly"""
    print("🧠 Testing memory system directly...")
    
    try:
        # Create memory manager
        memory_manager = VectorMemory()
        print("✅ VectorMemory instance created")
        
        # Test search
        question = "Como me chamo?"
        print(f"🔍 Searching for: {question}")
        
        results = memory_manager.search_memory(question, limit=5)
        print(f"📊 Search results: {results}")
        print(f"📊 Number of results: {len(results) if results else 0}")
        
        if results:
            print("✅ Found memories:")
            for i, result in enumerate(results, 1):
                print(f"  {i}. {result}")
        else:
            print("❌ No memories found")
            
        # Check if we have any memories at all
        print("\n🔍 Checking all memories...")
        all_results = memory_manager.search_memory("", limit=10)  # Empty query to get all
        print(f"📊 Total memories in database: {len(all_results) if all_results else 0}")
        
        if all_results:
            print("📝 All memories:")
            for i, result in enumerate(all_results, 1):
                print(f"  {i}. {result[:100]}...")
        
        memory_manager.close()
        
    except Exception as e:
        print(f"❌ Error testing memory: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # Load environment variables
    load_dotenv()
    
    asyncio.run(test_memory_directly())
