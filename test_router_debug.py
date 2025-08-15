#!/usr/bin/env python3
"""
Test script to debug router classification
"""
import asyncio
import os
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser

# Load environment variables
load_dotenv()

# Router prompt template (same as in chat.py)
router_prompt_template = """Given the user question, classify it as either `web_search` or `memory_search`.

`web_search` is for questions about:
- Current events, facts, news
- People (presidents, celebrities, politicians)
- Places, dates, information that changes over time
- General knowledge questions

`memory_search` is for questions about:
- Past conversations with the user
- User preferences or personal information
- "Do you remember..." type questions
- Previous discussions

Respond with ONLY one word: either "web_search" or "memory_search"

Question: {question}
Classification:"""

async def test_router_classification():
    """Test the router classification with various questions"""
    
    # Initialize the LLM
    try:
        google_key = os.getenv('GOOGLE_API_KEY')
        if not google_key or google_key == 'your_google_api_key_here':
            print("❌ Google API Key not configured")
            return
        
        router_llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0)
        router_prompt = PromptTemplate.from_template(router_prompt_template)
        router_chain = router_prompt | router_llm | StrOutputParser()
        
        print("✅ Router chain initialized successfully")
        
        # Test questions
        test_questions = [
            "Como me chamo?",  # This should be memory_search
            "Qual é o meu nome?",  # This should be memory_search  
            "Te lembras do que conversamos?",  # This should be memory_search
            "Que dia é hoje?",  # This should be web_search
            "Quem é o presidente do Brasil?",  # This should be web_search
            "O que conversamos sobre viagens?",  # This should be memory_search
        ]
        
        print("\n🔍 Testing router classification:")
        print("=" * 50)
        
        for question in test_questions:
            print(f"\n📝 Question: {question}")
            try:
                classification = await router_chain.ainvoke({"question": question})
                print(f"🏷️  Classification: '{classification.strip()}'")
                
                # Check if it's correctly classified
                if question in ["Como me chamo?", "Qual é o meu nome?", "Te lembras do que conversamos?", "O que conversamos sobre viagens?"]:
                    expected = "memory_search"
                else:
                    expected = "web_search"
                
                actual = classification.strip().lower()
                is_correct = expected in actual
                status = "✅ CORRECT" if is_correct else "❌ WRONG"
                print(f"🎯 Expected: {expected}, Got: {actual} - {status}")
                
            except Exception as e:
                print(f"❌ Error classifying: {e}")
        
        print("\n" + "=" * 50)
        
    except Exception as e:
        print(f"❌ Error initializing router: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_router_classification())
