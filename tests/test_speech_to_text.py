#!/usr/bin/env python3
"""
Test script for the speech-to-text functionality
"""

import asyncio
import sys
import os

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend_app.api.chat import speech_to_text
from backend_app.core.config import load_api_keys

async def test_speech_to_text():
    """
    Test the speech_to_text function
    Note: This test requires an actual audio file and OpenAI API key
    """
    try:
        # Load API keys
        load_api_keys()
        print("🔑 API keys carregadas")
        
        # For testing, you would need an actual audio file
        # This is a placeholder test
        print("📝 Teste de speech-to-text")
        print("⚠️  Para testar completamente, você precisa:")
        print("   1. Configurar OPENAI_API_KEY no arquivo .env")
        print("   2. Ter um arquivo de áudio para teste")
        print("   3. Chamar a função com o arquivo de áudio")
        
        # Example of how to use with a real audio file:
        """
        with open("path/to/your/audio.wav", "rb") as audio_file:
            result = await speech_to_text(audio_file)
            print(f"Texto transcrito: {result}")
        """
        
        print("✅ Função speech_to_text importada com sucesso")
        return True
        
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🧪 Testando funcionalidade de Speech-to-Text")
    success = asyncio.run(test_speech_to_text())
    if success:
        print("✅ Teste concluído com sucesso")
    else:
        print("❌ Teste falhou")
