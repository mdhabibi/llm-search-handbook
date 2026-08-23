"""Tests for the chunking strategies used in Chapter 11."""

import pytest

from chunking import fixed_word_chunks, sentence_chunks


def test_fixed_word_chunks_respects_size_and_overlap():
    text = " ".join(str(i) for i in range(10))  # 10 words: "0" .. "9"
    chunks = fixed_word_chunks(text, size=4, overlap=1)  # step = 3
    assert chunks == ["0 1 2 3", "3 4 5 6", "6 7 8 9"]


def test_fixed_word_chunks_empty_text_returns_empty():
    assert fixed_word_chunks("", size=4, overlap=1) == []


def test_fixed_word_chunks_overlap_not_smaller_than_size_raises():
    with pytest.raises(ValueError):
        fixed_word_chunks("a b c", size=2, overlap=2)


def test_sentence_chunks_groups_and_overlaps_sentences():
    text = "A. B. C. D."
    chunks = sentence_chunks(text, max_sentences=2, overlap_sentences=1)  # step = 1
    assert chunks == ["A. B.", "B. C.", "C. D."]


def test_sentence_chunks_overlap_not_smaller_than_max_raises():
    with pytest.raises(ValueError):
        sentence_chunks("A. B.", max_sentences=2, overlap_sentences=2)
