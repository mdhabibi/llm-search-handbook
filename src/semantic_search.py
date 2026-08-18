"""A tiny, reusable semantic-search engine used from Chapter 5 onward.

Design choice: the engine takes an ``encode_fn`` (any callable mapping a list of
strings to an (n, dim) array) instead of a specific model. That keeps it decoupled
from any one library, and makes it trivial to test with a mock encoder.

Example
-------
>>> from sentence_transformers import SentenceTransformer
>>> from corpus import load_corpus
>>> model = SentenceTransformer("all-MiniLM-L6-v2")
>>> engine = SemanticSearch(model.encode).index(load_corpus())
>>> for i, score, doc in engine.search("why is grass green?", k=3):
...     print(round(score, 3), doc["title"])
"""

from __future__ import annotations

from typing import Callable, List, Dict, Tuple
import numpy as np


class SemanticSearch:
    def __init__(self, encode_fn: Callable[[List[str]], np.ndarray]):
        self.encode_fn = encode_fn
        self.docs: List[Dict] | None = None
        self.matrix: np.ndarray | None = None  # (n_docs, dim), L2-normalized

    @staticmethod
    def _normalize(mat: np.ndarray) -> np.ndarray:
        mat = np.asarray(mat, dtype=float)
        if mat.ndim == 1:
            mat = mat[None, :]
        norms = np.linalg.norm(mat, axis=1, keepdims=True)
        return mat / np.clip(norms, 1e-12, None)

    def index(self, docs: List[Dict], texts: List[str] | None = None) -> "SemanticSearch":
        """Embed every document once and store a normalized matrix (the 'index')."""
        self.docs = docs
        if texts is None:
            texts = [d["text"] for d in docs]
        self.matrix = self._normalize(self.encode_fn(texts))
        return self

    def search(self, query: str, k: int = 3) -> List[Tuple[int, float, Dict]]:
        """Return the top-k (doc_index, cosine_score, doc) for a natural-language query."""
        if self.matrix is None:
            raise RuntimeError("Call .index(docs) before searching.")
        q = self._normalize(self.encode_fn([query]))[0]
        sims = self.matrix @ q                      # cosine, since everything is normalized
        order = np.argsort(-sims)[:k]
        return [(int(i), float(sims[i]), self.docs[i]) for i in order]
