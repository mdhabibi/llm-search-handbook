# Chapter 10 — RAG: Retrieval-Augmented Generation

> **Level:** 🟡 Intermediate  ·  **Status:** 🟩 Complete
> **Prerequisites:** Chapter 5 (dense retrieval). Chapters 6–9 helpful.
> **You'll build:** a grounded question-answering app over your own corpus.

---

## At a glance

So far our systems *retrieve* passages and hand them to the user. The final step is to let a
**Large Language Model** read those passages and write a direct, natural-language **answer**.
Done naïvely, LLMs hallucinate and go stale. **Retrieval-Augmented Generation (RAG)** fixes this
by retrieving relevant context first and instructing the model to answer *from it* — turning
search into an answer engine that is accurate, current, and citable. This chapter assembles
everything from Chapters 1–9 into one pipeline.

---

## The motivation: why not just ask the LLM?

Ask an LLM a question directly and two problems surface:

1. **Hallucination** — it may produce a fluent, confident answer that is simply *wrong*, because
   it's generating plausible text, not looking anything up.
2. **Stale / missing knowledge** — it only knows what it saw in training. Your private documents,
   last week's news, and this quarter's numbers aren't in there.

RAG addresses both by **grounding** the model in retrieved evidence. The model no longer has to
*remember* the answer — it just has to *read and summarize* the passages you give it.

---

## The RAG pattern

```
                    ┌─────────────────────────── RAG ───────────────────────────┐
                    │                                                            │
  user question ──▶ │  1. RETRIEVE   2. AUGMENT the prompt      3. GENERATE      │ ──▶ grounded answer
                    │   top passages    (question + passages)     (LLM reads      │      (+ citations)
                    │   (Ch 2–8)        into one instruction)     & answers)      │
                    └────────────────────────────────────────────────────────────┘
```

Three steps:

1. **Retrieve** — use any retriever we've built (dense, hybrid, + re-rank) to fetch the top few
   relevant passages for the question.
2. **Augment** — build a prompt that contains the question *and* those passages, with an
   instruction like *"Answer using only the context below; if the answer isn't there, say so."*
3. **Generate** — the LLM produces an answer grounded in the supplied context.

The retrieval half of this course is what makes the generation half trustworthy. **Better
retrieval → better answers.**

---

## Anatomy of a good RAG prompt

The prompt is where grounding is enforced. A solid template:

```
You are a helpful assistant. Answer the QUESTION using ONLY the CONTEXT below.
If the context does not contain the answer, say "I don't know based on the provided context."
Cite the passages you used by their [id].

CONTEXT:
[4] The blue whale is the largest animal known to have ever lived ...
[5] Although they live in the ocean, whales are mammals ...

QUESTION: what is the largest animal that has ever lived?

ANSWER:
```

Key ingredients:

- **A grounding instruction** ("use ONLY the context") to suppress hallucination.
- **A refusal clause** ("say I don't know") so the model declines instead of inventing.
- **The retrieved passages**, each tagged with an id for **citations**.
- **The user's question**, clearly delimited.

---

## The model we use

To keep the course open-source and key-free, the notebook defaults to a **small instruction-tuned
model** (`google/flan-t5-base`) via Hugging Face `transformers`. It's tiny, runs on CPU, and is
enough to demonstrate grounded answering. The notebook is written so you can **swap in a stronger
model or a hosted API** by changing a single `generate()` function — the retrieval and prompt
logic stay identical.

```python
from transformers import pipeline
llm = pipeline("text2text-generation", model="google/flan-t5-base")
answer = llm(prompt, max_new_tokens=128)[0]["generated_text"]
```

---

## Hands-on

Notebook: [`notebooks/10_rag.ipynb`](notebooks/10_rag.ipynb)

You will:

1. Retrieve top passages for a question (reusing the Chapter 5 dense retriever).
2. **Assemble a grounded RAG prompt** from the question + passages (with ids for citations).
3. Generate an answer with a small open-source LLM (or your own `generate()`).
4. Demonstrate **grounding**: ask something the corpus *can't* answer and watch the model refuse
   instead of hallucinating.
5. Wrap it all in a single `rag_answer(question)` function — the capstone of the course so far.

