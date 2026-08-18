"""Information-retrieval evaluation metrics, implemented from scratch for teaching.

Every function takes:
  ranked_ids : list[int]   document ids returned by a retriever, best first
  relevant   : set[int]    the ids judged relevant for this query (binary relevance)

and (where relevant) a cutoff k. Averaging helpers operate over many queries.

These are intentionally simple and readable — no external IR library — so the math in
Chapter 9 is fully transparent.
"""

from __future__ import annotations

from typing import List, Set, Sequence, Dict
import math


def precision_at_k(ranked_ids: List[int], relevant: Set[int], k: int) -> float:
    """Fraction of the top-k results that are relevant."""
    if k <= 0:
        return 0.0
    topk = ranked_ids[:k]
    hits = sum(1 for d in topk if d in relevant)
    return hits / k


def recall_at_k(ranked_ids: List[int], relevant: Set[int], k: int) -> float:
    """Fraction of all relevant documents found within the top-k."""
    if not relevant:
        return 0.0
    topk = ranked_ids[:k]
    hits = sum(1 for d in topk if d in relevant)
    return hits / len(relevant)


def reciprocal_rank(ranked_ids: List[int], relevant: Set[int]) -> float:
    """1 / rank of the first relevant result (0 if none found)."""
    for rank, d in enumerate(ranked_ids, start=1):
        if d in relevant:
            return 1.0 / rank
    return 0.0


def average_precision(ranked_ids: List[int], relevant: Set[int]) -> float:
    """Average of precision@k taken at each rank where a relevant doc appears."""
    if not relevant:
        return 0.0
    hits = 0
    score = 0.0
    for rank, d in enumerate(ranked_ids, start=1):
        if d in relevant:
            hits += 1
            score += hits / rank          # precision at this hit's position
    return score / len(relevant)


def dcg_at_k(ranked_ids: List[int], relevant: Set[int], k: int) -> float:
    """Discounted Cumulative Gain with binary gains and log2 discount."""
    dcg = 0.0
    for i, d in enumerate(ranked_ids[:k]):
        gain = 1.0 if d in relevant else 0.0
        dcg += gain / math.log2(i + 2)     # position i is 0-based -> rank i+1 -> log2(rank+1)
    return dcg


def ndcg_at_k(ranked_ids: List[int], relevant: Set[int], k: int) -> float:
    """Normalized DCG: DCG divided by the best possible DCG (ideal ranking)."""
    dcg = dcg_at_k(ranked_ids, relevant, k)
    ideal = dcg_at_k(list(relevant), relevant, k)   # all relevant docs up front
    return dcg / ideal if ideal > 0 else 0.0


# ---- averaging over many queries -------------------------------------------------

def mean_reciprocal_rank(rankings: Sequence[List[int]], relevants: Sequence[Set[int]]) -> float:
    return _mean(reciprocal_rank(r, rel) for r, rel in zip(rankings, relevants))


def mean_average_precision(rankings: Sequence[List[int]], relevants: Sequence[Set[int]]) -> float:
    return _mean(average_precision(r, rel) for r, rel in zip(rankings, relevants))


def mean_ndcg_at_k(rankings: Sequence[List[int]], relevants: Sequence[Set[int]], k: int) -> float:
    return _mean(ndcg_at_k(r, rel, k) for r, rel in zip(rankings, relevants))


def mean_precision_at_k(rankings: Sequence[List[int]], relevants: Sequence[Set[int]], k: int) -> float:
    return _mean(precision_at_k(r, rel, k) for r, rel in zip(rankings, relevants))


def mean_recall_at_k(rankings: Sequence[List[int]], relevants: Sequence[Set[int]], k: int) -> float:
    return _mean(recall_at_k(r, rel, k) for r, rel in zip(rankings, relevants))


def _mean(values) -> float:
    vals = list(values)
    return sum(vals) / len(vals) if vals else 0.0
