import requests
import base64
import io
from PIL import Image

# Create a valid image using PIL
img = Image.new('RGB', (100, 100), color = 'red')
img_byte_arr = io.BytesIO()
img.save(img_byte_arr, format='PNG')
img_byte_arr = img_byte_arr.getvalue()

b64_image = base64.b64encode(img_byte_arr).decode('utf-8')

url = "http://localhost:8001/api/vision/identify"
payload = {
    "image": b64_image
}
headers = {
    "Content-Type": "application/json"
}

print(f"Sending request to {url}...")
try:
    response = requests.post(url, json=payload, headers=headers, timeout=30)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text[:500]}") # Print first 500 chars
except Exception as e:
    print(f"Error: {e}")
