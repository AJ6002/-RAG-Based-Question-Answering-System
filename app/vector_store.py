import faiss
import pickle
import os
from typing import List, Dict, Tuple

VECTOR_DIR = "data/faiss_index"
INDEX_PATH = os.path.join(VECTOR_DIR, "index.faiss")
META_PATH = os.path.join(VECTOR_DIR, "meta.pkl")


def save_index(index: faiss.Index, metadata: List[Dict]):
    os.makedirs(VECTOR_DIR, exist_ok=True)
    faiss.write_index(index, INDEX_PATH)
    with open(META_PATH, "wb") as f:
        pickle.dump(metadata, f)


def load_index() -> Tuple[faiss.Index, List[Dict]]:
    if not os.path.exists(INDEX_PATH) or not os.path.exists(META_PATH):
        return None, []

    index = faiss.read_index(INDEX_PATH)
    with open(META_PATH, "rb") as f:
        metadata = pickle.load(f)

    return index, metadata
