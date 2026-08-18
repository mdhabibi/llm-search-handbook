"""Document chunking strategies for Chapter 11.

Chunking = splitting a long document into smaller pieces that are embedded and
retrieved independently. The right chunk size/overlap is one of the highest-leverage
knobs in a RAG system. These are small, readable reference implementations.
"""

from __future__ import annotations

from typing import List
import re


def fixed_word_chunks(text: str, size: int = 40, overlap: int = 10) -> List[str]:
    """Split into chunks of `size` words that overlap by `overlap` words.

    Overlap keeps a sentence that straddles a boundary from being cut in half in
    *both* chunks, so context isn't lost at the seams.
    """
    if overlap >= size:
        raise ValueError("overlap must be smaller than size")
    words = text.split()
    step = size - overlap
    chunks = []
    for start in range(0, max(len(words), 1), step):
        piece = words[start:start + size]
        if piece:
            chunks.append(" ".join(piece))
        if start + size >= len(words):
            break
    return chunks


def sentence_chunks(text: str, max_sentences: int = 3, overlap_sentences: int = 1) -> List[str]:
    """Group whole sentences into chunks, overlapping by `overlap_sentences`.

    Respects sentence boundaries, so chunks read naturally (better than cutting
    mid-sentence). A very simple regex splitter is used for teaching clarity.
    """
    if overlap_sentences >= max_sentences:
        raise ValueError("overlap_sentences must be smaller than max_sentences")
    sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if s.strip()]
    step = max_sentences - overlap_sentences
    chunks = []
    for start in range(0, max(len(sentences), 1), step):
        piece = sentences[start:start + max_sentences]
        if piece:
            chunks.append(" ".join(piece))
        if start + max_sentences >= len(sentences):
            break
    return chunks
