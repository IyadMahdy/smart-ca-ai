import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

from src.config import FAISS_INDEX_PATH, LAW_METADATA_PATH, EMBED_MODEL_NAME
from src.text_normalization import normalize_arabic_text
from pathlib import Path


LAW_TEXTS_PATH = Path("data/law/egypt_labor_law_texts.json")


class LawRetriever:
    def __init__(self):
        self.embedder = SentenceTransformer(EMBED_MODEL_NAME)

        self.index = faiss.read_index(str(FAISS_INDEX_PATH))

        with open(LAW_METADATA_PATH, "r", encoding="utf-8") as f:
            self.metadatas = json.load(f)

        with open(LAW_TEXTS_PATH, "r", encoding="utf-8") as f:
            self.texts = json.load(f)

        assert len(self.metadatas) == len(self.texts)

    def search(self, text: str, k=5):
        text = normalize_arabic_text(text)

        emb = self.embedder.encode([text], normalize_embeddings=True).astype("float32")

        D, I = self.index.search(emb, k)

        results = []
        for score, idx in zip(D[0], I[0]):
            r = self.metadatas[idx].copy()
            r["score"] = float(score)
            r["text"] = self.texts[idx]
            results.append(r)

        return results
