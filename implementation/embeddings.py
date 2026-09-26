"""Injectable embedding boundary; no import-time downloads."""
from config import EMBEDDING_MODEL


class SentenceEncoder:
    def __init__(self):
        from sentence_transformers import SentenceTransformer
        self.model = SentenceTransformer(EMBEDDING_MODEL)

    def encode(self, text):
        return self.model.encode(text, normalize_embeddings=True).tolist()
