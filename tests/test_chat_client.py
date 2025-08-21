#!/usr/bin/env python3
"""
Test script to call the chat endpoint and show debugging
"""
import requests
import json
import time

def test_chat_endpoint():
    """Test the chat endpoint"""
    
    # Wait for server to be ready
    time.sleep(2)
    
    url = "http://localhost:8000/chat"
    headers = {"Content-Type": "application/json"}
    data = {"text": "Como me chamo?"}
    
    print(f"🚀 Sending request to {url}")
    print(f"📝 Data: {data}")
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)
        
        print(f"📊 Status Code: {response.status_code}")
        print(f"📋 Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            response_data = response.json()
            print(f"✅ Response: {response_data}")
        else:
            print(f"❌ Error Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server. Is it running?")
    except requests.exceptions.Timeout:
        print("❌ Request timed out")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_chat_endpoint()
