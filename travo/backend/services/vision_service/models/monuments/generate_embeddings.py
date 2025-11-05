import os
import json
import pickle
from PIL import Image
from sentence_transformers import SentenceTransformer

def generate_embeddings():
    """Generates and saves embeddings for the monument reference images."""
    model = SentenceTransformer('clip-ViT-B-32')

    base_dir = os.path.dirname(__file__)
    images_dir = os.path.join(base_dir, 'images')
    labels_path = os.path.join(base_dir, 'labels.json')
    embeddings_path = os.path.join(base_dir, 'embeddings.pkl')

    with open(labels_path, 'r') as f:
        labels_data = json.load(f)

    embeddings = {}
    for monument in labels_data.get('monuments', []):
        monument_id = monument.get('id')
        image_filename = f"{monument_id}.jpg"
        image_path = os.path.join(images_dir, image_filename)

        if os.path.exists(image_path):
            image = Image.open(image_path)
            embedding = model.encode(image)
            embeddings[monument_id] = embedding
            print(f"Generated embedding for {monument_id}")

    with open(embeddings_path, 'wb') as f:
        pickle.dump(embeddings, f)

    print(f"Embeddings saved to {embeddings_path}")


if __name__ == "__main__":
    generate_embeddings()
