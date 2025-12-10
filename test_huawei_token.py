import requests
import json
import os

# The token provided by the user
TOKEN = "CcbRY-OG3iLi569ybZAIRscxj8pkfED6MflBbYY5pZt-tx_qFIqhadVXJ_-IAFInEAb1Q7R0vn0Kso8AVWOw2A"

# Correct API Endpoint from PDF
API_URL = "https://api-ap-southeast-1.modelarts-maas.com/v1/chat/completions"

def test_chat_completion():
    print(f"Testing API against {API_URL}...")
    
    headers = {
        "Content-Type": "application/json",
        "X-Auth-Token": TOKEN
    }
    
    # Payload for Qwen3-32B (Text only)
    payload = {
        "model": "qwen3-32b",
        "messages": [
            {
                "role": "user",
                "content": "Hello! Can you identify monuments? This is a test."
            }
        ],
        "max_tokens": 100,
        "temperature": 0.7
    }
    
    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ API Call SUCCESS!")
            data = response.json()
            print("Response:")
            print(json.dumps(data, indent=2))
        else:
            print("❌ API Call FAILED.")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"Error testing API: {e}")

if __name__ == "__main__":
    test_chat_completion()
