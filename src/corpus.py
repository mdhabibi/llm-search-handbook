"""Shared helpers for loading the course's sample corpus and basic text tools.

Kept intentionally small and readable — this is a teaching repo. Notebooks import
from here so we don't repeat boilerplate.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import List, Dict

# Resolve the data file relative to the repo root, regardless of where a notebook runs.
_REPO_ROOT = Path(__file__).resolve().parents[1]
_CORPUS_PATH = _REPO_ROOT / "data" / "sample_corpus.json"


def load_corpus(path: str | Path | None = None) -> List[Dict]:
    """Return the list of document dicts: {"id", "title", "text"}."""
    p = Path(path) if path else _CORPUS_PATH
    with open(p, "r", encoding="utf-8") as f:
        return json.load(f)["documents"]


# A minimal English stop-word list. Real systems use larger, curated lists (e.g. from
# NLTK); we keep a tiny one so the behavior is easy to inspect in a lesson.
STOP_WORDS = {
    "a", "an", "and", "are", "as", "at", "be", "by", "for", "from", "in", "into",
    "is", "it", "its", "of", "on", "or", "that", "the", "to", "was", "were",
    "what", "when", "where", "which", "who", "why", "with",
}


def tokenize(text: str, remove_stopwords: bool = False) -> List[str]:
    """Lowercase, split on non-letters, optionally drop stop words.

    This is a deliberately simple tokenizer so learners can see exactly what it does.
    """
    tokens = re.findall(r"[a-z]+", text.lower())
    if remove_stopwords:
        tokens = [t for t in tokens if t not in STOP_WORDS]
    return tokens


if __name__ == "__main__":
    docs = load_corpus()
    print(f"Loaded {len(docs)} documents.")
    print("Example:", docs[0]["title"], "->", tokenize(docs[0]["text"])[:8], "...")
