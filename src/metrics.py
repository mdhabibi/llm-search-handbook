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
    """Fraction of the top-k results that are relevant.

    Ranks 1 and 3 are relevant, so one of the first two results is a hit:

    >>> precision_at_k([1, 2, 3, 4], {1, 3}, 2)
    0.5

    The denominator is k, not the number of results, so precision falls as k
    grows past the relevant documents:

    >>> precision_at_k([1, 2, 3, 4], {1, 3}, 4)
    0.5
    >>> precision_at_k([1, 2, 3, 4], {1, 3}, 0)
    0.0
    """
    if k <= 0:
        return 0.0
    topk = ranked_ids[:k]
    hits = sum(1 for d in topk if d in relevant)
    return hits / k


def recall_at_k(ranked_ids: List[int], relevant: Set[int], k: int) -> float:
    """Fraction of all relevant documents found within the top-k.

    Here the denominator is how many relevant documents exist, so recall rises
    with k and reaches 1.0 once all of them are inside the cutoff:

    >>> recall_at_k([1, 2, 3, 4], {1, 3}, 2)
    0.5
    >>> recall_at_k([1, 2, 3, 4], {1, 3}, 4)
    1.0

    With nothing judged relevant, recall is undefined; this returns 0.0:

    >>> recall_at_k([1, 2], set(), 2)
    0.0
    """
    if not relevant:
        return 0.0
    topk = ranked_ids[:k]
    hits = sum(1 for d in topk if d in relevant)
    return hits / len(relevant)


def reciprocal_rank(ranked_ids: List[int], relevant: Set[int]) -> float:
    """1 / rank of the first relevant result (0 if none found).

    Only the first hit counts, and ranks are 1-based -- a relevant document in
    second place scores 1/2:

    >>> reciprocal_rank([5, 3, 1], {1, 3})
    0.5
    >>> reciprocal_rank([3, 5, 1], {1, 3})
    1.0
    >>> reciprocal_rank([5, 6], {1, 3})
    0.0
    """
    for rank, d in enumerate(ranked_ids, start=1):
        if d in relevant:
            return 1.0 / rank
    return 0.0


def average_precision(ranked_ids: List[int], relevant: Set[int]) -> float:
    """Average of precision@k taken at each rank where a relevant doc appears.

    For [1, 2, 3, 4] with {1, 3} relevant, hits land at ranks 1 and 3, giving
    precisions of 1/1 and 2/3; their mean over the two relevant documents is
    (1 + 2/3) / 2:

    >>> round(average_precision([1, 2, 3, 4], {1, 3}), 4)
    0.8333

    Ranking both hits first scores a perfect 1.0, which is what makes this
    sensitive to order in a way precision@k is not:

    >>> average_precision([1, 3, 2, 4], {1, 3})
    1.0
    """
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
    """Discounted Cumulative Gain with binary gains and log2 discount.

    A hit at rank 1 contributes 1/log2(2) = 1.0 and a hit at rank 3
    contributes 1/log2(4) = 0.5:

    >>> dcg_at_k([1, 2, 3], {1, 3}, 3)
    1.5

    Moving the second hit up to rank 2 is worth more, since 1/log2(3) > 0.5 --
    the discount is what makes DCG care about order:

    >>> round(dcg_at_k([1, 3, 2], {1, 3}, 3), 4)
    1.6309
    """
    dcg = 0.0
    for i, d in enumerate(ranked_ids[:k]):
        gain = 1.0 if d in relevant else 0.0
        dcg += gain / math.log2(i + 2)     # position i is 0-based -> rank i+1 -> log2(rank+1)
    return dcg


def ndcg_at_k(ranked_ids: List[int], relevant: Set[int], k: int) -> float:
    """Normalized DCG: DCG divided by the best possible DCG (ideal ranking).

    Dividing by the ideal ranking's DCG puts the score on a 0-1 scale, so a
    perfect ranking is exactly 1.0 whatever k is:

    >>> ndcg_at_k([1, 3, 2], {1, 3}, 3)
    1.0

    The same DCG of 1.5 from the example above is only 0.92 of what the ideal
    ranking would have scored:

    >>> round(ndcg_at_k([1, 2, 3], {1, 3}, 3), 4)
    0.9197

    >>> ndcg_at_k([1, 2], set(), 2)
    0.0
    """
    dcg = dcg_at_k(ranked_ids, relevant, k)
    ideal = dcg_at_k(list(relevant), relevant, k)   # all relevant docs up front
    return dcg / ideal if ideal > 0 else 0.0


# ---- averaging over many queries -------------------------------------------------

def mean_reciprocal_rank(rankings: Sequence[List[int]], relevants: Sequence[Set[int]]) -> float:
    """Mean of reciprocal_rank over one ranking per query.

    First query hits at rank 1, second at rank 2, so (1 + 1/2) / 2:

    >>> mean_reciprocal_rank([[1, 2], [2, 1]], [{1}, {1}])
    0.75

    >>> mean_reciprocal_rank([], [])
    0.0
    """
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
