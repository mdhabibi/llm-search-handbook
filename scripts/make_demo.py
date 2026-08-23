#!/usr/bin/env python3
"""Generate the README demo image: keyword (BM25) vs semantic search on the real
sample corpus, using the actual `src/` engines. Output: assets/demo.png

Run once to (re)generate:  python scripts/make_demo.py
Needs: sentence-transformers, rank-bm25, matplotlib (all in requirements.txt).
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from corpus import load_corpus, tokenize  # noqa: E402
from semantic_search import SemanticSearch  # noqa: E402

QUERY = "what can I take for a pounding head?"
RELEVANT = {2, 3}  # Migraine symptoms, Treating a headache
K = 4

BLUE = "#2563EB"
GREEN = "#16A34A"
GREY = "#94A3B8"
INK = "#0F172A"
PANEL = "#F8FAFC"


def keyword_results(docs, query, k):
    from rank_bm25 import BM25Okapi

    tokenized = [tokenize(f"{d['title']} {d['text']}") for d in docs]
    bm25 = BM25Okapi(tokenized)
    scores = bm25.get_scores(tokenize(query))
    order = sorted(range(len(docs)), key=lambda i: -scores[i])[:k]
    top = max(scores) or 1.0
    return [(i, scores[i] / top, docs[i]) for i in order]


def semantic_results(docs, query, k):
    from sentence_transformers import SentenceTransformer

    model = SentenceTransformer("all-MiniLM-L6-v2")
    engine = SemanticSearch(model.encode).index(
        docs, texts=[f"{d['title']}. {d['text']}" for d in docs]
    )
    return engine.search(query, k=k)


def draw_panel(ax, x0, title, subtitle, results):
    w = 0.44
    ax.add_patch(
        FancyBboxPatch(
            (x0, 0.06), w, 0.72, boxstyle="round,pad=0.012,rounding_size=0.02",
            linewidth=0, facecolor=PANEL, transform=ax.transAxes,
        )
    )
    ax.text(x0 + 0.03, 0.72, title, transform=ax.transAxes, fontsize=15,
            fontweight="bold", color=INK)
    ax.text(x0 + 0.03, 0.685, subtitle, transform=ax.transAxes, fontsize=9.5,
            color=GREY)
    y = 0.60
    for rank, (idx, score, doc) in enumerate(results, 1):
        hit = idx in RELEVANT
        mark, mcol = ("✓", GREEN) if hit else ("✗", GREY)
        ax.text(x0 + 0.03, y, mark, transform=ax.transAxes, fontsize=13,
                fontweight="bold", color=mcol)
        ax.text(x0 + 0.065, y, doc["title"], transform=ax.transAxes, fontsize=12,
                color=INK if hit else "#64748B",
                fontweight="bold" if hit else "normal")
        bar_x, bar_w = x0 + 0.065, 0.34
        ax.add_patch(plt.Rectangle((bar_x, y - 0.045), bar_w, 0.016,
                     transform=ax.transAxes, facecolor="#E2E8F0", linewidth=0))
        ax.add_patch(plt.Rectangle((bar_x, y - 0.045), bar_w * max(score, 0.02),
                     0.016, transform=ax.transAxes,
                     facecolor=GREEN if hit else GREY, linewidth=0))
        ax.text(bar_x + bar_w + 0.01, y - 0.045, f"{score:0.2f}",
                transform=ax.transAxes, fontsize=8.5, color=GREY)
        y -= 0.135


def main():
    docs = load_corpus()
    kw = keyword_results(docs, QUERY, K)
    sem = semantic_results(docs, QUERY, K)

    fig, ax = plt.subplots(figsize=(11, 5.2))
    ax.axis("off")
    fig.patch.set_facecolor("white")

    ax.text(0.5, 0.94, "Search Semantically", transform=ax.transAxes,
            ha="center", fontsize=13, color=BLUE, fontweight="bold")
    ax.text(0.5, 0.87, f'Query:  "{QUERY}"', transform=ax.transAxes,
            ha="center", fontsize=15, color=INK, fontweight="bold")

    draw_panel(ax, 0.04, "Keyword search (BM25)", "ranks by matching words", kw)
    draw_panel(ax, 0.52, "Semantic search (embeddings)", "ranks by meaning", sem)

    ax.text(0.5, 0.015,
            "Same query, same corpus  —  semantic search puts both relevant answers "
            "at the top; keyword search leads with unrelated hits.",
            transform=ax.transAxes, ha="center", fontsize=9.5, color=GREY)

    out = ROOT / "assets" / "demo.png"
    fig.savefig(out, dpi=150, bbox_inches="tight", facecolor="white")
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
