# Chapter 13 — Capstone Project

> **Level:** 🟡 Intermediate  ·  **Status:** 🟩 Complete
> **Prerequisites:** All previous chapters.
> **You'll build:** a complete semantic-search + RAG system end to end, over a corpus you care
> about, and assess it against a rubric.

---

## At a glance

This is where everything converges. Across twelve chapters you built each piece in isolation —
keyword search, embeddings, dense retrieval, vector indexes, re-ranking, fusion, evaluation, RAG,
chunking. The capstone connects them into **one working answer engine** and asks you to run it on
*your own* documents. The notebook provides a **reference implementation** (a `SearchStack` class)
you can study, then adapt.

---

## The full stack you're assembling

```
   YOUR DOCUMENTS
        │
        ▼
   ┌──────────┐   Ch 11        ┌──────────────────────────────┐
   │ INGEST   │  load→clean→   │  index: BM25 (Ch2) +          │
   │          │  chunk→embed → │  dense vectors (Ch4–6)        │
   └──────────┘                └──────────────────────────────┘
        │                                   │
   user question ──▶  RETRIEVE (hybrid: BM25 ∪ dense, RRF — Ch5,8)
                          │
                          ▼
                      RE-RANK (cross-encoder — Ch7)
                          │
                          ▼
                      GENERATE (grounded RAG answer + citations — Ch10)
                          │
                          ▼
                      EVALUATE (precision/MRR/nDCG — Ch9)
```

Every arrow is a chapter you've already done. The capstone is the wiring — and the judgment about
which pieces your use case actually needs.

---

## Step 1 — Choose a corpus and use case

Pick something you'll enjoy querying and can judge relevance for:

- Your own notes / a wiki / documentation.
- A set of articles, papers, or blog posts on a topic.
- A product catalog or FAQ.
- Meeting transcripts or a book.

Write down the **use case**: is it a search box (return passages) or a Q&A assistant (return
answers)? That decides whether you stop at retrieval or go all the way to RAG, and which metric
matters (nDCG for ranking; MRR/answer-quality for single-answer).

---

## Step 2 — Build the stack

The notebook's `SearchStack` wires the pieces together with sensible defaults. In outline:

```python
stack = SearchStack(
    encode_fn  = embedder.encode,      # Ch4 (encode_fn = any list[str] -> vectors callable)
    chunker    = sentence_chunks,      # Ch11
    reranker   = cross_encoder,        # Ch7  (pass None to skip re-ranking)
    generator  = my_llm,               # Ch10 (pass None for search-only)
    use_hybrid = True,                 # Ch2 + Ch5 + Ch8 (RRF)
).ingest(my_documents)                 # Ch11 pipeline

stack.search("a question")     # ranked passages
stack.answer("a question")     # grounded RAG answer + citations
stack.evaluate(my_eval_set)    # Ch9 metrics
```

Start minimal (dense only), confirm it works, then switch on hybrid, re-ranking, and RAG one at a
time — **measuring after each** so you know which additions actually help on *your* data.

---

## Step 3 — Evaluate honestly

Build a small labeled set (10–30 queries with relevant doc/chunk ids — the more the better) as in
Chapter 9, and report metrics for each configuration:

```
config                 nDCG@10   MRR    notes
dense only              ...      ...
+ hybrid (RRF)          ...      ...
+ cross-encoder rerank  ...      ...
```

Let the numbers — not vibes — decide your final configuration. Note where the system still fails;
that's your roadmap.

---

## Self-assessment rubric

Score your project honestly. Each item is a level you can reach.

| Area | Baseline | Good | Excellent |
|------|----------|------|-----------|
| **Ingestion** | Loads & chunks one doc type | Cleans + chunks with overlap + metadata | Handles multiple formats; caching/re-index |
| **Retrieval** | Dense retrieval works | Hybrid (BM25 + dense, RRF) | Hybrid + re-rank, tuned by measurement |
| **Generation** | Returns passages | Grounded RAG answers | Citations + refusal on unanswerable |
| **Evaluation** | A few queries eyeballed | Labeled set + precision/recall | nDCG/MRR across configs, dev/test split |
| **Engineering** | Runs in a notebook | Reusable functions/classes | Config-driven, documented, reproducible |
| **Understanding** | Can run it | Can explain each stage | Can justify every design choice & trade-off |

