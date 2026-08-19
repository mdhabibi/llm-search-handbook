# Chapter 0 — Introduction

> **Level:** 🟢 Beginner  ·  **Status:** 🟩 Complete
> **Prerequisites:** a little Python. No ML background needed.
> **You'll build:** a mental model of the whole search pipeline.

---

## At a glance

This chapter sets the stage. By the end you'll understand *what* semantic search is, *why*
LLMs changed search, and *how* the rest of the course fits together — so every later chapter
has a place to land.

---

## The motivation

Imagine you run a website with thousands of articles — picture a small Wikipedia, or a store
with a big product catalog. People need to *find* things. For decades the answer was
**keyword search**: match the words in the query to the words in the documents.

That works until someone searches for *"how do I stop my laptop from dying so fast"* and your
best article is titled *"Improving battery life on portable computers."* Not a single
important word matches — yet it's exactly the right answer. **Keyword search matches words;
people search by meaning.** Closing that gap is what this course is about.

---

## Intuition first: the four-step pipeline

Everything we build fits one simple pipeline. Keep this picture in your head:

```
            ┌──────────┐     ┌───────────┐     ┌────────────┐     ┌────────────┐
  query ──▶ │ RETRIEVE │ ──▶ │ RE-RANK   │ ──▶ │  GENERATE  │ ──▶ answer
            │ (find    │     │ (reorder  │     │ (LLM writes│
            │ candidates)    │  the best)│     │  from them)│
            └──────────┘     └───────────┘     └────────────┘
              Ch 2,5,6,8        Ch 7              Ch 10,11
```

- **Retrieve** — quickly pull a handful of likely-relevant documents from the whole corpus.
- **Re-rank** *(optional)* — carefully reorder those candidates so the best is on top.
- **Generate** *(optional)* — hand the top results to an LLM so it can write a direct answer
  grounded in them (this is **RAG**).

Some systems stop after Retrieve (a classic search box). Others go all the way to Generate (an
AI assistant that answers questions). You'll build each stage and understand the trade-offs.

---

## What "semantic" adds

The single most important upgrade is in the **Retrieve** step. Instead of matching words, we
convert text into **embeddings** — vectors of numbers that capture *meaning* — and find
documents whose vectors are closest to the query's vector. "Battery life" and "stop my laptop
dying" land near each other in this space even with no shared words. That's **semantic search**,
and Chapters 3–6 build it up from scratch.

---

## How to use this repo

1. Do the [setup](../../setup/SETUP.md) once.
2. Read chapters in order if you're new; jump around using the
   [roadmap](../../ROADMAP.md) if you're experienced.
3. Read each chapter's README, then run its `notebooks/` to see the idea in code.
4. Keep the [glossary](../../GLOSSARY.md) open in a tab.

---

## Hands-on

Notebook: [`notebooks/00_pipeline_tour.ipynb`](notebooks/00_pipeline_tour.ipynb) — a 5-minute
end-to-end demo: stand up a search system in three lines with the course's `SearchStack`, ask it
questions in plain English, and watch it answer by *meaning* — so you see the destination before
learning to build each part.

---

## Slides

📊 **[Chapter 0 slide deck (PDF)](../../slides/Chapter-00-Introduction.pdf)** — a visual intro:
beyond keywords, to meaning.

---

## Key terms

Large Language Model (LLM), embedding, retrieval, ranking, semantic search, RAG. *(See
[GLOSSARY](../../GLOSSARY.md).)*

---

## Check your understanding

1. In one sentence, why does keyword search miss relevant results?
2. What does the "Retrieve" step do, and how does "semantic" change it?
3. Which pipeline stages are optional, and when would you skip them?

---

<!-- cyu-answers:start -->

> 💡 *Try answering each question yourself first, then expand to check.*

<details>
<summary><b>Show answer — 1</b></summary>

Because it matches literal *words*, not *meaning*: if the best document phrases the same idea with different words, keyword search sees no overlap and misses it.

</details>

<details>
<summary><b>Show answer — 2</b></summary>

**Retrieve** quickly pulls a small set of likely-relevant documents from the whole corpus. Making it *semantic* means comparing the *meaning* of the query and documents (via embeddings) instead of shared words, so paraphrases still match.

</details>

<details>
<summary><b>Show answer — 3</b></summary>

**Re-rank** and **Generate** are optional. Skip re-ranking when first-stage results are already good enough or latency is tight; skip generation when you just want to return passages (a search box) rather than a written answer.

</details>

<!-- cyu-answers:end -->

## References

- DeepLearning.AI × Cohere — *Large Language Models with Semantic Search* (course inspiration).
- Links to primary sources are added as we write later chapters.
