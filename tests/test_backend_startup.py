#!/usr/bin/env python3
"""
Test script to verify backend startup without critical errors
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_imports():
    """Test if all required modules can be imported"""
    try:
        print("Testing imports...")
        from backend_app.api.chat import router
        print("✅ Chat router imported successfully")
        
        from backend_app.core.memory import VectorMemory
        print("✅ VectorMemory imported successfully")
        
        from backend_app.core.llm import get_llm_response
        print("✅ LLM module imported successfully")
        
        return True
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False

def test_environment():
    """Test environment variables"""
    print("\nTesting environment variables...")
    
    # Check Weaviate
    weaviate_key = os.getenv('WEAVIATE_API_KEY')
    if weaviate_key and weaviate_key != 'your_weaviate_api_key_here':
        print(f"✅ WEAVIATE_API_KEY: {weaviate_key[:10]}...")
    else:
        print("⚠️  WEAVIATE_API_KEY not configured")
    
    # Check Google API
    google_key = os.getenv('GOOGLE_API_KEY')
    if google_key and google_key != 'your_google_api_key_here':
        print(f"✅ GOOGLE_API_KEY: {google_key[:10]}...")
    else:
        print("⚠️  GOOGLE_API_KEY not configured")
    
    # Check Tavily API
    tavily_key = os.getenv('TAVILY_API_KEY')
    if tavily_key and tavily_key != 'your_tavily_api_key_here':
        print(f"✅ TAVILY_API_KEY: {tavily_key[:10]}...")
    else:
        print("⚠️  TAVILY_API_KEY not configured")

def test_memory_connection():
    """Test Weaviate connection"""
    print("\nTesting Weaviate connection...")
    try:
        from backend_app.core.memory import VectorMemory
        memory = VectorMemory()
        print("✅ Weaviate connection successful")
        memory.close()
        return True
    except Exception as e:
        print(f"❌ Weaviate connection failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Backend Startup Test")
    print("=" * 40)
    
    # Test imports
    if not test_imports():
        print("\n❌ Critical import errors detected!")
        return False
    
    # Test environment
    test_environment()
    
    # Test Weaviate connection
    if not test_memory_connection():
        print("\n⚠️  Weaviate connection failed - this may affect memory functionality")
    
    print("\n✅ Backend startup test completed!")
    print("\nTo fix API key issues:")
    print("1. Create a .env file with your API keys")
    print("2. Get Google API key from: https://makersuite.google.com/app/apikey")
    print("3. Get Tavily API key from: https://tavily.com/")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