Aim for at least **Good** across the board before reaching for **Excellent** anywhere — a balanced
system beats one spiky part.

---

## Hands-on

Notebook: [`notebooks/13_capstone.ipynb`](notebooks/13_capstone.ipynb)

The notebook provides the `SearchStack` reference implementation wired over the course corpus, plus
a clearly marked **"bring your own corpus"** cell. You will:

1. Ingest documents (chunk → embed → index).
2. Retrieve with hybrid search and re-rank.
3. Generate grounded answers with citations.
4. Evaluate configurations and pick a winner.
5. Swap in your own corpus and repeat.

> The wiring/logic runs with mock components in-sandbox; embeddings, cross-encoder, and LLM run on
> your machine (or via an API).

---

## Extension ideas (make it a portfolio piece)

- **A UI** — wrap it in a small Streamlit/Gradio app with a search box and answer panel.
- **Persistence & scale** — move to a persistent vector DB (Chroma/FAISS on disk); handle updates.
- **Deployment** — expose a `/search` and `/answer` API; add caching and logging.
- **New modality** — add image search with CLIP (Chapter 12).
- **Better evaluation** — grow the labeled set; add answer-faithfulness checks.
- **Advanced retrieval** — try HyDE, ColBERT, or a fine-tuned embedding model (Chapter 12) and
  measure the lift.

---

## You've finished the course 🎉

You can now explain *and build* a modern search system from keyword matching to grounded RAG,
measure it properly, and make deliberate engineering trade-offs. That's the full arc from
"matching words" to "matching meaning" — and shipping it.

Revisit the [ROADMAP](../../ROADMAP.md) to review, the [GLOSSARY](../../GLOSSARY.md) to lock in
terms, and any chapter's *Going Deeper* section to specialize.

---

## Check your understanding

1. For your use case, do you need RAG or is retrieval enough? Justify it.
2. Which single addition (hybrid, re-rank, RAG) gave the biggest measured lift, and why?
3. Where does your system still fail, and which chapter's technique would you try next?
4. If latency had to drop 5×, what would you cut first, and what quality cost would you accept?
5. Explain your final configuration to someone who's read only Chapter 1.

---

<!-- cyu-answers:start -->

> 💡 *Try answering each question yourself first, then expand to check.*

<details>
<summary><b>Show answer — 1</b></summary>

*(Reflective — model answer.)* Choose **retrieval only** if users just need to find and read source passages (a search box); choose **RAG** if they need a synthesized, direct answer. Justify by the user's task and whether a written, citable answer adds value over a ranked list.

</details>

<details>
<summary><b>Show answer — 2</b></summary>

*(Reflective.)* Report it from your own measurements. Typically **hybrid** helps most when queries mix exact terms and intent; **re-ranking** helps most when first-stage recall is good but ordering is off; **RAG** helps when users want answers, not passages. The right answer is whichever moved your Chapter 9 metrics most on *your* data.

</details>

<details>
<summary><b>Show answer — 3</b></summary>

*(Reflective.)* Identify the failing query type, then map it to a technique: missed synonyms -> better embeddings/hybrid (Ch4/8); wrong ordering -> re-ranking (Ch7); answer not in a chunk -> chunking (Ch11); hallucinated answers -> prompt grounding (Ch10); missed exact terms -> hybrid (Ch8).

</details>

<details>
<summary><b>Show answer — 4</b></summary>

*(Reflective.)* Usually drop the most expensive stage first — the **cross-encoder re-ranker** (or shrink its candidate set), then consider ANN over exact search. Accept the resulting small drop in nDCG/MRR; measure it so the latency/quality trade-off is explicit.

</details>

<details>
<summary><b>Show answer — 5</b></summary>

*(Reflective.)* In plain terms: "We turn every document into numbers that capture meaning, find the ones closest to the question, [optionally re-check the top few carefully], and [optionally] let an AI write an answer using only those documents." Tie each piece back to the words-vs-meaning idea from Chapter 1.

</details>

<!-- cyu-answers:end -->

## References

- Every prior chapter of this course.
- Lin, Nogueira & Yates, *Pretrained Transformers for Text Ranking: BERT and Beyond* (2021) — a
  broad survey tying these pieces together.
- DeepLearning.AI × Cohere, *Large Language Models with Semantic Search* (inspiration).
