# Roadmap & Curriculum

This document is the **master plan** for the repo. It describes every chapter, what it
covers, why it comes where it does, and how the chapters build on one another. Use it to
navigate, to track progress, and to decide where to jump in.

The course is organized into **seven parts** that move from "search before AI" all the
way to "ship a grounded AI answer engine."

```
PART I    Foundations         →  Ch 0–1   Why search is hard
PART II   Classical Search    →  Ch 2     Keyword / lexical retrieval
PART III  The Vector Toolkit  →  Ch 3–4   Turning text into meaning-vectors
PART IV   Semantic Retrieval  →  Ch 5–6   Search by meaning, at scale
PART V    Better Results      →  Ch 7–8   Re-ranking & hybrid search
PART VI   Measuring Quality   →  Ch 9     Evaluation
PART VII  Generation          →  Ch 10–11 RAG & production
EXTRA     Mastery             →  Ch 12–13 Advanced topics & capstone
```

---

## How each chapter is structured

To keep the experience consistent, **every chapter README** follows the same template:

1. **At a glance** — difficulty, prerequisites, what you'll build.
2. **The motivation** — the concrete problem this chapter solves (with a story/example).
3. **Intuition first** — the idea explained with analogies and diagrams, no jargon.
4. **The mechanics** — how it actually works, step by step, with a worked example.
5. **Hands-on** — pointer to the chapter's notebook(s) with our own code and data.
6. **Going deeper 🔴** — math, trade-offs, and advanced notes for experts.
7. **Pitfalls & gotchas** — common mistakes and how to avoid them.
8. **Key terms** — chapter glossary entries (also collected in the global GLOSSARY).
9. **Check your understanding** — short questions / exercises.
10. **References** — papers, docs, and further reading.

---

## PART I — Foundations

### Chapter 0 — Introduction
- What "semantic search" means and why LLMs changed search.
- The mental model: **query → retrieve → (re-rank) → (generate)**.
- A tour of the whole pipeline you'll build by the end.
- How to use this repo, set up your environment, and run notebooks.

### Chapter 1 — Foundations of Information Retrieval
- The core problem: a user has an *information need*; you have a pile of documents.
- Documents, queries, corpus, relevance — the vocabulary of search.
- Why exact-match matching is brittle (synonyms, phrasing, intent).
- A first look at the difference between **matching words** and **matching meaning**.

---

## PART II — Classical Search

### Chapter 2 — Keyword / Lexical Search
- The **inverted index**: how search engines find documents fast.
- Scoring with **TF-IDF**: term frequency × inverse document frequency, explained intuitively.
- **BM25**: the workhorse ranking function still used everywhere today.
- Tokenization, stemming, stop words.
- **Hands-on:** build a tiny keyword search engine over a sample corpus; rank with BM25.
- Limits of lexical search → motivation for embeddings.

---

## PART III — The Vector Toolkit

### Chapter 3 — From Text to Vectors
- Why computers need numbers, not words.
- One-hot encoding and bag-of-words — and why they miss meaning.
- The leap to **dense vectors**: similar meaning → nearby vectors.
- Measuring closeness: dot product, **cosine similarity**, Euclidean distance.
- **Hands-on:** visualize simple word/sentence vectors in 2D.

### Chapter 4 — Embeddings Deep Dive
- What an **embedding model** is and what it learns.
- Word vs. sentence vs. document embeddings.
- A short history: word2vec/GloVe → contextual (BERT) → sentence embeddings.
- Using a modern open-source embedding model (`sentence-transformers`).
- Properties: dimensionality, normalization, semantic arithmetic.
- **Hands-on:** embed sentences, explore nearest neighbors, cluster by meaning.

---

## PART IV — Semantic Retrieval

### Chapter 5 — Dense Retrieval & Semantic Search
- The big idea: embed the corpus once, embed the query, find nearest vectors.
- The **bi-encoder** architecture (two towers).
- Building semantic search end to end over our own dataset.
- Where dense retrieval beats keyword search — and where it doesn't.
- **Hands-on:** a working semantic search engine you query in natural language.

