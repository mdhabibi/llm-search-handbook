# Chapter 7 — Re-ranking

> **Level:** 🟡 Intermediate  ·  **Status:** 🟩 Complete
> **Prerequisites:** Chapter 5 (dense retrieval). Chapter 6 helpful.
> **You'll build:** a two-stage retrieve-then-rerank pipeline and measure the quality jump.

---

## At a glance

First-stage retrieval (BM25 or dense) is built for *speed*: it scans the whole corpus, so it
has to be cheap. That speed comes at a cost in precision — the top result isn't always the
*best* result. **Re-ranking** adds a second, slower, much more accurate model that re-scores
only the handful of candidates the first stage returned. This "retrieve wide and cheap, then
re-rank narrow and precise" pattern is how nearly every production search and RAG system gets
both speed and quality.

---

## The motivation

Recall the bi-encoder from Chapter 5: it embeds the query and each document *separately*, then
compares vectors. That separation is what makes it fast (precompute all document vectors) — but
it's also a limitation. The model never gets to read the query and a document *together*, so it
can miss subtle relevance signals. The result: the right document is usually somewhere in the
top 20–100, but not always at rank 1. Re-ranking fixes the ordering of that small set.

```
Stage 1 (retrieval)          Stage 2 (re-ranking)
top-50 candidates,           read query+doc TOGETHER,
fast but approximate    ─▶   re-score each of the 50   ─▶   precise top-5
(bi-encoder / BM25)          (cross-encoder)
```

---

## Bi-encoder vs. cross-encoder — the key distinction

This is the heart of the chapter.

```
BI-ENCODER (Chapter 5, first stage)        CROSS-ENCODER (this chapter, re-ranker)
──────────────────────────────────        ────────────────────────────────────────
query ─▶[encoder]─▶ q_vec                  query ┐
doc   ─▶[encoder]─▶ d_vec                        ├─▶ [ single model reads BOTH ] ─▶ score
score = cosine(q_vec, d_vec)               doc   ┘        (a relevance number)

+ document vectors precomputed once        + reads query+doc jointly -> far more accurate
+ scoring is just vector math (fast)       - must run the model for EVERY query-doc pair (slow)
- never sees query & doc together          - cannot precompute -> impossible over a full corpus
```

- A **bi-encoder** is like matching people by their dating-profile vectors — fast, but each
  profile was written without knowing who's asking.
- A **cross-encoder** is like a recruiter reading the job description and a résumé *side by
  side* — much better judgment, but you can't do it for a million résumés per query.

So we use each where it shines: bi-encoder to *retrieve* many candidates cheaply, cross-encoder
to *re-rank* the few precisely.

---

## Why not just use the cross-encoder for everything?

Because it can't precompute. To find the best of *N* documents, a cross-encoder must run the
model *N* times **per query** — reading each (query, document) pair fresh. At a million
documents that's a million forward passes for a single search: hopelessly slow. The bi-encoder
narrows the field to ~50 first; the cross-encoder then does its expensive, accurate work on
just those 50. Best of both worlds.

---

## The model we use

An open-source cross-encoder trained on MS MARCO (a large query→passage relevance dataset):

```python
from sentence_transformers import CrossEncoder
reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")
scores = reranker.predict([(query, doc1), (query, doc2), ...])   # higher = more relevant
```

It outputs a relevance score for each (query, document) pair. We sort candidates by that score.

---

## Hands-on

Notebook: [`notebooks/07_reranking.ipynb`](notebooks/07_reranking.ipynb)

You will:

1. Retrieve top-k candidates with the Chapter 5 dense retriever (first stage).
2. Load a **cross-encoder** and re-score those candidates (second stage).
3. Watch the ordering improve — a relevant passage that sat at rank 4 jumps to rank 1.
4. Wrap it as a reusable `retrieve_then_rerank(query)` function.
5. Discuss the cost: how big should the first-stage candidate set be? (The recall/latency knob.)

> The cross-encoder downloads on first run (internet once). The pipeline logic (take top-k,
> score pairs, re-sort) is written to be testable with a mock scorer.

