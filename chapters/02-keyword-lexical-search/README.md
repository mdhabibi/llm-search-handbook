# Chapter 2 — Keyword / Lexical Search

> **Level:** 🟢 Beginner  ·  **Status:** 🟩 Complete
> **Prerequisites:** Chapter 1.
> **You'll build:** a working keyword search engine — inverted index, TF-IDF, and BM25 — from
> scratch, then see exactly where it breaks.

---

## At a glance

Keyword search (a.k.a. **lexical search**) matches the literal words in a query against the
words in your documents. It's fast, transparent, needs no machine learning, and still powers a
huge share of search today. Understanding it deeply pays off twice: it's a strong baseline you
will keep using (in hybrid search, Chapter 8), and its failure modes are the exact reason
embeddings were invented (Chapters 3–6).

We'll build three things, each better than the last:

1. **Word-overlap search** — the naïve "count shared words" idea, to see the intuition.
2. **TF-IDF** — weight words by how *informative* they are.
3. **BM25** — the refined, industry-standard scoring function.

And we'll do it all over our own [sample corpus](../../data/sample_corpus.json), no external
services.

---

## The motivation

Think of any search box you used today — Spotify, YouTube, a shop, your company wiki. Behind
most of them, at least at the first stage, is keyword search. The task: given a query, score
every document by how well its words match, and return the top few. The genius is doing this
over millions of documents in *milliseconds*. Two ideas make that possible — a clever data
structure (the inverted index) and a good scoring function (BM25). Let's build both.

---

## Step 0 — Preparing text: tokenization

Before matching, we normalize text into **tokens** (roughly, words):

```
"What color is the Grass?"  ──tokenize──▶  ["what", "color", "is", "the", "grass"]
```

Typical steps: lowercase everything, split on non-letters, and often drop **stop words** (ultra-
common words like *the, is, of* that carry little meaning) and apply **stemming** (reduce
*running → run* so variants match). Our helper `src/corpus.py` (at the repo root) does a simple version you can
read in full.

> Why this matters: without normalization, "Grass" ≠ "grass" and "running" ≠ "run", and your
> matches silently fall apart.

---

## Step 1 — The inverted index: how search is *fast*

Imagine you had to answer a query by re-reading all 10 million documents every time. Hopeless.
Instead we build, **once, ahead of time**, an **inverted index**: a table mapping each word to
the list of documents that contain it (and how often).

```
FORWARD view (what we start with)      INVERTED INDEX (what we build)
────────────────────────────────      ─────────────────────────────────────
D0: "grass is green"                   term      → postings (doc: count)
D1: "the sky is blue"                  ────────────────────────────────────
D4: "the blue whale ..."               "grass"   → {D0:1}
                                       "green"   → {D0:1}
                                       "blue"    → {D1:1, D4:1}
                                       "whale"   → {D4:1}
                                       "sky"     → {D1:1}
```

Now a query like `blue` is answered by a single lookup — "blue → {D1, D4}" — instead of a full
scan. This is *the* trick behind instant search. The word→documents direction is why it's
called "inverted" (a normal index goes document→words).

---

## Step 2 — Scoring: not all shared words are equal

The naïve approach counts shared words. But we saw the flaw in Chapter 1: the words *the* and
*is* are shared by nearly every document and tell us nothing. We need to weight words by how
*informative* they are. That's **TF-IDF**.

### Term Frequency (TF)

> **Intuition:** a word that appears many times in a document probably matters to that document.

TF = how often term *t* appears in document *d*. If "whale" appears 3 times in a passage, that
passage is likely about whales.

### Inverse Document Frequency (IDF)

> **Intuition:** a word that appears in *few* documents is more distinctive and useful for
> telling documents apart. A word in *every* document is useless.

$$\text{IDF}(t) = \log\frac{N}{\text{df}(t)}$$

where *N* is the number of documents and df(*t*) is how many documents contain *t*.

### TF-IDF = TF × IDF

Multiply them: frequent-in-this-doc **and** rare-across-the-corpus = high score.

### Worked example (do the numbers yourself)

Take a 5-document toy corpus and the query `what color is the grass`:

```
D0 "the grass is green"          D1 "the sky is blue"       D2 "the capital of canada is ottawa"
D3 "a whale is a mammal"         D4 "tomorrow is saturday"
N = 5 documents
```

Compute IDF for the query's content words (log base *e*):

| term  | df (docs containing it) | IDF = ln(N/df)      |
|-------|-------------------------|---------------------|
| is    | 5                       | ln(5/5) = **0.00**  |
| the   | 3 (D0, D1, D2)          | ln(5/3) ≈ **0.51**  |
| color | 0                       | — (not in corpus)   |
| grass | 1 (D0)                  | ln(5/1) ≈ **1.61**  |

