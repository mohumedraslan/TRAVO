"""
Test all fixes for demo readiness
"""
import requests
import json

BASE_URL = "http://127.0.0.1:8000"

print("="*60)
print("TRAVO FIXES VERIFICATION")
print("="*60)

# Test 1: Login with test user
print("\n1. Testing login with test user...")
try:
    response = requests.post(
        f"{BASE_URL}/api/user/login",
        data={
            "username": "test@travo.com",
            "password": "testpass123"
        }
    )
    if response.status_code == 200:
        print("✅ Login successful!")
        token = response.json().get('access_token')
        print(f"   Token: {token[:20]}...")
    else:
        print(f"❌ Login failed: {response.status_code}")
        print(f"   Response: {response.json()}")
except Exception as e:
    print(f"❌ Error: {e}")

# Test 2: Get mock itinerary
print("\n2. Testing mock itinerary endpoint...")
try:
    response = requests.get(f"{BASE_URL}/api/itineraries/mock-itinerary-1")
    if response.status_code == 200:
        print("✅ Itinerary found!")
        data = response.json()
        print(f"   Title: {data.get('title')}")
        print(f"   Destination: {data.get('destination')}")
    else:
        print(f"❌ Failed: {response.status_code}")
        print(f"   Response: {response.json()}")
except Exception as e:
    print(f"❌ Error: {e}")

# Test 3: Vision endpoint
print("\n3. Testing vision identify endpoint...")
try:
    import base64
    from PIL import Image
    import io
    
    img = Image.new('RGB', (224, 224), color='green')
    buffer = io.BytesIO()
    img.save(buffer, format='JPEG')
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    
    response = requests.post(
        f"{BASE_URL}/api/vision/identify",
        json={"image": image_base64},
        timeout=30
    )
    if response.status_code == 200:
        print("✅ Vision endpoint working!")
        data = response.json()
        print(f"   Monument: {data.get('identified_monument')}")
        print(f"   Confidence: {data.get('confidence'):.4f}")
    else:
        print(f"❌ Failed: {response.status_code}")
except Exception as e:
    print(f"❌ Error: {e}")

print("\n" + "="*60)
print("VERIFICATION COMPLETE")
print("="*60)
