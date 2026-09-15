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

## What people actually build with this

This one-two step — search, then generate — is the engine behind a whole category of products
you've probably used. They differ only in what sits in the index:

| The product | The corpus behind it |
|---|---|
| "Chat with this PDF" | one document, chunked |
| Ask-an-author bots | a writer's collected essays or books |
| Podcast Q&A ("ask the show anything") | episode transcripts |
| Video Q&A / "jump to the moment" | subtitle tracks, timestamped |
| Company knowledge assistants | internal wikis, tickets, runbooks |
| Documentation search that answers | API docs and guides |
| Customer-support deflection | help centre articles + past tickets |

None of these needs a custom-trained model. They need **a good index and a careful prompt** —
which is to say, they need the nine chapters you've already done plus this one. When someone
says "we fine-tuned a model on our docs," the honest question is usually whether RAG would have
been cheaper, faster to update, and easier to cite.

The pattern also degrades gracefully: add re-ranking (Chapter 7) when the right passage is
retrieved but ranked badly, and hybrid search (Chapter 8) when users search by exact product
codes as well as by meaning.

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

### That `max_new_tokens` is not decoration

It's a hard cap on how many tokens the model may produce, and when the answer reaches it the
model **stops mid-sentence**:

```
Yes, side projects are a good idea. They help you develop skills and can be
a good way to network with others. However, make sure you don't create a
conflict with your employer and that you're not violating any
                                                              ^ cut off here
```

Nothing is broken and there is no error — you asked for at most *N* tokens and got exactly that.
Raise the cap for longer answers, or instruct the model to be brief. This is one of the most
common "why is my RAG output weird?" moments, and it costs people hours because it looks like a
model failure rather than a setting.

Watch both ends of the budget: the **prompt** (question + passages) and the **answer** share the
model's context window. Stuff in too many passages and you squeeze the room left to answer in.

---

## Generation is not deterministic

Everything before this chapter was **reproducible**. Run the same BM25 query, the same dense
retrieval, the same re-ranker twice and you get identical results — the scores are fixed
arithmetic over fixed vectors. You could rely on that.

The generator breaks it. Ask the same question, with the same retrieved passages, in the same
prompt, twice, and you can get two different answers:

```
run 1 → "Yes — Andrew recommends side projects to build skills and network."
run 2 → "Side projects are valuable, though avoid conflicts with your employer."
```

Both are grounded and correct. They are simply different, because most LLMs **sample** their
next token from a probability distribution rather than always taking the most likely one.
**Temperature** controls how adventurous that sampling is: near `0` the model almost always picks
the top token (nearly deterministic, repetitive); higher values flatten the distribution and give
more varied, more creative — and more wrongness-prone — output.

Three consequences worth internalising:

- **For factual RAG, keep temperature low.** You want the model to report the passages
  faithfully, not to improvise around them.
- **Judge a prompt on several runs, not one.** A prompt that worked once may have been lucky.
  Generate the same prompt 3–5 times and read the spread — that's the fastest way to see whether
  an instruction reliably lands. (The notebook does exactly this.)
- **Evaluate over multiple runs too.** A single-run score for a RAG answer partly measures luck.
  This is precisely why Chapter 9's retrieval metrics are the dependable half of RAG evaluation:
  retrieval is deterministic and cheap to measure; generation is neither.

> **Retrieval is arithmetic; generation is a roll of weighted dice.** Test them differently.

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
6. **Watch an answer truncate**: shrink `max_new_tokens` and see the output stop mid-sentence,
   then restore it.
7. **Sample one prompt several times** at different temperatures and compare the spread — the
   fastest way to tell a reliable prompt from a lucky one.

> The retrieval + prompt-assembly logic runs and is tested without any model. The generation step
> downloads a small model on first run (internet once), or you can plug in an API.

---

## Evaluating a RAG system: retrieval vs. generation 🟡

A RAG answer can fail in two very different places, and a single "was the answer good?" score
hides *which*. Always evaluate the two halves **separately**:

- **Retrieval quality** — did the right passage(s) reach the context at all?
- **Generation quality** — given that context, did the model use it *faithfully* and actually
  *answer the question*?

