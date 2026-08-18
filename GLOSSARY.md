# Glossary

A plain-language dictionary of every key term used across the course. Each entry gives a
one-line definition, a slightly fuller explanation, and the chapter where it's introduced.
Terms are grouped by theme; within each group they're ordered roughly from foundational to
advanced.

> Tip: when a chapter introduces a term, it links back here. As we write chapters, we'll
> keep this file the single source of truth for definitions.

---

## Core search vocabulary

**Information need** — what the user actually wants to know, which they express imperfectly
as a query. *(Ch 1)*

**Query** — the text a user submits to search. *(Ch 1)*

**Document** — a single retrievable unit of text (an article, paragraph, product
description, etc.). *(Ch 1)*

**Corpus** — the full collection of documents you search over. *(Ch 1)*

**Relevance** — how well a document satisfies the user's information need. The thing search
tries to maximize. *(Ch 1)*

**Retrieval** — the act of selecting candidate documents for a query from the corpus. *(Ch 1)*

**Ranking** — ordering retrieved documents so the most relevant appear first. *(Ch 2)*

---

## Classical / lexical search

**Lexical search** — matching on the literal words (lexemes) in the query and documents.
Also called keyword search. *(Ch 2)*

**Tokenization** — splitting text into smaller units (tokens), usually words or subwords. *(Ch 2)*

**Stop words** — extremely common words (the, a, of) often removed because they carry little
meaning. *(Ch 2)*

**Stemming / Lemmatization** — reducing words to a base form ("running" → "run") so variants
match. *(Ch 2)*

**Inverted index** — a lookup table mapping each term to the list of documents containing it;
what makes keyword search fast. *(Ch 2)*

**Term frequency (TF)** — how often a term appears in a document. *(Ch 2)*

**Inverse document frequency (IDF)** — how rare a term is across the corpus; rare terms are
more informative. *(Ch 2)*

**TF-IDF** — a classic score combining TF and IDF to weight terms by importance. *(Ch 2)*

**BM25** — a refined, widely-used ranking function that improves on TF-IDF with length
normalization and saturation. *(Ch 2)*

---

## Vectors & embeddings

**Vector** — an ordered list of numbers; here, a point in a high-dimensional space. *(Ch 3)*

**One-hot encoding** — representing a word as a vector that is all zeros except a single 1.
Sparse and meaning-blind. *(Ch 3)*

**Bag-of-words** — representing a document by its word counts, ignoring order. *(Ch 3)*

**Dense vector** — a compact vector where every dimension carries information (vs. sparse). *(Ch 3)*

**Embedding** — a learned dense vector that captures the *meaning* of text, so similar
meanings sit close together. *(Ch 3/4)*

**Embedding model** — a neural network that maps text to an embedding. *(Ch 4)*

**Dimensionality** — the number of components in a vector (e.g., 384, 768, 1536). *(Ch 4)*

**Cosine similarity** — a measure of closeness based on the angle between two vectors;
1 = same direction, 0 = unrelated. *(Ch 3)*

**Dot product** — multiply-and-sum of two vectors; relates to similarity (equals cosine when
vectors are normalized). *(Ch 3)*

**Normalization** — scaling a vector to unit length so only its direction matters. *(Ch 3)*

**word2vec / GloVe** — early models that learn one fixed vector per word. *(Ch 4)*

**Contextual embeddings** — vectors that depend on surrounding words (e.g., BERT), so "bank"
differs by context. *(Ch 4)*

---

## Semantic retrieval

**Semantic search** — finding documents by meaning rather than exact words. *(Ch 5)*

**Dense retrieval** — semantic search implemented by comparing dense embeddings. *(Ch 5)*

**Bi-encoder** — architecture that embeds query and documents separately, then compares; fast
and scalable. *(Ch 5)*

**Nearest neighbor search** — finding the corpus vectors closest to the query vector. *(Ch 5)*

**Approximate Nearest Neighbor (ANN)** — algorithms that find *almost* the closest vectors far
faster than exact search. *(Ch 6)*

**Vector database** — a system that stores embeddings and serves fast similarity search, with
filtering and persistence. *(Ch 6)*

**FAISS** — a popular open-source library for efficient similarity search over vectors. *(Ch 6)*

**HNSW** — Hierarchical Navigable Small World; a graph-based ANN index, very common. *(Ch 6)*

**IVF (inverted file index)** — an ANN technique that partitions vectors into clusters to
prune the search. *(Ch 6)*

**Product quantization (PQ)** — compressing vectors to save memory while keeping approximate
distances. *(Ch 6)*

---

## Improving results

**Re-ranking** — a second pass that re-scores top candidates more precisely. *(Ch 7)*

**Cross-encoder** — a model that reads query and document *together* for an accurate relevance
score; slow but precise. *(Ch 7)*

**Two-stage retrieval** — retrieve many candidates cheaply, then re-rank a few expensively. *(Ch 7)*

**Hybrid search** — combining lexical (BM25) and semantic (dense) retrieval. *(Ch 8)*

**Reciprocal Rank Fusion (RRF)** — a simple, robust way to merge multiple ranked lists. *(Ch 8)*

---

## Evaluation

**Ground truth / relevance judgments** — human-labeled "correct" results used to score a
system. *(Ch 9)*

**Precision@k** — fraction of the top-k results that are relevant. *(Ch 9)*

**Recall@k** — fraction of all relevant documents found within the top-k. *(Ch 9)*

**Mean Reciprocal Rank (MRR)** — average of 1/(rank of first relevant result). *(Ch 9)*

**nDCG** — Normalized Discounted Cumulative Gain; rewards putting highly-relevant results near
the top. *(Ch 9)*

**MAP** — Mean Average Precision across queries. *(Ch 9)*

---

## Generation & RAG

**Large Language Model (LLM)** — a neural network trained to predict and generate text. *(Ch 0/10)*

**Hallucination** — when an LLM produces fluent but false or unsupported content. *(Ch 10)*

**Retrieval-Augmented Generation (RAG)** — retrieving relevant context and having the LLM
answer using it, for grounded answers. *(Ch 10)*

**Grounding** — tying an answer to retrieved source text so it's verifiable. *(Ch 10)*

**Context window** — the amount of text an LLM can consider at once. *(Ch 10)*

**Chunking** — splitting documents into smaller pieces suitable for embedding and retrieval. *(Ch 11)*

**Chunk overlap** — repeating some text between adjacent chunks so context isn't cut off. *(Ch 11)*

**Ingestion pipeline** — the load → clean → chunk → embed → index process. *(Ch 11)*

---

## Advanced

**Query expansion / rewriting** — improving a query by adding terms or rephrasing it. *(Ch 12)*

**HyDE (Hypothetical Document Embeddings)** — generate a hypothetical answer, embed *that* to
retrieve. *(Ch 12)*

**ColBERT / late interaction** — multi-vector retrieval that compares token-level embeddings. *(Ch 12)*

**Multimodal search** — searching across modalities, e.g., text queries over images. *(Ch 12)*

**Fine-tuning** — further training an embedding model on your own labeled data. *(Ch 12)*

**Agentic RAG** — an LLM agent that plans multiple retrieval/reasoning steps. *(Ch 12)*
