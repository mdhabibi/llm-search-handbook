# Chapter 6 — Vector Databases & Approximate Nearest Neighbor (ANN)

> **Level:** 🟡 Intermediate  ·  **Status:** 🟩 Complete
> **Prerequisites:** Chapter 5 (dense retrieval).
> **You'll build:** a fast, persistent vector index and a felt understanding of the
> speed-vs-accuracy trade-off behind every vector database.

---

## At a glance

In Chapter 5 we scored the query against *every* document (brute force). That's exact and fine for
16 passages — but hopeless for 16 million. This chapter is about making nearest-neighbor search
*fast at scale*: the **approximate nearest neighbor (ANN)** idea, the index types that implement it
(**HNSW**, IVF, PQ), and the **vector databases** (FAISS, Chroma) that package it up with
persistence and metadata filtering.

---

## The motivation

Semantic search has a scaling problem hiding in plain sight. Brute-force search compares the query
to all *N* documents — that's *O(N)* per query. At a million vectors of 384 dimensions, every
single search touches hundreds of millions of numbers. Users expect answers in **milliseconds**.
Something has to give. The insight: we don't actually need the *exact* nearest neighbors — we need
the *right documents*, fast. Trading a tiny bit of accuracy for a huge speed-up is the whole game.

---

## Brute force, and why it breaks

```
brute force:  for each of N documents, compute similarity to the query, keep the top-k
              cost ∝ N × dimensions      ← grows linearly with corpus size
```

Double the corpus, double the work — *every query, forever*. Exact, but it doesn't scale. ANN
changes the shape of that cost.

---

## The ANN idea: don't look at everything

Approximate nearest neighbor algorithms **pre-organize** the vectors so a query only has to examine
a small, promising subset instead of the whole corpus. You give up the guarantee of finding the
*exact* closest vectors; in return you get sublinear search that's often 10–1000× faster while still
returning the true top results the vast majority of the time.

We measure that "vast majority" with **recall@k**: of the true top-k neighbors (from brute force),
how many did the approximate index actually return? Recall of 0.95 means you're getting 95% of the
exact answers at a fraction of the cost — usually a great deal.

### Two families to know

**HNSW (Hierarchical Navigable Small World)** — a *graph*. Each vector is a node linked to its near
neighbors, with a hierarchy of layers (like express lanes on a highway). A search greedily hops
from node to node, zooming in on the query's neighborhood. Fast, high recall, memory-hungry, and the
default in most vector databases.

```
   HNSW: start at the top layer (few, long links), descend layer by layer,
         at each layer walk greedily toward the query, refine at the bottom.

   layer 2:   ● ───────────────── ●            (coarse, long hops)
   layer 1:   ● ──── ● ──── ● ──── ●           (medium)
   layer 0:   ●─●─●─●─●─●─●─●─●─●─●─●           (dense, short hops — the full graph)
```

**IVF (Inverted File)** — *clustering*. Partition the space into buckets (via k-means); at query
time, only search the few buckets nearest the query instead of all of them. Simple and effective.

**Product Quantization (PQ)** — *compression*. Squash each vector into a compact code so millions
fit in RAM and distance approximations are cheap. Often combined with IVF (`IVF+PQ`).

You don't need to implement these — you need to know they exist and what knob each offers (recall
vs. speed vs. memory).

---

## Vector databases: the index plus everything else

An ANN index alone isn't a product. A **vector database** wraps it with the things real apps need:

- **Persistence** — save the index to disk and reload it; don't re-embed on every restart.
- **Metadata & filtering** — store fields alongside vectors ("language = en", "year ≥ 2020") and
  filter during search.
- **CRUD** — add, update, delete vectors as your corpus changes.
- **Scaling & serving** — batching, sharding, an API.

We use two open-source options:

- **FAISS** — a fast in-memory index library (from Meta). Great for learning and for large static
  indexes. We use `IndexFlatIP` (exact) and `IndexHNSWFlat` (approximate).
- **Chroma** — a lightweight vector *database* with persistence and metadata filtering, a gentle
  on-ramp to production patterns.

---

## Hands-on

Notebook: [`notebooks/06_vector_databases.ipynb`](notebooks/06_vector_databases.ipynb)

You will:

1. Build an **exact** FAISS index (`IndexFlatIP`) and confirm it matches Chapter 5's brute force.
2. Build an **HNSW** index over a larger set of synthetic vectors.
3. **Benchmark**: measure query time and **recall@10** of HNSW vs. exact search — and *feel* the
   trade-off (big speed-up, tiny recall loss).
