# Chapter 11 — Chunking & Production Pipelines

> **Level:** 🟡 Intermediate → 🔴 Advanced  ·  **Status:** 🟩 Complete
> **Prerequisites:** Chapter 10 (RAG).
> **You'll build:** chunking strategies and a reusable ingestion pipeline — the engineering that
> turns a notebook demo into something real.

---

## At a glance

Our course corpus is 16 tidy one-paragraph passages. Real documents are long, messy, and plentiful:
a 40-page PDF, a wiki with thousands of articles, a folder of transcripts. Before any of it can be
searched, it has to be **loaded, cleaned, chunked, embedded, and indexed**. This chapter covers
that ingestion pipeline — with **chunking** as the highest-leverage decision — plus the operational
concerns (freshness, cost, debugging) that separate a demo from a system.

---

## Why chunk at all?

You can't embed a whole book as one vector. Three reasons chunking is mandatory:

1. **Model input limits.** Embedding models truncate long inputs (a few hundred tokens). Feed a
   whole document and everything past the limit is silently dropped.
2. **Retrieval precision.** One vector for a long document averages many topics into a blur. A user
   asking about page 30 shouldn't be matched to a vector dominated by pages 1–29. Smaller chunks =
   sharper matches.
3. **Answer quality (RAG).** You want to hand the LLM the *relevant paragraph*, not the whole
   document — it's cheaper and less distracting (recall "lost in the middle" from Chapter 10).

So: **split documents into chunks, embed each chunk, retrieve chunks.** The document id travels
along as metadata so you can still cite the source.

---

## Chunking strategies

Implemented in [`src/chunking.py`](../../src/chunking.py).

### Fixed-size (by words or tokens)
Cut every *N* words with an **overlap** of *O* words between neighbors.

```
size=40, overlap=10:
[ words 1–40 ][ words 31–70 ][ words 61–100 ]
              └─overlap─┘     └─overlap─┘
```

Simple and predictable. The **overlap** matters: without it, a sentence spanning a boundary gets cut
in half and neither chunk contains the whole thought. Overlap re-includes the seam so context
survives.

### Sentence-based
Group *whole sentences* (e.g., 3 at a time, overlapping by 1). Chunks read naturally because they
never cut mid-sentence — usually better than fixed-size for prose.

### Semantic chunking
Split where the *topic* shifts (detected by drops in similarity between consecutive sentences).
Smartest but most complex; great for heterogeneous documents.

### Choosing size & overlap
- **Too small:** chunks lack context; the answer is split across several chunks.
- **Too large:** chunks blur multiple topics; retrieval precision drops; more tokens per LLM call.
- **Rule of thumb:** start ~200–500 tokens with ~10–20% overlap, then **tune by measuring**
  (Chapter 9). There is no universal best — it depends on your documents and queries.

---

## The ingestion pipeline

Every production RAG system has the same backbone:

```
   LOAD  ──▶  CLEAN  ──▶  CHUNK  ──▶  EMBED  ──▶  INDEX
   (read      (strip     (split     (Ch 4)     (Ch 6 vector DB,
    files)     boilerplate, into                 with chunk text +
               normalize)  chunks)               source metadata)
```

- **Load** — read PDFs, HTML, Markdown, transcripts into raw text.
- **Clean** — strip navigation/boilerplate, fix encoding, normalize whitespace.
- **Chunk** — apply a strategy above; attach metadata (`doc_id`, `title`, position).
- **Embed** — encode each chunk (batch for speed).
- **Index** — store vectors + chunk text + metadata in a vector database (Chapter 6).

The notebook builds a small, configurable `IngestionPipeline` class that runs this end to end and
lets you swap the chunker and embedder.

---

## Operating it (the unglamorous but essential part)

- **Batching.** Embed chunks in batches, not one at a time — often 10–100× faster.
- **Caching.** Don't re-embed unchanged documents; hash content and skip if seen.
- **Freshness / re-indexing.** Documents change. Decide on full rebuilds vs. incremental
  upserts/deletes, and how often.
- **Cost & latency.** Embedding and generation dominate cost. Measure tokens, batch, and cache.
- **Monitoring.** Track retrieval hit rate, latency, and answer quality over time — regressions are
  invisible without it.

---

## Debugging a RAG system

When answers are bad, localize the failure — don't randomly tweak the prompt:

```
Bad answer?
  ├─ Was the right chunk retrieved?  ──no──▶  RETRIEVAL problem
  │     → check chunking (too big/small?), embedding model, query, k, hybrid/rerank
  └─ Right chunk retrieved but answer still wrong?  ──▶ GENERATION problem
        → check the prompt (grounding/refusal), context budget, the model
```

