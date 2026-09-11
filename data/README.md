# Sample Data

Small, redistributable datasets used across chapters so every notebook is runnable out of
the box (a handful of short documents to search over). Larger or licensed datasets are
downloaded on demand inside the relevant notebook.

| File | Contents | Used in |
|------|----------|---------|
| `sample_corpus.json` | 16 short, original passages (id, title, text) on deliberately varied topics, including near-synonym pairs that show where keyword search fails and semantic search succeeds. | Every chapter, via `src/corpus.py` |
| `eval_queries.json` | 6 queries with binary relevance judgements over the sample corpus. | Chapter 9 — Evaluating Search |

Both files are original and released under CC BY 4.0 with the rest of the course content.
