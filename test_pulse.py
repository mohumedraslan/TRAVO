import requests
import time

# Create a small dummy image (1x1 pixel black jpeg)
# minimal jpeg header
dummy_jpeg = b'\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x01\x00`\x00`\x00\x00\xff\xdb\x00C\x00\x08\x06\x06\x07\x06\x05\x08\x07\x07\x07\t\t\x08\n\x0c\x14\r\x0c\x0b\x0b\x0c\x19\x12\x13\x0f\x14\x1d\x1a\x1f\x1e\x1d\x1a\x1c\x1c $.\' ",#\x1c\x1c(7),01444\x1f\'9=82<.342\xff\xc0\x00\x0b\x08\x00\x01\x00\x01\x01\x01\x11\x00\xff\xc4\x00\x1f\x00\x00\x01\x05\x01\x01\x01\x01\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\xff\xda\x00\x08\x01\x01\x00\x00\x00?\x00\xbf\x00\xff\xd9'

url = "http://127.0.0.1:8000/api/live/pulse"

print(f"Testing Pulse API at {url}...")
try:
    files = {"image": ("test.jpg", dummy_jpeg, "image/jpeg")}
    data = {"lat": 30.0444, "lon": 31.2357} # Cairo dummy coords
    
    start = time.time()
    response = requests.post(url, files=files, data=data)
    duration = time.time() - start
    
    print(f"Status: {response.status_code}")
    print(f"Time: {duration:.2f}s")
    print(f"Response: {response.text}")
    
except Exception as e:
    print(f"Failed: {e}")
