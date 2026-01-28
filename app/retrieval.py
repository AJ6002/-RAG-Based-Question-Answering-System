import numpy as np
import faiss
from app.embeddings import embed_texts
from app.vector_store import load_index

TOP_K = 5
CONFIDENCE_THRESHOLD = 0.25

def retrieve(query: str):
    index, metadata = load_index()

    if index is None or len(metadata) == 0:
        return [], 0.0

    query_embedding = embed_texts([query])[0]
    query_embedding = np.array([query_embedding], dtype="float32")

    distances, indices = index.search(query_embedding, TOP_K)

    results = []
    similarities = []

    for dist, idx in zip(distances[0], indices[0]):
        if idx == -1:
            continue

        similarity = 1 / (1 + dist)
        similarities.append(similarity)

        results.append({
            "text": metadata[idx]["text"],
            "source": metadata[idx]["source"],
            "chunk_id": metadata[idx]["chunk_id"],
            "similarity": similarity
        })

    max_similarity = max(similarities) if similarities else 0.0

    if max_similarity < CONFIDENCE_THRESHOLD:
        return [], max_similarity

    return results, max_similarity
