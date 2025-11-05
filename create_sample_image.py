from PIL import Image
import os

def create_sample_image(directory, filename, color):
    """Creates a sample 128x128 image with a solid color."""
    if not os.path.exists(directory):
        os.makedirs(directory)
    img = Image.new('RGB', (128, 128), color = color)
    img.save(os.path.join(directory, filename))

if __name__ == "__main__":
    images_dir = "travo/backend/services/vision_service/models/monuments/images"
    create_sample_image(images_dir, "eiffel-tower.jpg", "red")
    create_sample_image(images_dir, "colosseum.jpg", "green")
    create_sample_image(images_dir, "taj-mahal.jpg", "blue")
