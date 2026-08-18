# Chapter 1 — Foundations of Information Retrieval

> **Level:** 🟢 Beginner  ·  **Status:** 🟩 Complete
> **Prerequisites:** Chapter 0.
> **You'll build:** the vocabulary and the mental model that the whole course stands on.

---

## At a glance

Before we write a single ranking formula, we need to agree on *what search is* and *what
makes it hard*. This chapter defines the handful of words we'll use in every later chapter
(query, document, corpus, relevance, retrieval, ranking), lays out the shape of a search
system, and draws the single most important distinction in the course: **matching words vs.
matching meaning.**

---

## The motivation: a user with a question

Search always starts the same way: a person has something they want to know — an
**information need** — and somewhere out there is text that could satisfy it. The catch is
that the person doesn't hand you their need directly. They hand you a *query*: a short,
imperfect, often ambiguous stand-in for what they actually mean.

> Information need: *"I have a pounding pain on one side of my head — what is it?"*
> Query they type: *"strong pain in the side of the head"*

Your job is to bridge the gap between that messy query and the documents that truly answer it.
Everything in this course is a better and better bridge.

---

## The core vocabulary

These five words appear constantly. Learn them once here.

| Term | Meaning | Example (this course's corpus) |
|------|---------|-------------------------------|
| **Information need** | What the user actually wants to know | "Why does grass look green?" |
| **Query** | The text the user submits | `what color is the grass` |
| **Document** | One retrievable unit of text | The passage titled *"The color of grass"* |
| **Corpus** | The whole collection you search | Our 16 sample passages (later, millions) |
| **Relevance** | How well a document satisfies the need | The grass passage is relevant; the whale one isn't |

Two more describe the *actions* a search system takes:

- **Retrieval** — pulling a set of candidate documents out of the corpus for a query.
- **Ranking** — ordering those candidates so the most relevant sit at the top.

---

## The shape of a search system

At the highest level, every search system looks like this:

```
                    ┌───────────────────────────────────────┐
                    │            SEARCH SYSTEM                │
   query ─────────▶ │                                        │ ─────▶ ranked results
                    │   uses a precomputed INDEX of the      │        (most relevant first)
                    │   CORPUS to retrieve & rank documents  │
                    └───────────────────────────────────────┘
                                     ▲
                                     │ built ahead of time
                              ┌─────────────┐
                              │   CORPUS     │  (all your documents)
                              └─────────────┘
```

The key idea hiding in that picture: **the corpus is processed *before* any query arrives.**
The system builds a data structure called an **index** in advance, so that at query time it
can answer in *milliseconds* instead of re-reading every document. (We build a concrete index —
the *inverted index* — in Chapter 2.)

### Search is usually multi-stage

Real systems rarely do everything in one shot. They split the work into stages:

```
             STAGE 1                         STAGE 2 (optional)
        ┌──────────────┐                ┌──────────────────┐
query ─▶│  RETRIEVAL   │ ─ candidates ─▶│    RE-RANKING    │ ─▶ final results
        │  fast, wide  │   (top ~100)   │  slow, precise   │    (top ~10)
        └──────────────┘                └──────────────────┘
```

- **Stage 1 — Retrieval** casts a wide net *cheaply*. It has to look at the whole corpus, so it
  must be fast. Classic keyword retrieval (BM25, Chapter 2) lives here, and so does semantic
  dense retrieval (Chapter 5).
- **Stage 2 — Re-ranking** takes the small candidate set and reorders it *carefully* using a
  more expensive, more accurate model, and can fold in extra signals like popularity or
  freshness (Chapter 7).

You'll meet both stages repeatedly. Keep the pattern in mind: **retrieve wide and cheap, then
re-rank narrow and precise.**

---

## The one distinction that matters most: words vs. meaning

Here is the crux of the entire course, in one example.

A naïve search system answers a query by counting **shared words** between the query and each
document. Take the query `what color is the grass` against a tiny archive:

```
Query:  what color is the grass

D0  "the grass is green ..."          shared: the, grass, is   → 3   ✅ best
D1  "the sky is blue ..."             shared: the, is          → 2
D2  "the capital of canada is ..."    shared: the, is          → 2
D3  "a whale is a mammal ..."         shared: is               → 1
```

Word-counting gets this right — D0 wins — because the answer literally repeats the query's
words. This is the whole idea behind **keyword (lexical) search**, and it's remarkably
effective and fast. It powered the web for decades.

But now flip the example. Same idea, different phrasing:

```
Query:  strong pain in the side of the head

D2  "A migraine produces a sharp, throbbing sensation localized to one temple ..."
        shared meaningful words with the query: (basically none)  → ~0  ❌ missed!
```

That document is *exactly* the right answer — but it shares almost no words with the query.
"Temple" means "side of the head"; "sensation" means "pain"; "migraine" is the "strong" thing.
A word-counter is blind to all of it. This is the **vocabulary mismatch problem**, and it's the
fundamental limitation of keyword search.

> **Matching words is not the same as matching meaning.** Keyword search matches words.
> The rest of this course is the story of teaching machines to match *meaning* — using
> language models and embeddings (Chapters 3–6) — and of combining both worlds (Chapter 8).

---

## Hands-on

Notebook: [`notebooks/01_words_vs_meaning.ipynb`](notebooks/01_words_vs_meaning.ipynb)

You'll load the course corpus and write a five-line "search" that just counts shared words.
You'll watch it nail the *grass* query and completely miss the *headache* query — feeling the
vocabulary-mismatch problem for yourself. That failure is the motivation for everything that
follows.

---

## Going deeper 🔴

- **Relevance is not binary.** In practice relevance is graded (perfect / good / marginal /
  irrelevant) and *subjective* — two annotators may disagree. Chapter 9 turns this into
  measurable metrics.
- **Precision vs. recall tension.** A system can favor returning only sure-thing results
  (high precision) or casting a wide net to miss nothing (high recall). Different applications
  sit at different points on this trade-off.
- **The query is a lossy encoding of the need.** Much of modern search (query rewriting,
  expansion, HyDE — Chapter 12) is really about reconstructing the underlying need from a thin
  query.

---

## Pitfalls & gotchas

- **Confusing retrieval with ranking.** Retrieval decides *which* documents are candidates;
  ranking decides their *order*. A perfect ranker can't save you if retrieval never surfaced
  the right document.
- **Assuming more shared words = more relevant.** Common words ("the", "is") are shared by
  almost everything and signal nothing. Chapter 2's IDF fixes exactly this.
- **Forgetting the index is precomputed.** Beginners imagine search scans every document live.
  It doesn't — the heavy lifting happens at indexing time.

---

## Key terms

information need, query, document, corpus, relevance, retrieval, ranking, index, vocabulary
mismatch, retrieval stage, re-ranking stage. *(See [GLOSSARY](../../GLOSSARY.md).)*

---

## Check your understanding

1. Explain the difference between an *information need* and a *query* in your own words.
2. Why does a search system build an index *before* any query arrives?
3. Name the two classic stages of a search system and what each optimizes for.
4. Give your own example of two texts that mean the same thing but share no keywords.
5. Why is counting shared words a poor measure of relevance when the words are common?

---

<!-- cyu-answers:start -->

> 💡 *Try answering each question yourself first, then expand to check.*

<details>
<summary><b>Show answer — 1</b></summary>

An **information need** is what the user actually wants to know; the **query** is the short, imperfect text they type to express it. The query is a lossy stand-in for the need.

</details>

<details>
<summary><b>Show answer — 2</b></summary>

So it can answer in milliseconds. Building the **index** ahead of time means the system doesn't have to re-read every document at query time — it just looks up the precomputed structure.

</details>

<details>
<summary><b>Show answer — 3</b></summary>

**Retrieval** (stage 1) casts a wide, cheap net over the whole corpus, optimizing for speed and recall; **re-ranking** (stage 2) reorders the small candidate set precisely, optimizing for accuracy.

</details>

<details>
<summary><b>Show answer — 4</b></summary>

Any true paraphrase works, e.g. *"side of the head hurts"* and *"pain localized to one temple"* — same meaning, essentially no shared content words.

</details>

<details>
<summary><b>Show answer — 5</b></summary>

Common words like *the* and *is* appear in almost every document, so shared counts of them signal nothing about relevance — they inflate scores without indicating meaning. (IDF fixes this in Chapter 2.)

</details>

<!-- cyu-answers:end -->

## References

- Manning, Raghavan & Schütze, *Introduction to Information Retrieval* (free online) — the
  classic textbook for these foundations.
- DeepLearning.AI × Cohere, *Large Language Models with Semantic Search*, Lesson 1 (inspiration).
