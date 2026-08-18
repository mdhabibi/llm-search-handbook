"""SearchStack — the Chapter 13 capstone: the whole course in one class.

Wires together chunking (Ch11), BM25 keyword search (Ch2), dense retrieval (Ch5),
Reciprocal Rank Fusion hybrid (Ch8), optional cross-encoder re-ranking (Ch7),
optional grounded RAG generation (Ch10), and evaluation metrics (Ch9).

It is deliberately dependency-light: you pass in
  - ``encode_fn``  : list[str] -> (n, dim) array   (e.g. SentenceTransformer.encode)
  - ``reranker``   : optional obj with .predict(list[(q, doc)]) -> scores
  - ``generator``  : optional callable(prompt) -> str
so the whole thing can be driven by real models *or* mocks (for testing/learning).
"""

from __future__ import annotations

from typing import Callable, List, Dict, Optional
from collections import Counter, defaultdict
import math
import numpy as np

from corpus import tokenize
from chunking import sentence_chunks
import metrics as M


class SearchStack:
    def __init__(
        self,
        encode_fn: Callable[[List[str]], np.ndarray],
        chunker: Callable[[str], List[str]] = lambda t: sentence_chunks(t, 3, 1),
        reranker=None,
        generator: Optional[Callable[[str], str]] = None,
        use_hybrid: bool = True,
    ):
        self.encode_fn = encode_fn
        self.chunker = chunker
        self.reranker = reranker
        self.generator = generator
        self.use_hybrid = use_hybrid
        # populated by ingest()
        self.chunks: List[str] = []
        self.meta: List[Dict] = []
        self.matrix: Optional[np.ndarray] = None
        self._tok: List[List[str]] = []
        self._df = defaultdict(int)
        self._avgdl = 0.0

    # ---- ingestion (Ch11) -----------------------------------------------------
    def ingest(self, docs: List[Dict]) -> "SearchStack":
        for d in docs:
            for pos, ch in enumerate(self.chunker(d["text"])):
                self.chunks.append(ch)
                self.meta.append({"doc_id": d["id"], "title": d["title"], "pos": pos})
        # dense index
        mat = np.asarray(self.encode_fn(self.chunks), dtype=float)
        self.matrix = mat / np.clip(np.linalg.norm(mat, axis=1, keepdims=True), 1e-12, None)
        # bm25 index
        self._tok = [tokenize(c) for c in self.chunks]
        self._avgdl = sum(len(t) for t in self._tok) / len(self._tok)
        self._df = defaultdict(int)
        for t in self._tok:
            for term in set(t):
                self._df[term] += 1
        return self

    # ---- retrievers (Ch2, Ch5) -----------------------------------------------
    def _idf(self, term: str) -> float:
        n = len(self._tok)
        return math.log(1 + (n - self._df[term] + 0.5) / (self._df[term] + 0.5))

    def _bm25_rank(self, query: str, k: int, k1=1.5, b=0.75) -> List[int]:
        q = tokenize(query)
        scores = []
        for i, t in enumerate(self._tok):
            f = Counter(t)
            s = 0.0
            for term in q:
                if term in f:
                    s += self._idf(term) * (f[term] * (k1 + 1)) / (
                        f[term] + k1 * (1 - b + b * len(t) / self._avgdl)
                    )
            scores.append((i, s))
        return [i for i, _ in sorted(scores, key=lambda x: -x[1])][:k]

    def _dense_rank(self, query: str, k: int) -> List[int]:
        q = np.asarray(self.encode_fn([query]), dtype=float)[0]
        q = q / (np.linalg.norm(q) + 1e-12)
        return list(np.argsort(-(self.matrix @ q))[:k])

    @staticmethod
    def _rrf(rankings: List[List[int]], k: int = 60) -> List[int]:
        scores: Dict[int, float] = {}
        for r in rankings:
            for rank, i in enumerate(r, start=1):
                scores[i] = scores.get(i, 0.0) + 1.0 / (k + rank)
        return sorted(scores, key=lambda i: -scores[i])

    # ---- public search / answer / evaluate -----------------------------------
    def retrieve(self, query: str, k: int = 5, candidate_k: int = 20) -> List[int]:
        """Return chunk indices, best first (hybrid + optional re-rank)."""
        if self.use_hybrid:
            cand = self._rrf([self._bm25_rank(query, candidate_k),
                              self._dense_rank(query, candidate_k)])
        else:
            cand = self._dense_rank(query, candidate_k)
        cand = cand[:candidate_k]
        if self.reranker is not None and cand:
            scores = self.reranker.predict([(query, self.chunks[i]) for i in cand])
            cand = [i for i, _ in sorted(zip(cand, scores), key=lambda x: -x[1])]
        return cand[:k]

    def search(self, query: str, k: int = 5) -> List[Dict]:
        return [{"chunk": self.chunks[i], **self.meta[i]} for i in self.retrieve(query, k)]

    def answer(self, query: str, k: int = 3) -> Dict:
        hits = self.retrieve(query, k)
        passages = [(self.meta[i]["doc_id"], self.chunks[i]) for i in hits]
        context = "\n".join(f"[{doc_id}] {text}" for doc_id, text in passages)
        prompt = (
            "Answer the QUESTION using ONLY the CONTEXT below.\n"
            'If the context does not contain the answer, say "I don\'t know based on the '
            'provided context."\nCite the passages you used by their [id].\n\n'
            f"CONTEXT:\n{context}\n\nQUESTION: {query}\n\nANSWER:"
        )
        if self.generator is None:
            return {"prompt": prompt, "answer": None, "citations": [d for d, _ in passages]}
        return {"prompt": prompt, "answer": self.generator(prompt),
                "citations": [d for d, _ in passages]}

    def evaluate(self, eval_set: List[Dict], k: int = 10) -> Dict[str, float]:
        """Score against doc-id relevance judgments (chunks map back to their doc_id)."""
        rankings, rels = [], []
        for q in eval_set:
            chunk_ids = self.retrieve(q["query"], k=k, candidate_k=max(k, 20))
            # collapse chunks to unique doc_ids, preserving order
            seen, doc_ranking = set(), []
            for ci in chunk_ids:
                did = self.meta[ci]["doc_id"]
                if did not in seen:
                    seen.add(did)
                    doc_ranking.append(did)
            rankings.append(doc_ranking)
            rels.append(set(q["relevant_ids"]))
        return {
            "nDCG@10": M.mean_ndcg_at_k(rankings, rels, k),
            "MRR": M.mean_reciprocal_rank(rankings, rels),
            "MAP": M.mean_average_precision(rankings, rels),
            "recall@10": M.mean_recall_at_k(rankings, rels, k),
        }
