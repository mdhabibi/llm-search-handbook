# Chapter 5 — Dense Retrieval & Semantic Search

> **Level:** 🟢 Beginner → 🟡 Intermediate  ·  **Status:** 🟩 Complete
> **Prerequisites:** Chapter 4 (embeddings & cosine similarity).
> **You'll build:** a complete semantic search engine you query in natural language, and a
> head-to-head against BM25.

---

## At a glance

This is the payoff of Part III. We take the embeddings from Chapter 4 and turn them into an
actual **search engine**: embed every document once, embed the query, return the documents whose
vectors are nearest. That's **dense retrieval** — retrieval by *meaning*. You'll build it end to
end over our own corpus, then race it against the BM25 engine from Chapter 2 to see exactly where
each wins.

---

## The motivation

We've been circling this since Chapter 1: the *"strong pain in the side of the head"* query whose
answer (the migraine passage) says *"sharp sensation localized to one temple."* Keyword search
can't bridge that gap. In Chapter 4 we saw embeddings put those two phrases near each other in
vector space. Now we make that the basis of retrieval — so a user can ask in their own words and
still find the right passage.

---

## The core algorithm (three steps)

Dense retrieval is beautifully simple:

```
   INDEXING (once, offline)                 SEARCH (per query)
   ─────────────────────────                ────────────────────────────
   for each document d:                     1. embed the query -> q_vec
       d_vec = embed(d)                      2. score every d: cosine(q_vec, d_vec)
   store all d_vec in a matrix               3. return the top-k highest-scoring docs
```

That's it. The "intelligence" lives entirely in the embedding model; retrieval itself is just
"find the nearest vectors." Contrast this with BM25, where the intelligence was in the scoring
formula and the model was just word counts.

```
   query ──embed──▶ q_vec ─┐
                           ├─ cosine similarity ─▶ ranked documents
  corpus ─embed──▶ D (matrix)┘   (nearest = most relevant)
```

---

## The bi-encoder: why this scales

The model we use is a **bi-encoder** (two-tower): it embeds the query and each document
*independently*.

```
        ┌───────────┐                    ┌───────────┐
query ─▶│  encoder  │─▶ q_vec   d ──────▶│  encoder  │─▶ d_vec
        └───────────┘                    └───────────┘
                     ╲                  ╱
                      cosine(q_vec, d_vec)
```

Why does "independently" matter so much? Because document vectors don't depend on the query, you
can **precompute them all once** and reuse them for every future query. At search time you only
embed the (short) query and do fast vector math. This is what makes dense retrieval practical over
millions of documents — and it's the crucial difference from the **cross-encoder** re-ranker in
Chapter 7, which is more accurate but must re-run the model for every query–document pair.

---

## Building it over our corpus

In the notebook we implement a small, reusable `SemanticSearch` class:

1. **Index:** embed all 16 passages → a `(16, 384)` matrix, L2-normalized so cosine = dot
   product.
2. **Search:** embed the query, take the dot product with the matrix, `argsort` for the top-k.
3. **Query in plain English:** `search("why is grass green?")`, `search("a large ocean animal")`,
   `search("strong pain in the side of the head")`.

The migraine query — our running example — now returns the migraine passage as the **top** result,
finally solving the problem we posed in Chapter 1.

---

## Dense vs. BM25: a fair race

Neither method is strictly better; they fail differently. We run both on the same queries and
compare:

| Query type | BM25 (keyword) | Dense (semantic) |
|------------|----------------|------------------|
| Paraphrase / synonyms ("pain in the head" → "temple") | ❌ misses | ✅ finds |
| Conceptual ("a large ocean animal" → "blue whale") | ❌ often misses | ✅ finds |
| Exact rare term / code / name ("all-MiniLM-L6-v2") | ✅ nails it | ⚠️ can drift |
| Typo-free keyword overlap | ✅ strong | ✅ usually fine |

The takeaway that sets up Chapter 8: **dense retrieval wins on meaning; keyword retrieval wins on
exactness.** Real systems often want both — which is why hybrid search exists.

---

## Hands-on

Notebook: [`notebooks/05_dense_retrieval.ipynb`](notebooks/05_dense_retrieval.ipynb)

