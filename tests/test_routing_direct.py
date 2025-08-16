#!/usr/bin/env python3
"""
Direct test of the routing chain without HTTP
"""
import asyncio
import os
from dotenv import load_dotenv

# Import the components from our chat module
import sys
sys.path.append('/Users/catiamachado/Documents/Ethic Companion V2')

from backend_app.api.chat import full_chain, router_chain, execute_memory_search

async def test_routing_directly():
    """Test the routing logic directly"""
    
    load_dotenv()
    
    print("🔍 Testing routing chain directly...")
    
    test_question = "Como me chamo?"
    
    try:
        # Test 1: Router classification only
        if router_chain:
            print(f"\n1️⃣ Testing router classification for: '{test_question}'")
            classification = await router_chain.ainvoke({"question": test_question})
            print(f"   Classification: '{classification.strip()}'")
        
        # Test 2: Memory search directly
        print(f"\n2️⃣ Testing memory search directly for: '{test_question}'")
        memory_result = await execute_memory_search(test_question)
        print(f"   Memory result: {memory_result[:100]}...")
        
        # Test 3: Full chain
        if full_chain:
            print(f"\n3️⃣ Testing full routing chain for: '{test_question}'")
            full_result = await full_chain.ainvoke({"question": test_question})
            print(f"   Full chain result: {full_result[:100]}...")
        
    except Exception as e:
        print(f"❌ Error in direct testing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_routing_directly())
