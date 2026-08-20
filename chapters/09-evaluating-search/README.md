# Chapter 9 — Evaluating Search

> **Level:** 🟡 Intermediate  ·  **Status:** 🟩 Complete
> **Prerequisites:** Chapters 2, 5, 7, 8 (the retrievers we'll score).
> **You'll build:** an evaluation harness and a leaderboard comparing every retriever you've
> built.

---

## At a glance

We've built keyword, dense, hybrid, and re-ranked retrievers, and *claimed* each is better than
the last. This chapter makes those claims **measurable**. You'll create a small labeled test set
and implement the standard IR metrics — **precision@k, recall@k, MRR, nDCG, MAP** — from scratch,
then use them to turn "this feels better" into a number.

> The golden rule of this chapter: **you cannot improve what you do not measure.** Every tuning
> decision in earlier chapters (k₁ and b in BM25, efSearch in HNSW, α in hybrid, candidate depth
> in re-ranking) should be made by measuring, not guessing.

---

## The motivation

Imagine two search systems. On one query System A looks better; on another System B does. Which
should you ship? Eyeballing a few queries doesn't scale and isn't reproducible. We need (1) a set
of queries with known correct answers, and (2) numbers that summarize ranking quality across all
of them. That's an **evaluation set** plus **metrics**.

---

## Step 1 — Relevance judgments (the ground truth)

Evaluation starts with a labeled set: queries paired with the documents a human judged
**relevant**. We ship a tiny one in [`data/eval_queries.json`](../../data/eval_queries.json) —
six queries over our 16-passage corpus, each with its relevant document ids.

```json
{"query": "a large animal that lives in the ocean", "relevant_ids": [4, 5]}
```

We use **binary** relevance (relevant or not) for simplicity. Real sets are bigger and often use
**graded** relevance (perfect / good / marginal), which nDCG can exploit. Building good judgments
is the hard, human part of evaluation — the metrics are the easy part.

---

## Step 2 — The metrics, by intuition

Each metric answers a different question. Implemented from scratch in
[`src/metrics.py`](../../src/metrics.py).

### Precision@k — "of what I showed, how much was good?"
Fraction of the top-k results that are relevant. `precision@5 = 0.6` → 3 of the top 5 are
relevant. Cares about the top; ignores relevant docs you missed.

### Recall@k — "of what's good, how much did I find?"
Fraction of all relevant documents that appear in the top-k. `recall@5 = 0.5` → you surfaced
half of the relevant docs. Precision and recall trade off against each other.

### MRR (Mean Reciprocal Rank) — "how high was the *first* right answer?"
For each query take `1 / (rank of the first relevant result)`, then average over queries. First
relevant at rank 1 → 1.0; rank 2 → 0.5; rank 5 → 0.2. Perfect when you only care about the single
best answer (e.g., "I feel lucky" search, or the top passage for RAG).

### nDCG (Normalized Discounted Cumulative Gain) — "are the best results near the top?"
Rewards putting relevant documents *high*, with a logarithmic discount for lower positions, then
normalizes by the ideal ordering so the score sits in [0, 1]. The go-to metric when *order*
matters across the whole list.

```
DCG   = Σ  gain(rank) / log2(rank + 1)          (a hit at rank 1 is worth more than at rank 5)
nDCG  = DCG / DCG(ideal ranking)                 (1.0 = perfect order)
```

### MAP (Mean Average Precision) — "overall precision across all relevant docs"
Average precision computes precision each time a relevant doc appears, averaged; MAP averages
that over queries. A single robust number that accounts for both rank and completeness.

### Which to use?
- One correct answer matters most → **MRR**.
- Ordering of many relevant docs matters → **nDCG**.
- Overall precision/recall balance → **MAP** / **precision@k** / **recall@k**.
Report several; they illuminate different failure modes.

### A worked nDCG number
For ranked `[D0, D1, D2, D3]` with relevant `{D1, D3}` (hits at ranks 2 and 4):

```
DCG@4  = 1/log2(3) + 1/log2(5) = 0.6309 + 0.4307 = 1.0616
ideal  = 1/log2(2) + 1/log2(3) = 1.0000 + 0.6309 = 1.6309   (both relevant docs up front)
nDCG@4 = 1.0616 / 1.6309 = 0.651
```

(These exact numbers are asserted in the notebook, so you can trust the implementation.)

---

## Step 3 — The leaderboard

The notebook evaluates BM25, dense, hybrid, and (optionally) re-ranked retrieval on the same test
set and prints a table:

```
retriever     nDCG@5   MRR    recall@5
BM25            ...     ...     ...
Dense           ...     ...     ...
Hybrid          ...     ...     ...
Dense+Rerank    ...     ...     ...
```

Now the progression across the course stops being a story and becomes evidence.

---

## Hands-on

Notebook: [`notebooks/09_evaluating_search.ipynb`](notebooks/09_evaluating_search.ipynb)

You will:

1. Load the labeled queries and confirm the metric implementations against hand-computed values.
2. Produce rankings from BM25, dense, and hybrid retrievers over the eval queries.
3. Compute precision@k, recall@k, MRR, nDCG, MAP and assemble a **leaderboard**.
4. Interpret the differences — and notice how a tiny test set makes numbers noisy (a lesson in
   itself).

> BM25 evaluation runs fully offline. Dense/hybrid rows use the embedding model (your machine).
> The metric functions are verified independently with fixed rankings.

---

## Slides

📊 **[Chapter 9 slide deck (PDF)](../../slides/Chapter-09-Evaluating-Search.pdf)** — a visual summary
of measuring search quality with IR metrics.

---

## Going deeper 🔴

- **Offline vs. online.** Offline metrics (this chapter) use a fixed labeled set. Online
  evaluation (**A/B testing**, interleaving) measures real user behavior — clicks, dwell time,
  conversions — which is the ultimate ground truth but slower and costlier to run.
- **Statistical significance.** With six queries, differences are noise. Real evaluations use
  hundreds/thousands of queries and significance tests (e.g., paired t-test) before declaring a
  winner.
- **Graded relevance & judgment cost.** nDCG shines with graded labels. Gathering judgments is
  expensive; pooling and tools like TREC-style qrels exist to manage it.
- **Metric gaming.** Optimizing one metric can hurt others (e.g., chasing recall floods results
  with marginal hits). Watch a basket of metrics.
- **Beyond relevance.** Production also weighs latency, diversity, freshness, and fairness —
  quality is multi-dimensional.

---

## Pitfalls & gotchas

- **Tuning on your test set.** If you tune hyperparameters against the same queries you report
  on, you overfit. Keep a separate dev/validation set.
- **Reading too much into a tiny set.** Six queries can't rank systems reliably; treat this
  chapter's numbers as illustrative, not definitive.
- **Comparing metrics at different k.** precision@5 and precision@10 aren't comparable; fix k.
- **Ignoring first-stage recall when evaluating re-rankers.** If retrieval missed the relevant
  doc, the re-ranker's ceiling is already capped — measure both stages.

---

## Key terms

relevance judgments, ground truth, precision@k, recall@k, MRR, nDCG, DCG, MAP, average precision,
offline vs. online evaluation, A/B testing. *(See [GLOSSARY](../../GLOSSARY.md).)*

---

## Check your understanding

1. Give the one-line question each of precision@k, recall@k, MRR, and nDCG answers.
2. Why does nDCG need to be *normalized*, and what by?
3. When is MRR the right metric to optimize, and when is it misleading?
4. Why are six queries not enough to declare one retriever better than another?
5. What's the danger of tuning k₁, b, or α on the same queries you report metrics on?

---

<!-- cyu-answers:start -->

> 💡 *Try answering each question yourself first, then expand to check.*

<details>
<summary><b>Show answer — 1</b></summary>

**Precision@k**: of the top-k I showed, how many were relevant? **Recall@k**: of all relevant docs, how many did I find in the top-k? **MRR**: how high was the first relevant result? **nDCG**: are the most relevant results near the top?

</details>

<details>
<summary><b>Show answer — 2</b></summary>

Because raw DCG grows with the number of relevant documents and isn't comparable across queries; dividing by the **ideal DCG** (the best possible ordering) rescales it to [0, 1] so queries are comparable.

</details>

<details>
<summary><b>Show answer — 3</b></summary>

Right when only the single best answer matters (e.g. one passage for RAG, an "I feel lucky" result). Misleading when there are many relevant documents and you care about finding all of them or their overall order — MRR only looks at the first hit.

</details>

<details>
<summary><b>Show answer — 4</b></summary>

The results are too noisy: with so few queries, one lucky or unlucky query swings the average, and differences between systems aren't statistically significant. Real evaluations use hundreds+ of queries.

</details>

<details>
<summary><b>Show answer — 5</b></summary>

You **overfit** to those queries — you'll pick settings that look good on the test set but don't generalize. Tune on a separate dev/validation split and report on a held-out test set.

</details>

<!-- cyu-answers:end -->

## References

- Manning, Raghavan & Schütze, *Introduction to Information Retrieval*, evaluation chapter.
- Järvelin & Kekäläinen, *Cumulated Gain-based Evaluation of IR Techniques* (nDCG, 2002).
- TREC evaluation methodology and `trec_eval` (industry-standard tooling).
- DeepLearning.AI × Cohere, *Large Language Models with Semantic Search* (inspiration).
