"""
Test all critical endpoints for demo
"""
import requests
import json
import base64
from PIL import Image
import io

BASE_URL = "http://127.0.0.1:8000"

def test_root():
    """Test root endpoint"""
    print("\n1. Testing root endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"✅ Status: {response.status_code}")
        print(f"   Response: {response.json()}")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_vision_identify():
    """Test vision identify endpoint"""
    print("\n2. Testing vision identify endpoint...")
    try:
        # Create a test image
        img = Image.new('RGB', (224, 224), color='blue')
        buffer = io.BytesIO()
        img.save(buffer, format='JPEG')
        image_bytes = buffer.getvalue()
        image_base64 = base64.b64encode(image_bytes).decode('utf-8')
        
        response = requests.post(
            f"{BASE_URL}/api/vision/identify",
            json={"image": image_base64},
            timeout=60
        )
        print(f"✅ Status: {response.status_code}")
        result = response.json()
        print(f"   Monument: {result.get('identified_monument')}")
        print(f"   Confidence: {result.get('confidence'):.4f}")
        print(f"   Candidates: {len(result.get('candidates', []))}")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_itinerary():
    """Test itinerary endpoint"""
    print("\n3. Testing itinerary test endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/api/itineraries/test")
        print(f"✅ Status: {response.status_code}")
        print(f"   Response: {response.json()}")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_user_endpoints():
    """Test user endpoints exist"""
    print("\n4. Testing user endpoints...")
    try:
        # Test login endpoint (should return 422 for empty credentials)
        response = requests.post(
            f"{BASE_URL}/api/user/login",
            data={"username": "", "password": ""}
        )
        if response.status_code in [401, 422]:
            print(f"✅ Login endpoint exists (status: {response.status_code})")
            return True
        else:
            print(f"⚠️  Unexpected status: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("="*50)
    print("TRAVO Critical Endpoints Test")
    print("="*50)
    
    results = []
    results.append(("Root", test_root()))
    results.append(("Vision Identify", test_vision_identify()))
    results.append(("Itinerary", test_itinerary()))
    results.append(("User", test_user_endpoints()))
    
    print("\n" + "="*50)
    print("Test Summary:")
    print("="*50)
    for name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{name}: {status}")
    
    all_passed = all(result[1] for result in results)
    print("\n" + ("✅ ALL TESTS PASSED!" if all_passed else "❌ SOME TESTS FAILED"))
