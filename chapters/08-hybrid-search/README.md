# Chapter 8 — Hybrid Search

> **Level:** 🟡 Intermediate  ·  **Status:** 🟩 Complete
> **Prerequisites:** Chapters 2 (BM25) and 5 (dense retrieval).
> **You'll build:** a hybrid retriever that fuses keyword and semantic search, and see it beat
> either one alone.

---

## At a glance

We've now built two retrievers that fail in *different* ways. BM25 nails exact words but is
blind to meaning; dense retrieval matches meaning but can miss exact terms, names, and codes.
The obvious move: **use both and combine them.** That's **hybrid search**, and because the two
methods are complementary, the fused result is often better than either alone. The trick is
*how* to combine two different kinds of scores — and the cleanest answer is **Reciprocal Rank
Fusion (RRF)**.

---

## The motivation

A quick table you've seen building across the course:

| Query | BM25 (keyword) | Dense (semantic) |
|-------|----------------|------------------|
| "strong pain in the side of the head" | ❌ misses (no shared words) | ✅ finds migraine passage |
| "a large ocean animal" | ❌ misses | ✅ finds blue whale |
| "Lucene" (exact library name) | ✅ exact hit | ⚠️ may drift |
| "SKU-4471-B" (a product code) | ✅ exact hit | ❌ meaningless to the model |

Notice the ❌'s and ✅'s are in *different rows*. Where one fails, the other tends to succeed.
Hybrid search is about capturing both columns of ✅ at once.

---

## The hard part: two scores that don't mix

You can't just add a BM25 score and a cosine score. They live on different scales:

- **BM25** scores are unbounded positives (e.g., 0 to ~15), depending on term rarity and length.
- **Cosine** scores sit in roughly [−1, 1].

Adding them lets BM25's larger numbers dominate arbitrarily. Two ways to fix this:

### Option A — Score normalization + weighted sum
Rescale each score to [0, 1] (e.g., min-max), then combine with a weight:

```
hybrid = α · normalize(dense_score) + (1 − α) · normalize(bm25_score)
```

Simple, but fragile: min-max normalization is sensitive to outliers, and the best α varies by
query and corpus.

### Option B — Reciprocal Rank Fusion (RRF) ← preferred
Ignore the raw scores entirely; use only each document's **rank** in each list. For a document
*d*:

$$\text{RRF}(d) = \sum_{r \in \text{rankers}} \frac{1}{k + \text{rank}_r(d)}$$

where `rank` is 1-based and *k* is a small constant (commonly 60). Sum a document's reciprocal
ranks across all retrievers; sort by the total.

Why RRF is the default:

- **Scale-free.** It never compares a BM25 number to a cosine number — only positions.
- **Robust.** Outlier scores can't dominate; a document ranked highly by *both* retrievers wins.
- **Trivially simple.** A few lines of code, no tuning of α, no normalization headaches.

### RRF worked example

Query returns these rankings (k = 60):

```
BM25 : [D10, D4,  D2]        Dense: [D2,  D4,  D7]
        #1   #2   #3                 #1   #2   #3

RRF scores (k = 60):
D2  : 1/(60+3) [BM25 #3] + 1/(60+1) [Dense #1] = 0.01587 + 0.01639 = 0.03227   ← highest
D4  : 1/(60+2) [BM25 #2] + 1/(60+2) [Dense #2] = 0.01613 + 0.01613 = 0.03226   ← a hair behind
D10 : 1/(60+1) [BM25 #1] + 0        (not in Dense)                 = 0.01639
D7  : 0        (not in BM25) + 1/(60+3) [Dense #3]                 = 0.01587
```

D2 and D4 rise to the top because *both* retrievers liked them — exactly the consensus behavior
we want, and neither needed to be #1 in a single list to win. The documents only one retriever
found (D10, D7) rank well below them. Note D2 edges out D4 despite D4 being more evenly placed:
one #1 finish (1/61) outweighs two #2 finishes here. RRF rewards strong positions and,
especially, agreement across retrievers.

---

## Hands-on

Notebook: [`notebooks/08_hybrid_search.ipynb`](notebooks/08_hybrid_search.ipynb)

You will:

1. Reuse BM25 (Chapter 2) and the dense retriever (Chapter 5) to produce two ranked lists.
2. Implement **Reciprocal Rank Fusion** in a few lines and fuse the lists.
3. Compare BM25-only vs. dense-only vs. hybrid on queries designed to expose each method's
   weakness (a synonym query and an exact-token query).