---

## Going deeper 🔴

- **Choosing the candidate depth (top-k).** Re-rank too few and you might exclude the best
  document (first-stage recall caps your ceiling); re-rank too many and latency grows. Typical
  values: retrieve 50–200, re-rank to 5–10. Tune by measuring (Chapter 9).
- **Re-ranking is bounded by retrieval recall.** A re-ranker can only reorder what it's given.
  If the right document never made the top-50, no re-ranker can save you — improve first-stage
  recall first.
- **Extra signals.** Production re-rankers often blend the semantic score with popularity,
  freshness, click data, or business rules — re-ranking is the natural place to fold these in.
- **LLM re-rankers.** You can prompt an LLM to rank passages (listwise). Powerful but slower and
  costlier than a dedicated cross-encoder; useful when quality matters more than latency.
- **Latency budgeting.** The cross-encoder is the expensive step; batch the pairs and cap k to
  stay within your latency target.

---

## Pitfalls & gotchas

- **Re-ranking the whole corpus.** Never. Only re-rank the small first-stage candidate set.
- **Mismatched task.** Use a cross-encoder trained for query→passage relevance (e.g. MS MARCO),
  not a sentence-similarity model, for search re-ranking.
- **Ignoring first-stage recall.** Spending all your effort on the re-ranker while the retriever
  misses relevant docs is optimizing the wrong stage.
- **Comparing cross-encoder scores across queries.** Like cosine scores, they rank within a
  query; they're not calibrated probabilities across queries.

---

## Key terms

re-ranking, cross-encoder, bi-encoder, two-stage retrieval, candidate set, first-stage recall,
MS MARCO, listwise ranking. *(See [GLOSSARY](../../GLOSSARY.md).)*

---

## Check your understanding

1. In one sentence, what can a cross-encoder do that a bi-encoder can't — and what does it cost?
2. Why can't we just use the cross-encoder as the first-stage retriever?
3. What limits how much a re-ranker can improve results, no matter how good it is?
4. You retrieve top-10 and re-rank, but quality is still poor. Name two different fixes and when
   each applies.
5. Where in a two-stage pipeline would you add a "prefer recent documents" rule, and why there?

---

<!-- cyu-answers:start -->

> 💡 *Try answering each question yourself first, then expand to check.*

<details>
<summary><b>Show answer — 1</b></summary>

A cross-encoder reads the query and a document **together**, giving a far more accurate relevance score; the cost is it must run the model for every query-document pair, so it can't be precomputed.

</details>

<details>
<summary><b>Show answer — 2</b></summary>

Because it can't precompute: scoring N documents means N model runs **per query**, which is hopelessly slow over a full corpus. The bi-encoder narrows the field first so the cross-encoder only scores a few candidates.

</details>

<details>
<summary><b>Show answer — 3</b></summary>

**First-stage recall.** A re-ranker only reorders the candidates it's given; if the relevant document never made the first-stage top-k, no re-ranker can surface it.

</details>

<details>
<summary><b>Show answer — 4</b></summary>

Either (a) the right document isn't in the top-10 -> improve **first-stage retrieval** (bigger k, hybrid, better embeddings); or (b) it is but ranked wrong -> use a **stronger/better-matched re-ranker**. Diagnose by checking whether the relevant doc is in the candidate set.

</details>

<details>
<summary><b>Show answer — 5</b></summary>

In the **re-ranking** stage — it's the natural place to blend extra signals (recency, popularity, business rules) with the relevance score, on the small candidate set, without slowing first-stage retrieval.

</details>

<!-- cyu-answers:end -->

## References

- Nogueira & Cho, *Passage Re-ranking with BERT* (2019) — the cross-encoder re-ranking idea.
- Reimers & Gurevych, *Sentence-BERT* (2019) — bi- vs. cross-encoder trade-offs.
- `sentence-transformers` CrossEncoder documentation and MS MARCO models.
- DeepLearning.AI × Cohere, *Large Language Models with Semantic Search*, Lesson 4 (inspiration).
