#!/usr/bin/env python3
"""
Integration test - add user info and test the complete system
"""
import sys
import os
import requests
import time
from dotenv import load_dotenv

# Add the project root to the Python path
sys.path.append('/Users/catiamachado/Documents/Ethic Companion V2')

# Load environment variables
load_dotenv()

from backend_app.core.memory import VectorMemory

def add_user_info_to_memory():
    """Add proper user information to memory"""
    try:
        print("💾 Adding user information to memory...")
        memory = VectorMemory()
        
        # Add clear, useful information about the user
        user_info = [
            "O nome da utilizadora é Catia",
            "A utilizadora chama-se Catia Machado", 
            "User: Como me chamo?\nAssistant: O seu nome é Catia.",
            "User: Qual é o meu nome?\nAssistant: Você se chama Catia.",
            "Informações sobre a utilizadora: Nome: Catia Machado, Profissão: Programadora, Localização: Portugal",
            "A Catia está a desenvolver uma aplicação de chat AI"
        ]
        
        for info in user_info:
            memory.add_memory(info)
            print(f"✅ Added: {info[:50]}...")
        
        print("🔍 Testing memory search...")
        test_results = memory.search_memory("Como me chamo", limit=3)
        print(f"📊 Found {len(test_results)} results:")
        for i, result in enumerate(test_results, 1):
            print(f"  {i}. {result[:80]}...")
        
        memory.close()
        return True
        
    except Exception as e:
        print(f"❌ Error adding user info: {e}")
        return False

def test_chat_api():
    """Test the chat API"""
    try:
        print("\n🚀 Testing chat API...")
        
        url = "http://localhost:8000/chat"
        headers = {"Content-Type": "application/json"}
        data = {"text": "Como me chamo?"}
        
        response = requests.post(url, headers=headers, json=data, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ API Response: {result['reply']}")
            return True
        else:
            print(f"❌ API Error: {response.status_code} - {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to API. Server not running?")
        return False
    except Exception as e:
        print(f"❌ API Test Error: {e}")
        return False

def main():
    print("🧪 Integration Test: Memory + Chat API")
    print("=" * 50)
    
    # Step 1: Add user info to memory
    if not add_user_info_to_memory():
        print("❌ Failed to add user info to memory")
        return
    
    # Step 2: Wait a moment
    print("\n⏳ Waiting for system to be ready...")
    time.sleep(2)
    
    # Step 3: Test the API
    if test_chat_api():
        print("\n✅ Integration test successful!")
    else:
        print("\n❌ Integration test failed!")
        
    # Step 4: Check for failed response logs
    print("\n📋 Checking failed response logs...")
    try:
        with open("failed_responses.log", "r") as f:
            content = f.read()
            if content.strip():
                print("📝 Failed responses logged:")
                print(content)
            else:
                print("✅ No failed responses logged")
    except FileNotFoundError:
        print("ℹ️  No failed response log file found")

if __name__ == "__main__":
    main()
