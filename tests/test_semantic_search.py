"""Tests for the Chapter 5 engine, using a mock encoder.

`SemanticSearch` takes an `encode_fn` rather than a model precisely so this is
possible, and its module docstring says as much. These tests hold that promise
to account: nothing here downloads a model, imports a transformer, or touches
the network -- the "embeddings" are a hand-written dict of 2-D vectors, chosen
so the expected ranking can be read straight off the page.
"""

import numpy as np
import pytest

from semantic_search import SemanticSearch

# Points on the unit circle. Cosine similarity between two of them is just the
# cosine of the angle between them, so the ranking below is arithmetic rather
# than a guess: EAST is 0 degrees, NNE is 30, NORTH is 90, WEST is 180.
EAST = [1.0, 0.0]
NNE = [np.cos(np.pi / 6), np.sin(np.pi / 6)]
NORTH = [0.0, 1.0]
WEST = [-1.0, 0.0]

VECTORS = {
    "query: grass": EAST,
    "chlorophyll reflects green light": EAST,
    "photosynthesis in leaves": NNE,
    "the sky scatters blue light": NORTH,
    "a treatise on tax law": WEST,
}

DOCS = [
    {"id": 0, "title": "Chlorophyll", "text": "chlorophyll reflects green light"},
    {"id": 1, "title": "Photosynthesis", "text": "photosynthesis in leaves"},
    {"id": 2, "title": "Rayleigh scattering", "text": "the sky scatters blue light"},
    {"id": 3, "title": "Tax law", "text": "a treatise on tax law"},
]


def encode(texts):
    """A deterministic stand-in for a sentence encoder.

    Deliberately *not* normalized -- the last vector is doubled -- so that the
    engine's own `_normalize` is what makes the scores comparable. If that
    normalization were dropped, the tax-law document's larger magnitude would
    push it up the ranking and `test_magnitude_does_not_beat_direction` fails.
    """
    out = []
    for text in texts:
        vector = VECTORS[text]
        out.append([c * 2 for c in vector] if text == "a treatise on tax law" else vector)
    return np.array(out, dtype=float)


@pytest.fixture
def engine():
    return SemanticSearch(encode).index(DOCS)


def test_search_ranks_by_meaning_not_shared_words(engine):
    results = engine.search("query: grass", k=3)

    # "chlorophyll reflects green light" shares no word with the query and
    # still wins, which is the whole point of the chapter.
    assert [doc["id"] for _, _, doc in results] == [0, 1, 2]


def test_scores_are_sorted_descending(engine):
    scores = [score for _, score, _ in engine.search("query: grass", k=4)]

    assert scores == sorted(scores, reverse=True)


def test_scores_are_the_cosines_they_claim_to_be(engine):
    results = engine.search("query: grass", k=4)
    by_id = {doc["id"]: score for _, score, doc in results}

    # 0, 30, 90 and 180 degrees from the query.
    assert by_id[0] == pytest.approx(1.0)
    assert by_id[1] == pytest.approx(np.cos(np.pi / 6))
    assert by_id[2] == pytest.approx(0.0, abs=1e-12)
    assert by_id[3] == pytest.approx(-1.0)


def test_magnitude_does_not_beat_direction(engine):
    """The doubled tax-law vector must stay last.

    Without `_normalize`, its dot product with the query would be -2 rather
    than -1 -- still last here, but the same bug promotes any long document
    that points the right way. This pins that scores never leave [-1, 1].
    """
    scores = [score for _, score, _ in engine.search("query: grass", k=4)]

    assert all(-1.0 - 1e-9 <= s <= 1.0 + 1e-9 for s in scores)


def test_k_limits_the_number_of_results(engine):
    assert len(engine.search("query: grass", k=1)) == 1
    assert len(engine.search("query: grass", k=4)) == 4


def test_index_returns_self_so_it_can_be_chained():
    # The module docstring advertises `SemanticSearch(model.encode).index(...)`
    # as a single expression, so this is part of the documented interface.
    assert isinstance(SemanticSearch(encode).index(DOCS), SemanticSearch)


def test_search_before_index_raises_runtime_error():
    engine = SemanticSearch(encode)

    with pytest.raises(RuntimeError, match=r"\.index\(docs\)"):
        engine.search("query: grass")


def test_index_can_take_explicit_texts(docs=DOCS):
    """`texts=` overrides the default `d["text"]`, e.g. to index title+body."""
    engine = SemanticSearch(encode).index(
        [{"id": 9, "title": "Renamed", "body": "chlorophyll reflects green light"}],
        texts=["chlorophyll reflects green light"],
    )

    (_, score, doc) = engine.search("query: grass", k=1)[0]
    assert doc["id"] == 9
    assert score == pytest.approx(1.0)