4. Use **Chroma** to persist embeddings with metadata and run a filtered semantic query
   ("only English passages").
5. Reflect on choosing an index for your corpus size.

> The FAISS benchmark runs fully offline with synthetic vectors (no model needed). The Chroma
> section uses the embedding model, so it runs on your machine after the first model download.

---

## Slides

📊 **[Chapter 6 slide deck (PDF)](../../slides/Chapter-06-Vector-Databases-and-ANN.pdf)** — a visual
summary of vector databases and approximate nearest neighbor search.

---

## Going deeper 🔴

- **The three-way trade-off.** Every ANN index balances **recall**, **speed (QPS)**, and **memory**.
  You can't max all three; you tune for your constraints. HNSW's `M` and `efSearch`, IVF's `nprobe`
  are the knobs.
- **Build time vs. query time.** HNSW is slower to *build* and heavier in RAM but very fast to
  *query*. IVF is cheaper to build. For frequently-rebuilt indexes this matters.
- **Filtering is hard.** Combining metadata filters with ANN ("nearest vectors *where* year=2024")
  can wreck recall if done naively; mature vector DBs implement careful pre/post-filtering.
- **Disk-based & billion-scale.** Techniques like DiskANN push ANN beyond RAM. The principles are
  the same; the engineering is deeper.
- **Benchmarks.** ann-benchmarks.com compares libraries on the recall/speed frontier — useful when
  choosing.

---

## Pitfalls & gotchas

- **Using the wrong metric.** FAISS `IndexFlatIP` maximizes inner product — normalize your vectors
  so it equals cosine, or use `IndexFlatL2` intentionally.
- **Judging quality by speed alone.** A blazing index with 0.6 recall is silently dropping relevant
  results. Always measure recall against exact search.
- **Rebuilding vs. updating.** Some indexes don't support deletes well; plan how your corpus
  changes.
- **Over-engineering small corpora.** Under ~10⁵ vectors, exact search is often fast enough — don't
  reach for ANN until you need it.

---

## Key terms

approximate nearest neighbor (ANN), recall@k, brute-force search, HNSW, IVF, product quantization
(PQ), vector database, FAISS, Chroma, metadata filtering, quantization. *(See
[GLOSSARY](../../GLOSSARY.md).)*

---

## Check your understanding

1. Why does brute-force search stop being viable as the corpus grows?
2. What exactly does ANN approximate, and how do we measure the cost of that approximation?
3. Give a one-sentence intuition for how HNSW avoids scanning every vector.
4. What does a vector *database* add on top of a raw ANN *index*?
5. You have 5,000 vectors. Should you reach for HNSW? Why or why not?

---

<!-- cyu-answers:start -->

> 💡 *Try answering each question yourself first, then expand to check.*

<details>
<summary><b>Show answer — 1</b></summary>

Its cost is proportional to N (corpus size) x dimensions, so every query scans the whole corpus. As N grows to millions, that linear cost blows past the milliseconds users expect.

</details>

<details>
<summary><b>Show answer — 2</b></summary>

It approximates the **true set of nearest neighbors** — you may miss a few. The cost of that approximation is measured by **recall@k**: the fraction of the exact top-k that the approximate index actually returns.

</details>

<details>
<summary><b>Show answer — 3</b></summary>

It builds a navigable graph linking each vector to near neighbors (with express-lane upper layers), so a query greedily hops toward its neighborhood, visiting only a small subset instead of all vectors.

</details>

<details>
<summary><b>Show answer — 4</b></summary>

**Persistence** (save/reload the index), **metadata + filtering**, **CRUD** (add/update/delete), and serving/scaling — everything around the raw ANN index needed to run it as a real service.

</details>

<details>
<summary><b>Show answer — 5</b></summary>

No — with only 5,000 vectors, exact search is already fast (sub-millisecond) and simpler. ANN pays off at much larger scales; under ~100k vectors, exact search is usually fine.

</details>

<!-- cyu-answers:end -->

## References

- Malkov & Yashunin, *Efficient and robust approximate nearest neighbor search using HNSW graphs* (2016).
- Johnson, Douze & Jégou, *Billion-scale similarity search with GPUs* (FAISS, 2017).
- FAISS and Chroma documentation (open-source tools used here).
- ann-benchmarks.com — recall/speed comparisons across libraries.
- DeepLearning.AI × Cohere, *Large Language Models with Semantic Search*, Lesson 3 (Dense Retrieval; ANN/vector-DB portion) (inspiration).
