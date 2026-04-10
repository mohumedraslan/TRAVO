"""Quick test for TEXT query only"""
import requests
import json

BASE_URL = "http://127.0.0.1:8000/api"

print("Testing TEXT query to /assistant/ask...")
print("="*60)

payload = {
    "query": "Tell me about the Sphinx",
    "location": "Giza, Egypt",
    "query_type": "TEXT"
}

print(f"\nRequest:")
print(json.dumps(payload, indent=2))

try:
    response = requests.post(
        f"{BASE_URL}/assistant/ask",
        json=payload,
        timeout=30
    )
    
    print(f"\nStatus: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"\n✅ SUCCESS!")
        print(f"\nResponse:")
        print(json.dumps(result, indent=2))
    else:
        print(f"\n❌ FAILED")
        print(f"Response: {response.text}")
        
except Exception as e:
    print(f"\n❌ ERROR: {e}")
