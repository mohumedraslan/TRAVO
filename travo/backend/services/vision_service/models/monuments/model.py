import os
import pickle
from PIL import Image
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class MonumentIdentifier:
    def __init__(self):
        self.model = SentenceTransformer('clip-ViT-B-32')
        self.embeddings_path = os.path.join(os.path.dirname(__file__), 'embeddings.pkl')
        self.monument_embeddings = self._load_embeddings()

    def _load_embeddings(self):
        with open(self.embeddings_path, 'rb') as f:
            return pickle.load(f)

    def identify(self, image: Image.Image):
        """
        Identifies a monument in an image by comparing its embedding with
        pre-computed embeddings of known monuments.
        """
        if not self.monument_embeddings:
            return None

        # Compute the embedding for the input image
        image_embedding = self.model.encode(image)

        # Compare with the stored embeddings
        monument_ids = list(self.monument_embeddings.keys())
        stored_embeddings = np.array(list(self.monument_embeddings.values()))

        # Calculate cosine similarities
        similarities = cosine_similarity([image_embedding], stored_embeddings)[0]

        # Find the best match
        best_match_index = np.argmax(similarities)
        best_match_score = similarities[best_match_index]
        best_match_id = monument_ids[best_match_index]

        return {
            "monument_id": best_match_id,
            "confidence": float(best_match_score)
        }