You will:

1. Build a reusable `SemanticSearch` class (index + search).
2. Query the corpus in natural language and inspect scores.
3. Confirm the migraine query is finally solved.
4. Run **dense vs. BM25** side by side on several queries and interpret the differences.
5. Probe a failure case (an exact rare token) that motivates hybrid search.

> First run downloads the small embedding model (needs internet once). The retrieval logic
> (normalize, dot product, top-k) is written to be testable even without the model.

---

## Slides

📊 **[Chapter 5 slide deck (PDF)](../../slides/Chapter-05-Dense-Retrieval.pdf)** — a visual
summary of dense retrieval and semantic search.

---

## Going deeper 🔴

- **Exact vs. approximate search.** Our corpus is tiny, so we compute cosine against *every*
  document (brute force, exact). At scale that's too slow — Chapter 6 introduces approximate
  nearest-neighbor indexes.
- **Asymmetric retrieval.** For question→passage search, models fine-tuned on query/passage pairs
  (e.g. MS MARCO models) often beat symmetric sentence models. Match the model to the task.
- **Score calibration.** Cosine scores aren't probabilities and aren't comparable across models
  or even across queries. Use them to *rank*, not as absolute confidence.
- **Dense vs. sparse-neural (SPLADE).** There's a middle ground: learned *sparse* representations
  that keep an inverted index but add semantics. Worth knowing the landscape exists.

---

## Pitfalls & gotchas

- **Embedding query and corpus with different models** (or different pooling/normalization) →
  garbage results. Keep them identical.
- **Forgetting to normalize** when you use dot product as the similarity. Either normalize and use
  dot product, or use full cosine.
- **Assuming semantic always beats keyword.** It doesn't for exact identifiers, product codes,
  or rare names — the exact case keyword search was built for.
- **Stale index.** Add or edit documents? You must embed and add them to the matrix, or they're
  invisible to search.

---

## Key terms

dense retrieval, semantic search, bi-encoder, two-tower, embedding index, nearest neighbor search,
brute-force search, top-k, asymmetric search. *(See [GLOSSARY](../../GLOSSARY.md).)*

---

## Check your understanding

1. State the three steps of dense retrieval in your own words.
2. Why can a bi-encoder precompute document vectors, and why is that essential for scale?
3. Give one query where BM25 beats dense retrieval, and explain why.
4. Why do we L2-normalize the embeddings before taking dot products?
5. Our search is "brute force." What does that mean, and when does it stop being good enough?

---

<!-- cyu-answers:start -->

> 💡 *Try answering each question yourself first, then expand to check.*

<details>
<summary><b>Show answer — 1</b></summary>

(1) Embed every document once into a matrix (indexing); (2) embed the query; (3) score documents by similarity to the query vector and return the top-k nearest.

</details>

<details>
<summary><b>Show answer — 2</b></summary>

Because a bi-encoder embeds documents without seeing the query, their vectors are query-independent and can be computed once and reused for every search. Without that, you couldn't search a large corpus fast.

</details>

<details>
<summary><b>Show answer — 3</b></summary>

Exact terms it doesn't understand semantically — e.g. a product code like `SKU-4471-B`, a rare proper name, or the exact string `Lucene`; keyword search matches these exactly while a dense model may drift.

</details>

<details>
<summary><b>Show answer — 4</b></summary>

So that the dot product equals cosine similarity. Normalizing removes magnitude effects (which often just reflect length), leaving direction (meaning) — and it's faster than computing full cosine each time.

</details>

<details>
<summary><b>Show answer — 5</b></summary>

"Brute force" means scoring the query against **every** document (exact, O(N)). It stops being good enough when N grows large (hundreds of thousands+), where the per-query cost becomes too slow — motivating ANN (Chapter 6).

</details>

<!-- cyu-answers:end -->

## References

- Karpukhin et al., *Dense Passage Retrieval for Open-Domain Question Answering* (DPR, 2020).
- Reimers & Gurevych, *Sentence-BERT* (2019).
- `sentence-transformers` documentation (semantic search utilities).
- DeepLearning.AI × Cohere, *Large Language Models with Semantic Search*, Lesson 3 (inspiration).