### Chapter 6 — Vector Databases & Approximate Nearest Neighbor (ANN)
- Why brute-force search breaks at scale.
- **ANN** intuition: trading a little accuracy for huge speed.
- Index types: IVF, **HNSW**, product quantization (conceptually).
- Using **FAISS** and a vector DB (e.g., Chroma) for persistence and filtering.
- **Hands-on:** index thousands of vectors and query in milliseconds.

---

## PART V — Better Results

### Chapter 7 — Re-ranking
- Why first-stage retrieval returns "good enough," not "best."
- **Cross-encoders**: reading query + document together for a precise score.
- The two-stage pattern: retrieve many cheaply → re-rank a few precisely.
- **Hands-on:** add a re-ranker and measure the quality jump.

### Chapter 8 — Hybrid Search
- Keyword search and semantic search have complementary strengths.
- Combining scores: weighted fusion and **Reciprocal Rank Fusion (RRF)**.
- When hybrid wins (names, codes, rare terms + fuzzy intent).
- **Hands-on:** fuse BM25 + dense retrieval and compare.

---

## PART VI — Measuring Quality

### Chapter 9 — Evaluating Search
- You can't improve what you don't measure.
- Building a relevance test set (queries + judged results).
- Metrics: precision@k, recall@k, **MRR**, **nDCG**, MAP — what each tells you.
- Offline vs. online evaluation; A/B testing basics.
- **Hands-on:** evaluate and compare every retriever we've built so far.

---

## PART VII — Generation

### Chapter 10 — RAG: Retrieval-Augmented Generation
- The problem with asking an LLM straight: hallucination, stale knowledge.
- **RAG**: retrieve relevant context, then have the LLM answer *from it*.
- Anatomy of a RAG prompt; grounding and citations.
- **Hands-on:** build a question-answering app over our corpus (open-source LLM option).

### Chapter 11 — Chunking & Production Pipelines
- Splitting documents: fixed, sentence, semantic chunking; overlap and metadata.
- The full ingestion pipeline: load → clean → chunk → embed → index.
- Caching, batching, freshness, monitoring, cost.
- Failure modes and how to debug a RAG system.
- **Hands-on:** a reusable, configurable ingestion + retrieval pipeline.

---

## EXTRA — Mastery

### Chapter 12 — Advanced Topics 🔴
- Query understanding: expansion, rewriting, HyDE.
- Multi-vector retrieval (**ColBERT**) and late interaction.
- Multilingual and **multimodal** (text + image) search.
- Fine-tuning embedding models on your own data.
- **Agentic RAG** and multi-step retrieval.

### Chapter 13 — Capstone Project
- Pick a corpus (docs, articles, product catalog, your notes).
- Build the full stack: ingest → hybrid retrieve → re-rank → RAG answer → evaluate.
- A rubric to assess your own system.
- Ideas for extending it into a portfolio piece.

---

## Suggested learning tracks

- **"I just want to understand it"** → Chapters 0, 1, 2, 3, 4, 5, 10.
- **"I want to build a RAG app"** → Chapters 0, 4, 5, 6, 10, 11, then 7–9 to improve it.
- **"I want depth/research"** → All chapters, including every *Going Deeper 🔴* section, plus 12.

---

## Progress tracker

| # | Chapter | Status |
|---|---------|--------|
| 0 | Introduction | 🟩 Complete |
| 1 | Foundations of Information Retrieval | 🟩 Complete |
| 2 | Keyword / Lexical Search | 🟩 Complete |
| 3 | From Text to Vectors | 🟩 Complete |
| 4 | Embeddings Deep Dive | 🟩 Complete |
| 5 | Dense Retrieval & Semantic Search | 🟩 Complete |
| 6 | Vector Databases & ANN | 🟩 Complete |
| 7 | Re-ranking | 🟩 Complete |
| 8 | Hybrid Search | 🟩 Complete |
| 9 | Evaluating Search | 🟩 Complete |
| 10 | RAG | 🟩 Complete |
| 11 | Chunking & Production Pipelines | 🟩 Complete |
| 12 | Advanced Topics | 🟩 Complete |
| 13 | Capstone Project | 🟩 Complete |

> Update a row to 🟨 In progress / 🟩 Complete as we flesh out each chapter from your shared studies.
