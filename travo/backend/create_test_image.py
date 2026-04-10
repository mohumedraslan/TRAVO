#!/usr/bin/env python3
"""
Create a simple test image for testing monument identification.
This creates a simple geometric pattern that can be used for testing.
"""

from PIL import Image, ImageDraw
import numpy as np

def create_test_image():
    # Create a 512x512 image with a simple pyramid-like pattern
    img = Image.new('RGB', (512, 512), color='white')
    draw = ImageDraw.Draw(img)
    
    # Draw a simple pyramid shape (triangle)
    # This represents a monument-like structure
    points = [(256, 100), (156, 400), (356, 400)]
    draw.polygon(points, fill='beige', outline='brown')
    
    # Add some details to make it look more like a monument
    # Draw a small triangle on top (pyramidion)
    top_points = [(256, 100), (236, 150), (276, 150)]
    draw.polygon(top_points, fill='gold', outline='brown')
    
    # Add some texture lines
    for i in range(5):
        y = 150 + i * 50
        x1 = 156 + (i * 25)
        x2 = 356 - (i * 25)
        draw.line([(x1, y), (x2, y)], fill='brown', width=2)
    
    # Add a sky background
    draw.rectangle([0, 0, 512, 80], fill='lightblue')
    
    # Add a sun
    draw.ellipse([420, 30, 480, 90], fill='yellow', outline='orange')
    
    return img

if __name__ == "__main__":
    test_img = create_test_image()
    test_img.save('tests/test_images/pyramids.jpg', 'JPEG', quality=95)
    print("Test image created at tests/test_images/pyramids.jpg")