4. See hybrid stay strong on *both*, where each single method fails on one.
5. (Optional) Add the Chapter 7 re-ranker on top of the fused candidates — the full modern stack.

> The RRF logic is pure Python and runs anywhere. The dense list needs the embedding model
> (runs on your machine); the fusion is verified independently with fixed rankings.

---

## Slides

📊 **[Chapter 8 slide deck (PDF)](../../slides/Chapter-08-Hybrid-Search.pdf)** — a visual summary of
fusing keyword and semantic retrieval.

---

## Going deeper 🔴

- **Tuning k in RRF.** Larger *k* flattens the contribution of top ranks (more democratic across
  the list); smaller *k* rewards being #1 heavily. 60 is a robust default from the original
  paper.
- **Weighted RRF.** You can weight retrievers: `Σ wᵣ /(k + rankᵣ)`. Useful when you trust one
  retriever more, but adds a knob to tune.
- **Hybrid + re-rank is the standard modern stack:** BM25 ∪ dense → RRF fuse → cross-encoder
  re-rank → (LLM for RAG). Chapters 2, 5, 7, 8, and 10 assembled.
- **Sparse-neural hybrids.** Learned sparse models (SPLADE) blur the keyword/semantic line by
  putting semantics *into* an inverted index; another route to "best of both."
- **Fusion vs. single strong model.** Sometimes one well-tuned retriever suffices. Measure
  (Chapter 9) before adding fusion complexity.

---

## Pitfalls & gotchas

- **Summing raw scores from different scales.** The classic mistake; use RRF or normalize
  carefully.
- **Fusing lists of different lengths inconsistently.** Decide how to treat documents missing
  from one list (they simply contribute 0 from that retriever in RRF).
- **Assuming hybrid always wins.** For a corpus of pure natural-language prose with no codes or
  names, dense alone may already be enough — hybrid adds most when queries mix intent and exact
  terms.
- **Double-counting near-duplicate retrievers.** Fusing two very similar dense models adds little;
  diversity (lexical + semantic) is what makes fusion pay off.

---

## Key terms

hybrid search, score normalization, Reciprocal Rank Fusion (RRF), rank fusion, weighted fusion,
complementary retrievers, SPLADE. *(See [GLOSSARY](../../GLOSSARY.md).)*

---

## Check your understanding

1. Why can't you simply add a BM25 score and a cosine score together?
2. Explain, in one sentence, what RRF uses instead of raw scores and why that helps.
3. In the worked example, why do D2 and D4 outrank D10 and D7?
4. Give a query where hybrid clearly beats both BM25-only and dense-only, and say why.
5. Where does re-ranking (Chapter 7) fit relative to fusion in the full stack?

---

<!-- cyu-answers:start -->

> 💡 *Try answering each question yourself first, then expand to check.*

<details>
<summary><b>Show answer — 1</b></summary>

They live on different scales (BM25 is unbounded positive; cosine is roughly [-1, 1]), so summing lets BM25's larger numbers dominate arbitrarily and swamp the semantic signal.

</details>

<details>
<summary><b>Show answer — 2</b></summary>

It uses each document's **rank** in each list (via 1/(k+rank)), not the raw scores — so it never compares incompatible score scales and is robust to outliers; documents ranked highly by multiple retrievers win.

</details>

<details>
<summary><b>Show answer — 3</b></summary>

Because both retrievers ranked D2 and D4 highly, so they accumulate reciprocal-rank contributions from both lists; D10 and D7 appear in only one list, contributing from a single source and scoring lower.

</details>

<details>
<summary><b>Show answer — 4</b></summary>

A query mixing an exact term with fuzzy intent, e.g. *"Lucene for semantic search"* or *"SKU-4471-B waterproof jacket"*: keyword nails the exact token, dense captures the intent, and RRF keeps documents both liked on top.

</details>

<details>
<summary><b>Show answer — 5</b></summary>

**After** fusion: hybrid (BM25 ∪ dense -> RRF) produces the candidate set, then the cross-encoder re-ranks those candidates for the final order (BM25 ∪ dense -> RRF -> re-rank -> RAG).

</details>

<!-- cyu-answers:end -->

## References

- Cormack, Clarke & Büttcher, *Reciprocal Rank Fusion outperforms Condorcet and individual rank
  learning methods* (2009) — the RRF paper.
- Robertson & Zaragoza, *The Probabilistic Relevance Framework: BM25 and Beyond* (2009).
- Formal et al., *SPLADE* (2021) — learned sparse retrieval.
- DeepLearning.AI × Cohere, *Large Language Models with Semantic Search* (inspiration).