> The retrieval + prompt-assembly logic runs and is tested without any model. The generation step
> downloads a small model on first run (internet once), or you can plug in an API.

---

## Slides

📊 **[Chapter 10 slide deck (PDF)](../../slides/Chapter-10-RAG.pdf)** — a visual summary of
retrieval-augmented generation.

---

## Going deeper 🔴

- **Grounding is not a guarantee.** Models can still ignore the context or over-generalize.
  Prompt design, and evaluating the *faithfulness* of answers to the context, matter.
- **Citations & attribution.** Returning the passage ids the answer used lets users verify claims
  — a major reason RAG beats a bare LLM for trust.
- **How many passages (context budget).** More context can help or hurt: too little misses the
  answer; too much dilutes it and risks the model latching onto a distractor ("lost in the
  middle"). Tune it.
- **Retrieval quality dominates.** Most RAG failures are *retrieval* failures — the answer wasn't
  in the passages. Improve the retriever (Chapters 6–8) before blaming the LLM.
- **RAG vs. fine-tuning.** RAG injects knowledge at query time (easy to update, citable);
  fine-tuning bakes it into weights (fast at inference, hard to update). They're complementary.

---

## Pitfalls & gotchas

- **No refusal clause.** Without "say I don't know," the model invents answers for
  unanswerable questions.
- **Dumping the whole corpus into the prompt.** Context windows are finite and models degrade
  with irrelevant text; retrieve, don't stuff.
- **Passages too big.** Long, unchunked passages waste context and bury the answer — motivating
  chunking (Chapter 11).
- **Blaming the LLM for retrieval bugs.** Always check *what was retrieved* before tuning the
  prompt or model.
- **No evaluation.** Answer quality should be measured (faithfulness, answer relevance), not
  eyeballed.

---

## Key terms

Large Language Model (LLM), hallucination, Retrieval-Augmented Generation (RAG), grounding,
context window, prompt template, refusal, citation, faithfulness. *(See
[GLOSSARY](../../GLOSSARY.md).)*

---

## Check your understanding

1. Name the two problems with asking an LLM directly that RAG addresses, and how it addresses each.
2. List the three steps of RAG and what each contributes.
3. What two clauses in the prompt reduce hallucination, and how?
4. Why are most RAG failures actually *retrieval* failures?
5. When would you choose RAG over fine-tuning to give a model new knowledge?

---

<!-- cyu-answers:start -->

> 💡 *Try answering each question yourself first, then expand to check.*

<details>
<summary><b>Show answer — 1</b></summary>

**Hallucination** (fluent but false answers) and **stale/missing knowledge**. RAG retrieves relevant, current passages and instructs the model to answer *from them*, so answers are grounded in real evidence and can include your private/up-to-date documents.

</details>

<details>
<summary><b>Show answer — 2</b></summary>

**Retrieve** relevant passages for the question; **augment** the prompt with those passages (plus instructions); **generate** an answer grounded in that context. Retrieval supplies the facts; the prompt enforces grounding; generation writes the answer.

</details>

<details>
<summary><b>Show answer — 3</b></summary>

The **grounding instruction** ("use ONLY the context") stops the model from drawing on unverified memory, and the **refusal clause** ("say I don't know if it's not there") gives it permission to decline instead of inventing an answer.

</details>

<details>
<summary><b>Show answer — 4</b></summary>

Because the LLM can only answer from what it's given: if the retriever didn't surface the passage containing the answer, the model has nothing correct to work from — so fixing retrieval (chapters 6-8) usually matters more than tweaking the prompt.

</details>

<details>
<summary><b>Show answer — 5</b></summary>

When knowledge changes often, must be **citable/verifiable**, or is private/large — RAG injects it at query time and is easy to update. Fine-tuning bakes knowledge into weights (fast at inference, hard to update) and suits fixed style/behavior more than fast-changing facts.

</details>

<!-- cyu-answers:end -->

## References

- Lewis et al., *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks* (RAG, 2020).
- Liu et al., *Lost in the Middle: How Language Models Use Long Contexts* (2023).
- Hugging Face `transformers` documentation (open-source generation used here).
- DeepLearning.AI × Cohere, *Large Language Models with Semantic Search*, Lesson on generating
  answers (inspiration).
