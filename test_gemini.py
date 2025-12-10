
import os
import asyncio
import google.generativeai as genai
from dotenv import load_dotenv

# Load from backend/.env
load_dotenv(r"c:\Users\moras\Documents\GitHub\TRAVO\travo\backend\.env")

# Manually set key for test if env var isn't picked up by python process yet
# (PowerShell env var might only be in that shell session, but let's try reading os.environ)
# If it fails, I'll ask user to paste it here or rely on the shell.

API_KEY = os.getenv("GEMINI_API_KEY") 

async def test_gemini():
    print(f"Checking API Key: {'Found' if API_KEY else 'Not Found'}")
    
    if not API_KEY:
        print("Please set GEMINI_API_KEY environment variable.")
        return

    try:
        genai.configure(api_key=API_KEY)
        print("Listing available models...")
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(f"- {m.name}")
        print("✅ Configured.")
        
    except Exception as e:
        print(f"❌ Gemini Connection Failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_gemini())
