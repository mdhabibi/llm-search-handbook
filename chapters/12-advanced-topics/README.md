# Chapter 12 — Advanced Topics

> **Level:** 🔴 Advanced  ·  **Status:** 🟩 Complete
> **Prerequisites:** Chapters 5–11.
> **You'll build:** familiarity with the techniques that push retrieval beyond the core pipeline —
> and one runnable late-interaction demo.

---

## At a glance

Once the core stack (retrieve → fuse → re-rank → generate) is solid, these techniques squeeze out
more quality or unlock new capabilities. Treat this as a **menu of deeper dives**: each section is a
concept plus a pointer to primary sources, and the notebook includes concrete demos — most notably a
from-scratch **ColBERT-style late-interaction** score you can run and inspect.

---

## 1. Query understanding: the query is a lossy clue

The user's query is a thin, imperfect stand-in for their information need (Chapter 1). Several
techniques reconstruct a better one:

- **Query expansion** — add synonyms/related terms so keyword and dense retrieval match more.
  *"heart attack"* → *"heart attack, myocardial infarction, MI"*.
- **Query rewriting** — rephrase a messy or conversational query into a clean search query (crucial
  in chat: *"and what about its capital?"* → *"what is the capital of Australia?"*).
- **HyDE (Hypothetical Document Embeddings)** — a clever trick: ask an LLM to *write a hypothetical
  answer* to the query, then embed **that** and retrieve with it. A fake answer is often closer in
  embedding space to the real answer passages than the short question is.

```
HyDE:  question ──LLM──▶ hypothetical answer ──embed──▶ retrieve real passages
```

---

## 2. Multi-vector retrieval (ColBERT) & late interaction

A bi-encoder (Chapter 5) squashes a whole passage into **one** vector — lossy. A cross-encoder
(Chapter 7) is accurate but can't precompute. **ColBERT** is the middle ground: represent each text
as **one vector per token**, and score a query–document pair with **MaxSim** — for each query token,
take its best-matching document token, then sum:

$$\text{score}(q,d) = \sum_{i \in q} \max_{j \in d} \; \cos(\mathbf{q}_i, \mathbf{d}_j)$$

This "late interaction" keeps token-level detail (more accurate than a single vector) while still
allowing document token vectors to be **precomputed** (scalable, unlike a cross-encoder). The
notebook implements MaxSim in a few lines of numpy so you can see exactly how it rewards fine-grained
matches.

---

## 3. Multilingual & multimodal search

- **Multilingual** — models trained on many languages place *"dog"* and *"perro"* near each other, so
  a query in one language retrieves documents in another. One embedding space, many languages.
- **Multimodal** — models like CLIP embed **images and text into the same space**, so a text query
  can retrieve images (and vice versa). Same nearest-neighbor machinery, new modality. Extends to
  audio and video.

---

## 4. Fine-tuning embedding models

Off-the-shelf models are general. If your domain is unusual (legal, medical, code, your product's
jargon), **fine-tuning** on your own (query, relevant-passage) pairs — usually with contrastive
learning — can lift retrieval quality substantially. The cost is building training data and a
training loop; the payoff is a space shaped to *your* notion of relevance.

---

## 5. Agentic RAG & multi-step retrieval

Simple RAG retrieves once and answers. Hard questions need more:

- **Multi-hop** — decompose a question, retrieve for each part, combine (*"Which is older, the
  company that makes X or the one that makes Y?"* needs two lookups).
- **Iterative / agentic** — an LLM *agent* decides what to search, reads results, and searches again
  until it can answer — a loop of retrieve→reason→retrieve.
- **Tool use** — the agent chooses among tools (search, calculator, SQL, web) per step.

More powerful, but harder to control, evaluate, and keep cheap — use when single-shot RAG genuinely
falls short.

---

## Hands-on

Notebook: [`notebooks/12_advanced_topics.ipynb`](notebooks/12_advanced_topics.ipynb)

You will:

1. Do simple **query expansion** and see recall change.
2. Trace the **HyDE** flow (with a mock generator so it runs anywhere).
3. Implement **ColBERT-style MaxSim late interaction** from scratch in numpy and compare it to
   single-vector cosine on a crafted example.
4. See a sketch of **multimodal** (shared-space) retrieval and where to plug in CLIP.

> The MaxSim and query-expansion demos run fully offline. HyDE and real embedding/CLIP steps are
> written to plug into a model on your machine.

---

## Slides

📊 **[Chapter 12 slide deck (PDF)](../../slides/Chapter-12-Advanced-Topics.pdf)** — a visual summary
of advanced retrieval techniques.

---

## Going deeper 🔴

- **HyDE caveats.** It adds an LLM call (latency/cost) and can hurt when the model hallucinates a
  misleading hypothetical. Measure before adopting.
- **ColBERT storage.** One vector per token means much larger indexes; production uses compression
  and specialized indexes (PLAID).
- **Cross-encoder vs. ColBERT vs. bi-encoder.** A spectrum of accuracy/cost: bi-encoder (cheapest) →
  ColBERT (mid) → cross-encoder (most accurate, most expensive). Pick per stage and budget.
- **Evaluation still rules.** Every technique here should earn its place by improving Chapter 9
  metrics on *your* data, not by reputation.

---

## Pitfalls & gotchas

- **Adding complexity without measuring.** Each advanced trick adds latency/cost/failure modes;
  justify it with metrics.
- **HyDE/agent loops without guards.** Unbounded LLM steps blow up cost and latency; cap them.
- **Assuming multilingual/multimodal models are as strong as specialized ones.** Often a trade-off;
  verify on your task.
- **Fine-tuning on tiny or biased data.** You can overfit and *worsen* general retrieval; you need
  enough diverse pairs.

---

## Key terms

query expansion, query rewriting, HyDE, ColBERT, late interaction, MaxSim, multi-vector retrieval,
multilingual embeddings, multimodal search, CLIP, fine-tuning, contrastive learning, agentic RAG,
multi-hop retrieval. *(See [GLOSSARY](../../GLOSSARY.md).)*

---

## Check your understanding

1. Explain HyDE in one sentence and why embedding a *hypothetical answer* can beat embedding the
   question.
2. What does ColBERT keep that a bi-encoder throws away, and how does MaxSim use it?
3. Why can ColBERT precompute document vectors while a cross-encoder can't?
4. How does multimodal search reuse the exact machinery from Chapter 5?
5. When is agentic/multi-step RAG worth its extra cost over single-shot RAG?

---

<!-- cyu-answers:start -->

> 💡 *Try answering each question yourself first, then expand to check.*

<details>
<summary><b>Show answer — 1</b></summary>

HyDE asks an LLM to write a **hypothetical answer** to the query and retrieves using that answer's embedding. It helps because a full answer-like passage sits closer in embedding space to the real answer passages than a short, sparse question does.

</details>

<details>
<summary><b>Show answer — 2</b></summary>

It keeps **token-level (per-token) vectors** instead of squashing the text into one vector. **MaxSim** scores a pair by, for each query token, taking its best-matching document token's similarity and summing — preserving fine-grained matches.

</details>

<details>
<summary><b>Show answer — 3</b></summary>

Because ColBERT embeds each document's tokens **independently of the query**, so those token vectors can be precomputed and stored. A cross-encoder must read query and document jointly, so nothing can be precomputed.

</details>

<details>
<summary><b>Show answer — 4</b></summary>

A multimodal model (e.g. CLIP) embeds images and text into **one shared space**, so a text query vector can be compared to image vectors with the **same nearest-neighbor search** used for text-to-text retrieval in Chapter 5.

</details>

<details>
<summary><b>Show answer — 5</b></summary>

When a single retrieve-then-answer pass isn't enough — e.g. **multi-hop** questions needing several lookups, or queries requiring reasoning/tools between retrievals. It costs more latency and complexity, so reserve it for questions single-shot RAG genuinely can't handle.

</details>

<!-- cyu-answers:end -->

## References

- Gao et al., *Precise Zero-Shot Dense Retrieval without Relevance Labels* (HyDE, 2022).
- Khattab & Zaharia, *ColBERT: Efficient and Effective Passage Search via Contextualized Late
  Interaction over BERT* (2020).
- Radford et al., *Learning Transferable Visual Models from Natural Language Supervision* (CLIP, 2021).
- Reimers & Gurevych, multilingual sentence-transformers.
- DeepLearning.AI × Cohere, *Large Language Models with Semantic Search* (inspiration).
