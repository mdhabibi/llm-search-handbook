"""Tests for the shared corpus loader and tokenizer."""

from corpus import load_corpus, tokenize


def test_tokenize_lowercases_and_splits_on_non_letters():
    assert tokenize("Hello, WORLD! foo123bar") == ["hello", "world", "foo", "bar"]


def test_tokenize_removes_stopwords_when_asked():
    assert tokenize("The cat and a dog", remove_stopwords=True) == ["cat", "dog"]


def test_load_corpus_returns_documents_with_expected_keys():
    docs = load_corpus()
    assert len(docs) > 0
    assert {"id", "title", "text"} <= set(docs[0].keys())
