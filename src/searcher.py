import numpy as np
from typing import List
from src.indexer import DocumentIndex
from src.utils import preprocess


def cosine_similarity(vec1: np.ndarray, vec2: np.ndarray) -> float:
    dot = np.dot(vec1, vec2)
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)

    if norm1 == 0 or norm2 == 0:
        return 0.0

    return dot / (norm1 * norm2)


def query_to_vector(query: str, vocab: List[str], idf: np.ndarray) -> np.ndarray:
    tokens = preprocess(query)
    tf = np.zeros(len(vocab))

    token_counts = {word: tokens.count(word) for word in tokens}
    total_tokens = len(tokens)

    for i, word in enumerate(vocab):
        if total_tokens > 0:
            tf[i] = token_counts.get(word, 0) / total_tokens

    tfidf = tf * idf
    return tfidf


def search(query: str, index: DocumentIndex, top_k=3):
    vocab = index.vocab
    idf = index.idf
    tfidf_matrix = index.tfidf_matrix
    docs = index.documents
    filenames = index.filenames

    query_vec = query_to_vector(query, vocab, idf)

    if not np.any(query_vec):
        return []

    scores = []

    for i, doc_vec in enumerate(tfidf_matrix):
        score = cosine_similarity(query_vec, doc_vec) 
        scores.append((i, score))

    # Sort by score descending
    scores = sorted(scores, key=lambda x: x[1], reverse=True)

    results = []

    for idx, score in scores[:top_k]:
        snippet = docs[idx][:200]  # first 200 chars
        #snippet = " ".join(docs[idx].split()[:40])

        results.append({    
            "document": filenames[idx],
            "score": round(float(score), 4),
            "snippet": snippet
        })

    return results