import requests

import requests
import os

url = "http://localhost:8000/api/vision/identify"

# Get the absolute path to the image
image_path = os.path.abspath(os.path.join("tests", "test_images", "pyramids.jpg"))
print(f"Attempting to open: {image_path}")


try:
    with open(image_path, "rb") as f:
        files = {"image": f}
        response = requests.post(url, files=files)

    print(f"Status Code: {response.status_code}")
    print("Response Text:")
    print(response.text)

except FileNotFoundError:
    print(f"Error: Image file not found at {image_path}")
except requests.exceptions.RequestException as e:
    print(f"Request failed: {e}")