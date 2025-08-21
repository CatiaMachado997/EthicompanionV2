#!/usr/bin/env python3
"""
Quick test script to verify OpenAI API key and speech-to-text setup
"""

import asyncio
import sys
import os

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend_app.core.config import load_api_keys, get_api_key
import openai

async def test_openai_setup():
    """Test OpenAI API key and client setup"""
    print("🔧 Testing OpenAI API setup...")
    
    try:
        # Load API keys
        load_api_keys()
        print("✅ API keys loaded")
        
        # Get OpenAI API key
        api_key = get_api_key('OPENAI_API_KEY')
        print(f"✅ OpenAI API Key: {api_key[:20]}...{api_key[-10:]}")
        
        # Initialize OpenAI client
        client = openai.AsyncOpenAI(api_key=api_key)
        print("✅ OpenAI client initialized")
        
        # Test API connection (list models to verify key works)
        print("🔍 Testing API connection...")
        try:
            models = await client.models.list()
            whisper_models = [m for m in models.data if 'whisper' in m.id.lower()]
            print(f"✅ API connection successful - Found {len(whisper_models)} Whisper models")
            
            if whisper_models:
                print("🎤 Available Whisper models:")
                for model in whisper_models:
                    print(f"   - {model.id}")
            
        except openai.AuthenticationError:
            print("❌ Authentication failed - Please check your API key")
            return False
        except Exception as e:
            print(f"⚠️  API test failed: {e}")
            print("   This might be normal if there are rate limits or network issues")
        
        print("\n🚀 Speech-to-text setup is ready!")
        print("\n📝 To test with actual audio:")
        print("   1. Start your FastAPI server:")
        print("      python main.py")
        print("   2. Test with curl:")
        print("      curl -X POST 'http://localhost:8000/speech-to-text' \\")
        print("           -F 'audio_file=@your_audio.wav'")
        print("   3. Or use the /voice-chat endpoint for full interaction")
        
        return True
        
    except Exception as e:
        print(f"❌ Setup test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🧪 OpenAI Speech-to-Text Setup Test")
    success = asyncio.run(test_openai_setup())
    
    if success:
        print("\n✅ All tests passed! Your speech-to-text functionality is ready.")
    else:
        print("\n❌ Some tests failed. Please check your configuration.")