The single most common root cause is **retrieval, not generation** — and often the fix is
*chunking*. Print what was retrieved before touching anything else.

---

## Hands-on

Notebook: [`notebooks/11_chunking_and_pipelines.ipynb`](notebooks/11_chunking_and_pipelines.ipynb)

You will:

1. Apply fixed-size (with overlap) and sentence-based chunking to a long document and compare.
2. See *why* overlap matters with a boundary-straddling sentence.
3. Build a configurable `IngestionPipeline` (load → clean → chunk → embed → index).
4. Show that chunking a long document improves retrieval precision over embedding it whole.
5. Walk the retrieval-vs-generation debugging checklist on a deliberately broken example.

> Chunking logic and the pipeline scaffold run offline. The embed/index steps use the model +
> Chroma (your machine).

---

## Slides

📊 **[Chapter 11 slide deck (PDF)](../../slides/Chapter-11-Chunking-and-Pipelines.pdf)** — a visual
summary of chunking and production ingestion pipelines.

---

## Going deeper 🔴

- **Token vs. word chunking.** Embed limits are in *tokens*; word counts approximate. For precise
  control, chunk by tokens with the model's tokenizer (e.g., `tiktoken`).
- **Metadata-rich chunks.** Store section headers, page numbers, timestamps — they power filtering
  (Chapter 6) and better citations.
- **Parent-document / small-to-big retrieval.** Retrieve on small chunks for precision but hand the
  LLM the surrounding *parent* passage for context. A popular, effective pattern.
- **Deduplication & near-duplicates.** Large corpora have repeats; dedupe to avoid burning context
  and skewing retrieval.
- **Incremental indexing at scale.** Upserts, tombstones for deletes, and background re-embedding
  keep a live index fresh without full rebuilds.

---

## Pitfalls & gotchas

- **No overlap.** Answers that straddle chunk boundaries get lost. Always overlap a little.
- **One-size-fits-all chunking.** Code, tables, and prose want different strategies; don't force
  one.
- **Chunking away structure.** Splitting mid-table or mid-code-block destroys meaning; respect
  structural boundaries.
- **Forgetting metadata.** Without `doc_id`/position you can't cite sources or filter — cripples
  RAG trust.
- **Re-embedding everything on every change.** Cache; embed only what changed.

---

## Key terms

chunking, chunk size, chunk overlap, fixed-size chunking, sentence chunking, semantic chunking,
ingestion pipeline, batching, caching, re-indexing, parent-document retrieval, upsert. *(See
[GLOSSARY](../../GLOSSARY.md).)*

---

## Check your understanding

1. Give three reasons you must chunk long documents before embedding them.
2. What problem does chunk *overlap* solve? What goes wrong without it?
3. Describe the five stages of an ingestion pipeline in order.
4. A RAG answer is wrong. What's the first thing to check, and why?
5. Why is there no universal best chunk size, and how do you find a good one for your data?

---

<!-- cyu-answers:start -->

> 💡 *Try answering each question yourself first, then expand to check.*

<details>
<summary><b>Show answer — 1</b></summary>

(1) Embedding models have **input limits** and silently truncate long text; (2) one vector for a long document **blurs many topics**, hurting retrieval precision; (3) for RAG you want to hand the LLM the **relevant paragraph**, not a whole document (cheaper, less distracting).

</details>

<details>
<summary><b>Show answer — 2</b></summary>

Overlap prevents a thought that **straddles a chunk boundary** from being cut in half so neither chunk contains it. Without overlap, answers spanning a seam are lost because no single chunk holds the complete context.

</details>

<details>
<summary><b>Show answer — 3</b></summary>

**Load -> Clean -> Chunk -> Embed -> Index.** (Read raw text, strip boilerplate/normalize, split into chunks with metadata, encode each chunk, store vectors + text + metadata in a vector DB.)

</details>

<details>
<summary><b>Show answer — 4</b></summary>

**What was actually retrieved.** Most RAG failures are retrieval failures; if the right chunk wasn't retrieved, fix retrieval/chunking, not the prompt. Only if the right chunk *was* retrieved do you debug the generation step.

</details>

<details>
<summary><b>Show answer — 5</b></summary>

Because it depends on your documents and queries: too small loses context, too large blurs topics and wastes tokens. Find a good value by **measuring** (Chapter 9 metrics) across a few sizes/overlaps on your own data.

</details>

<!-- cyu-answers:end -->

## References

- Liu et al., *Lost in the Middle* (2023) — why context size and placement matter.
- LangChain / LlamaIndex documentation on text splitters and ingestion (concepts, not required).
- `tiktoken` for token-accurate chunking.
- DeepLearning.AI × Cohere, *Large Language Models with Semantic Search* (inspiration).
