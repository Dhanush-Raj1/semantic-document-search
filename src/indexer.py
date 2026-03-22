import os
import numpy as np
from typing import List, Tuple
from collections import Counter
from math import log
from src.utils import preprocess


def load_documents(doc_path="documents") -> Tuple[List[str], List[str]]:
    docs = []
    filenames = []

    for file in sorted(os.listdir(doc_path)):
        if file.endswith(".txt"):
            with open(os.path.join(doc_path, file), "r", encoding="utf-8") as f:
                text = f.read()
                docs.append(text)
                filenames.append(file)

    return docs, filenames


def build_vocab(tokenized_docs: List[List[str]]) -> List[str]:
    vocab = set()

    for tokens in tokenized_docs:
        vocab.update(tokens)

    return sorted(vocab)


def compute_tf(tokens: List[str], vocab: List[str]) -> np.ndarray:
    tf = np.zeros(len(vocab))
    token_counts = Counter(tokens)   
    total_tokens = len(tokens)

    if total_tokens == 0:      
        return tf 

    for i, word in enumerate(vocab):
        tf[i] = token_counts[word] / total_tokens

    return tf


def compute_idf(tokenized_docs: List[List[str]], vocab: List[str]) -> np.ndarray:
    N = len(tokenized_docs)
    idf = np.zeros(len(vocab))

    for i, word in enumerate(vocab):
        df = sum(1 for doc in tokenized_docs if word in doc)
        idf[i] = log((N + 1) / (df + 1)) + 1  # smoothing, prevents division by zero

    return idf


def build_tfidf(tokenized_docs: List[List[str]], vocab: List[str]) -> Tuple[np.ndarray, np.ndarray]:
    tf_matrix = []

    for tokens in tokenized_docs:
        tf = compute_tf(tokens, vocab)
        tf_matrix.append(tf)

    tf_matrix = np.array(tf_matrix)
    idf = compute_idf(tokenized_docs, vocab)

    tfidf = tf_matrix * idf

    return tfidf, idf



class DocumentIndex:
    def __init__(self, doc_path: str = "documents"):
        self.doc_path = doc_path
        self.documents: List[str] = []
        self.filenames: List[str] = []
        self.vocab: List[str] = []
        self.idf: np.ndarray = np.array([])
        self.tfidf_matrix: np.ndarray = np.array([])

    def build(self) -> None:
        docs, filenames = load_documents(self.doc_path)
        tokenized_docs = [preprocess(doc) for doc in docs]
        vocab = build_vocab(tokenized_docs)
        tfidf_matrix, idf = build_tfidf(tokenized_docs, vocab)

        self.documents = docs
        self.filenames = filenames
        self.vocab = vocab
        self.idf = idf
        self.tfidf_matrix = tfidf_matrix