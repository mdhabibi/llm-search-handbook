"""Tests for the from-scratch IR metrics used in Chapter 9."""

import math

import pytest

from metrics import (
    average_precision,
    dcg_at_k,
    mean_precision_at_k,
    mean_reciprocal_rank,
    ndcg_at_k,
    precision_at_k,
    recall_at_k,
    reciprocal_rank,
)

RANKED = [1, 2, 3, 4]
RELEVANT = {1, 3}


def test_precision_at_k_counts_relevant_in_topk():
    assert precision_at_k(RANKED, RELEVANT, 2) == 0.5
    assert precision_at_k(RANKED, RELEVANT, 4) == 0.5


def test_precision_at_k_zero_k_is_zero():
    assert precision_at_k(RANKED, RELEVANT, 0) == 0.0


def test_recall_at_k_fraction_of_relevant_found():
    assert recall_at_k(RANKED, RELEVANT, 2) == 0.5
    assert recall_at_k(RANKED, RELEVANT, 4) == 1.0


def test_recall_at_k_empty_relevant_is_zero():
    assert recall_at_k(RANKED, set(), 4) == 0.0


def test_reciprocal_rank_uses_first_relevant_position():
    assert reciprocal_rank([2, 1, 3], {1, 3}) == 0.5


def test_reciprocal_rank_zero_when_none_relevant():
    assert reciprocal_rank([2, 4], {1, 3}) == 0.0


def test_average_precision_averages_precision_at_hits():
    # hits at ranks 1 and 3: (1/1 + 2/3) / 2
    assert average_precision([1, 2, 3], {1, 3}) == pytest.approx((1.0 + 2 / 3) / 2)


def test_dcg_uses_log2_discount():
    assert dcg_at_k([1, 2], {1}, 2) == pytest.approx(1.0)
    assert dcg_at_k([2, 1], {1}, 2) == pytest.approx(1 / math.log2(3))


def test_ndcg_is_one_for_ideal_ranking_and_normalized_otherwise():
    assert ndcg_at_k([1, 2], {1}, 2) == pytest.approx(1.0)
    assert ndcg_at_k([2, 1], {1}, 2) == pytest.approx(1 / math.log2(3))


def test_ndcg_zero_when_no_relevant():
    assert ndcg_at_k([1, 2], set(), 2) == 0.0


def test_mean_helpers_average_over_queries():
    assert mean_reciprocal_rank([[1], [2]], [{1}, {1}]) == pytest.approx(0.5)


def test_mean_helpers_empty_input_is_zero():
    assert mean_precision_at_k([], [], 5) == 0.0