See what happened? **"is" contributes nothing** (it's everywhere), **"grass" contributes the
most** (it's rare and distinctive). Now score D0 by summing TF·IDF over query terms present:

```
score(D0) = TF(grass)·IDF(grass) + TF(the)·IDF(the) + TF(is)·IDF(is)
          =    1 · 1.61          +   1 · 0.51        +   1 · 0.00
          =  2.12   ← highest, and driven almost entirely by "grass"
```

Every other document only shares "the"/"is", so they score ≤ 0.51. TF-IDF gets the ranking
right *for the right reason*: the rare, meaningful word did the work.

---

## Step 3 — BM25: the workhorse

TF-IDF has two weaknesses that **BM25** fixes, and both come from common sense:

1. **Term saturation.** Seeing "whale" 10 times isn't 10× more relevant than seeing it once —
   there are diminishing returns. TF-IDF grows linearly forever; BM25 flattens out.
2. **Document length.** A long document naturally repeats words more, unfairly inflating raw
   TF. BM25 normalizes by length, comparing a document to the *average* document length.

The BM25 score of document *d* for query *q*:

$$\text{BM25}(q,d) = \sum_{t \in q} \text{IDF}(t) \cdot
\frac{f(t,d)\,(k_1 + 1)}{f(t,d) + k_1\left(1 - b + b\,\frac{|d|}{\text{avgdl}}\right)}$$

Don't be scared — read it piece by piece:

- $f(t,d)$ — how many times term *t* appears in *d* (the TF).
- $|d|$ — length of *d*; $\text{avgdl}$ — average document length in the corpus.
- $k_1$ (typically ~1.2–2.0) — controls **saturation**: how quickly extra occurrences stop
  helping.
- $b$ (typically ~0.75) — controls **length normalization**: 0 = ignore length, 1 = fully
  normalize.
- The IDF term is BM25's own variant, but the intuition (rare = valuable) is identical.

The whole fraction is just "TF, but with saturation and length-normalization built in." That's
BM25. It has been the default first-stage ranker for decades because it's fast, robust, and
needs no training.

---

## Hands-on

Notebook: [`notebooks/02_keyword_search.ipynb`](notebooks/02_keyword_search.ipynb)

In order, you will:

1. Load the corpus and tokenize it.
2. **Build an inverted index** and answer a query with a single lookup.
3. Implement **word-overlap** scoring and rank the *grass* query.
4. Implement **TF-IDF** from scratch and reproduce the worked example's numbers.
5. Implement **BM25** from scratch, then cross-check against the `rank-bm25` library.
6. Run the **failure demo**: the *"strong pain in the side of the head"* query that BM25 misses
   even though the migraine passage answers it — motivating embeddings in Chapter 3.

---

## Going deeper 🔴

- **Why the "+0.5" terms in BM25's IDF?** BM25 uses
  $\text{IDF}(t)=\ln\!\big(1+\frac{N-\text{df}(t)+0.5}{\text{df}(t)+0.5}\big)$. The smoothing
  keeps IDF from blowing up or going negative for very common terms.
- **Tuning $k_1$ and $b$.** These are corpus-dependent. Short, uniform documents want low $b$;
  long, varied documents want $b$ near 0.75. Chapter 9 shows how to tune them by *measuring*.
- **BM25F and fielded search.** Real documents have fields (title, body, tags). BM25F weights
  matches in important fields (like the title) more heavily.
- **Still a strong baseline.** On many benchmarks, well-tuned BM25 is surprisingly competitive
  with — and complementary to — neural retrieval, which is exactly why hybrid search (Chapter 8)
  combines them.

---

## Pitfalls & gotchas

- **Mismatched tokenization.** You must tokenize the query the *same way* as the documents, or
  matches vanish. Same lowercasing, same stemming, same stop-word list.
- **Over-aggressive stop-word removal.** Dropping "not" or "no" can flip meaning; dropping "IT"
  can erase a real term. Be careful.
- **Raw counts without length normalization.** Long documents will dominate. Use BM25, not
  plain TF, in practice.
- **Expecting keyword search to understand synonyms.** It fundamentally can't — that's the
  point of the failure demo, and the reason the course continues.

---

## Key terms

lexical search, tokenization, stop words, stemming, inverted index, postings, term frequency
(TF), document frequency (df), inverse document frequency (IDF), TF-IDF, BM25, term saturation,
length normalization. *(See [GLOSSARY](../../GLOSSARY.md).)*

---

## Check your understanding

1. Why is it called an *inverted* index, and what problem does it solve?
2. In the worked example, why does the word "is" contribute nothing to the score?
3. What two problems does BM25 fix compared to plain TF-IDF, and which parameter controls each?
4. Predict: for the query "blue", will D1 (sky) or D4 (whale) score higher, and what would
   change your answer? (Hint: think TF and length.)
5. Give a query where keyword search would fail on our corpus, and explain why.

---

<!-- cyu-answers:start -->

> 💡 *Try answering each question yourself first, then expand to check.*

<details>
<summary><b>Show answer — 1</b></summary>

It maps term -> the documents containing it (the inverse of document -> words). This lets a query be answered by a direct lookup instead of scanning every document, which is what makes search fast.

</details>

<details>
<summary><b>Show answer — 2</b></summary>

Its IDF is 0: *is* appears in every document, so ln(N/df) = ln(N/N) = 0. A term in every document carries no power to distinguish documents, so it adds nothing to the score.

</details>

<details>
<summary><b>Show answer — 3</b></summary>

**Term saturation** (extra occurrences give diminishing returns) — controlled by **k1**; and **length normalization** (long documents shouldn't win just for being long) — controlled by **b**.

</details>

<details>
<summary><b>Show answer — 4</b></summary>

**D1 (sky) scores higher.** *blue* appears twice in D1 but once in D4, and D1 is shorter, so BM25's TF and length-normalization both favor D1. It would flip if D4 repeated *blue* more often or were much shorter than D1.

</details>

<details>
<summary><b>Show answer — 5</b></summary>

*"strong pain in the side of the head"* — the answer (the migraine passage) says *"sharp sensation localized to one temple"* and shares almost no words, so keyword search buries it.

</details>

<!-- cyu-answers:end -->

## References

- Robertson & Zaragoza, *The Probabilistic Relevance Framework: BM25 and Beyond* (2009).
- Manning, Raghavan & Schütze, *Introduction to Information Retrieval*, chapters on term
  weighting and the vector space model.
- `rank-bm25` — the small Python library we cross-check against.
- DeepLearning.AI × Cohere, *Large Language Models with Semantic Search*, Lesson 1 (inspiration).
