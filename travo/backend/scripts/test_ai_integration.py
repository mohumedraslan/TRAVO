"""
Test AI Integration - DeepSeek + Google Vision
"""
import requests
import json
import base64
from PIL import Image
import io

BASE_URL = "http://127.0.0.1:8000/api"

print("="*70)
print("TRAVO AI INTEGRATION TEST")
print("DeepSeek API + Google Vision API")
print("="*70)

# Test 1: Text Query
print("\n" + "="*70)
print("TEST 1: TEXT QUERY")
print("="*70)
try:
    payload = {
        "query": "Tell me about the pedestal in the museum.",
        "location": "Egyptian Museum, Cairo",
        "query_type": "TEXT"
    }
    
    print(f"\nSending request to /assistant/ask...")
    print(f"Payload: {json.dumps(payload, indent=2)}")
    
    response = requests.post(
        f"{BASE_URL}/assistant/ask",
        json=payload,
        timeout=30
    )
    
    print(f"\nStatus Code: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"\n✅ TEXT QUERY SUCCESS!")
        print(f"\nType: {result.get('type')}")
        print(f"Original Query: {result.get('original_query')}")
        print(f"Location: {result.get('location')}")
        print(f"\nDeepSeek Response:")
        print("-" * 70)
        print(result.get('deepseek_response', 'No response'))
        print("-" * 70)
    else:
        print(f"\n❌ TEXT QUERY FAILED")
        print(f"Response: {response.text}")
        
except Exception as e:
    print(f"\n❌ ERROR: {e}")

# Test 2: Image Query
print("\n" + "="*70)
print("TEST 2: IMAGE QUERY")
print("="*70)
try:
    # Create a test image (you can replace this with a real monument image)
    print("\nCreating test image...")
    img = Image.new('RGB', (400, 300), color='blue')
    
    # Add some text to make it more interesting
    from PIL import ImageDraw, ImageFont
    draw = ImageDraw.Draw(img)
    draw.text((50, 150), "TEST MONUMENT", fill='white')
    
    # Convert to base64
    buffer = io.BytesIO()
    img.save(buffer, format='JPEG')
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    
    print(f"Image size: {len(image_base64)} bytes (base64)")
    
    payload = {
        "query": "What can you tell me about this landmark?",
        "location": "Cairo, Egypt",
        "query_type": "IMAGE",
        "image": image_base64
    }
    
    print(f"\nSending request to /assistant/ask...")
    print(f"Query: {payload['query']}")
    print(f"Location: {payload['location']}")
    print(f"Query Type: {payload['query_type']}")
    
    response = requests.post(
        f"{BASE_URL}/assistant/ask",
        json=payload,
        timeout=60  # Longer timeout for image processing
    )
    
    print(f"\nStatus Code: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"\n✅ IMAGE QUERY SUCCESS!")
        print(f"\nType: {result.get('type')}")
        print(f"Original Query: {result.get('original_query')}")
        print(f"Landmark Detected: {result.get('landmark_detected', 'None')}")
        if result.get('confidence'):
            print(f"Confidence: {result.get('confidence'):.2%}")
        if result.get('description'):
            print(f"Description: {result.get('description')}")
        print(f"Location: {result.get('location')}")
        print(f"\nDeepSeek Response:")
        print("-" * 70)
        print(result.get('deepseek_response', 'No response'))
        print("-" * 70)
    else:
        print(f"\n❌ IMAGE QUERY FAILED")
        print(f"Response: {response.text}")
        
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    import traceback
    traceback.print_exc()

# Test 3: Invalid Query Type
print("\n" + "="*70)
print("TEST 3: INVALID QUERY TYPE (Error Handling)")
print("="*70)
try:
    payload = {
        "query": "Test query",
        "query_type": "INVALID"
    }
    
    response = requests.post(
        f"{BASE_URL}/assistant/ask",
        json=payload,
        timeout=10
    )
    
    print(f"\nStatus Code: {response.status_code}")
    
    if response.status_code == 400:
        print(f"✅ Error handling works correctly!")
        print(f"Response: {response.json()}")
    else:
        print(f"Response: {response.text}")
        
except Exception as e:
    print(f"❌ ERROR: {e}")

# Test 4: Missing Image for IMAGE Query
print("\n" + "="*70)
print("TEST 4: MISSING IMAGE (Error Handling)")
print("="*70)
try:
    payload = {
        "query": "What is this?",
        "query_type": "IMAGE"
        # No image field
    }
    
    response = requests.post(
        f"{BASE_URL}/assistant/ask",
        json=payload,
        timeout=10
    )
    
    print(f"\nStatus Code: {response.status_code}")
    
    if response.status_code == 400:
        print(f"✅ Error handling works correctly!")
        print(f"Response: {response.json()}")
    else:
        print(f"Response: {response.text}")
        
except Exception as e:
    print(f"❌ ERROR: {e}")

print("\n" + "="*70)
print("TEST COMPLETE")
print("="*70)
print("\nSummary:")
print("- Text queries use DeepSeek API for conversational responses")
print("- Image queries use Google Vision for landmark detection")
print("- Then DeepSeek provides detailed information about detected landmarks")
print("- Error handling works for invalid inputs")
print("\n" + "="*70)