Separating them matters because the fix is opposite in each case:

| Symptom | Where it broke | What to fix |
|---------|----------------|-------------|
| The evidence was never retrieved | **Retrieval** | the retriever (Ch 6–8): embeddings, hybrid, re-ranking, chunking |
| The passage *was* retrieved, but the answer misses or misreads it | **Generation** | the prompt, the model, the context budget |

A blended answer score can look identical in both situations — yet one is a **"missing evidence"**
problem and the other an **"answer construction"** problem. Measuring each half tells you which.

**Measuring retrieval** is exactly Chapter 9: label which passages are relevant for each question
and compute **recall@k / MRR / nDCG** on what the retriever returned. If recall@k is low, the LLM
never had a chance — stop tuning the prompt and fix the retriever.

**Measuring generation** (conditioned on the retrieved context) usually tracks two things:

- **Faithfulness / groundedness** — is every claim in the answer supported by the passages
  (no hallucination)?
- **Answer relevance** — does the answer actually address the question, not just echo context?

These are harder to score automatically. Common approaches are human ratings or an
**LLM-as-a-judge** that reads `(question, context, answer)` and rates faithfulness and relevance —
cheaper to run, but calibrate it against a few human labels first.

> **Rule of thumb:** condition generation metrics on *good* retrieval. If you score answers over
> contexts that don't even contain the evidence, you're measuring the retriever's failures as if
> they were the model's.

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
context window, prompt template, refusal, citation, faithfulness, answer relevance,
temperature, sampling, greedy decoding, max tokens / truncation,
retrieval vs. generation evaluation, LLM-as-a-judge. *(See
[GLOSSARY](../../GLOSSARY.md).)*

---

## Check your understanding

1. Name the two problems with asking an LLM directly that RAG addresses, and how it addresses each.
2. List the three steps of RAG and what each contributes.
3. What two clauses in the prompt reduce hallucination, and how?
4. Why are most RAG failures actually *retrieval* failures?
5. When would you choose RAG over fine-tuning to give a model new knowledge?
6. A RAG answer comes back wrong. What single check tells you whether to fix the *retriever* or the *prompt/model*, and why?
7. Your RAG answer stops mid-sentence. What is the most likely cause, and where else does the same budget bite?
8. You run the same question twice and get two different answers. Explain why, and say what you would change for a factual assistant.

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

<details>
<summary><b>Show answer — 6</b></summary>

Check **what was retrieved** (and compute retrieval recall for that question). If the evidence never made it into the context, it's a **retrieval** failure — fix the retriever (Ch 6–8). If the right passage *was* there but the answer missed or misread it, it's a **generation** failure — fix the prompt, model, or context budget. Evaluating retrieval and generation separately localizes the fix instead of guessing.

</details>

<details>
<summary><b>Show answer — 7</b></summary>

You hit the **token cap** (`max_new_tokens` / `max_tokens`): the model was allowed only N tokens and stopped exactly there — no error, just a truncated sentence. Raise the cap, or instruct the model to answer briefly. The same budget bites at the other end too: the prompt (question + retrieved passages) and the answer share the model's **context window**, so packing in more passages leaves less room to answer in.

</details>

<details>
<summary><b>Show answer — 8</b></summary>

Because generation is **sampled**, not computed: the model draws each next token from a probability distribution instead of always taking the most likely one, so wording varies between runs. For a factual assistant, lower the **temperature** (near 0, or use greedy decoding) so output is near-deterministic and hews to the retrieved passages — and evaluate prompts over several runs rather than one, since a single good answer may just be luck.

</details>

<!-- cyu-answers:end -->

## References

- Lewis et al., *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks* (RAG, 2020).
- Liu et al., *Lost in the Middle: How Language Models Use Long Contexts* (2023).
- Es et al., *RAGAS: Automated Evaluation of Retrieval Augmented Generation* (2023) — separates
  faithfulness, answer relevance, and context relevance.
- Hugging Face `transformers` documentation (open-source generation used here).
- DeepLearning.AI × Cohere, *Large Language Models with Semantic Search*, Lesson on generating
  answers (inspiration).
