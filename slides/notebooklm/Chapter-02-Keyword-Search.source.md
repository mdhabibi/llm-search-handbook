# Keyword / Lexical Search — Slide Source (Chapter 2)

*Course: “Search Semantically — Large Language Models & Semantic Search” by Dr. Mahdi Habibi.*
*This document is a self-contained teaching source designed to be turned into a slide deck (about 12 slides). It contains the narrative, the exact examples and numbers, descriptions of the diagrams, key terms, and a suggested slide-by-slide outline. Build the deck to follow the outline near the end.*

**Audience:** beginners with a little Python; scales to intermediate.
**One-line goal:** understand how keyword (lexical) search works — the inverted index, TF-IDF, and BM25 — and why it eventually needs embeddings.

---

## Learning objectives

By the end, a learner can:
1. Explain what keyword (lexical) search is and where it is used.
2. Describe the inverted index and why it makes search fast.
3. Explain TF, IDF, and TF-IDF, and compute a simple TF-IDF score.
4. Explain what BM25 adds over TF-IDF (term saturation and length normalization).
5. Name the fundamental limitation of keyword search (the vocabulary-mismatch / synonym problem).

---

## The narrative (use this as the slide content)

### 1. What is keyword search, and why it still matters
Keyword search — also called **lexical search** — finds documents by matching the **literal words** in a query against the words in documents. It powers most search boxes you use (shops, wikis, help centers) and is still a strong first-stage baseline. Understanding it deeply explains exactly *why* we later need embeddings. Two ideas make keyword search work: a fast data structure (the **inverted index**) and a good **scoring function** (BM25).

### 2. The task
A user submits a **query**; the system must return the **documents** that best match — over potentially millions of documents, in **milliseconds**. Keyword search scores each document by how well its words match the query, then returns the top results.

### 3. Intuition: count the shared words
Take the query **“what color is the grass”** against a tiny archive:
- D0 “the grass is green” → shares **3** words (the, grass, is) — best.
- D1 “the sky is blue” → shares 2 (the, is).
- D2 “the capital of canada is ottawa” → shares 2 (the, is).
- D3 “a whale is a mammal” → shares 1 (is).
D0 wins because it repeats the query’s words. **Problem:** ultra-common words like “the” and “is” dominate the count while carrying no meaning. We must weight words by how informative they are.

### 4. Step 1 — Tokenization
Before matching, normalize text into **tokens**: (1) lowercase (“Grass” = “grass”), (2) split on non-letters, (3) optionally drop **stop words** (the, is, of), (4) optionally **stem** (running → run). Rule: tokenize the query the **same way** as the documents, or matches silently vanish.

### 5. Step 2 — The inverted index (why search is instant)
An **inverted index** maps each **term → the list of documents that contain it** (the “postings”). It is built once, ahead of time. A query then becomes a single dictionary lookup instead of scanning every document — this is why results return in milliseconds.
*Diagram to show:* three rows — “grass → {D0}”, “blue → {D1, D4}”, “whale → {D4}” — each a term box with an arrow to its postings list. (It’s called *inverted* because the normal direction is document → words; here it’s word → documents.)

### 6. Step 3 — TF-IDF: weight words by how informative they are
- **Term Frequency (TF):** how often a term appears in a document. Frequent in a document → probably matters to that document.
- **Inverse Document Frequency (IDF):** how rare a term is across the whole corpus. Rare across the corpus → more distinctive and useful. Formula: **IDF(t) = ln(N / df(t))**, where N is the number of documents and df(t) is how many contain t.
- **TF-IDF = TF × IDF:** high when a term is frequent *here* AND rare *overall*.

### 7. Worked example (the key numbers)
Corpus of **N = 5** documents. Query content words and their IDF = ln(N / df):
| term | df (docs containing it) | IDF = ln(N / df) |
|------|--------------------------|------------------|
| is | 5 | ln(5/5) = 0.00 |
| the | 3 | ln(5/3) ≈ 0.51 |
| grass | 1 | ln(5/1) ≈ 1.61 |
Scoring D0 (“the grass is green”) by summing TF×IDF over the query terms it contains:
**score(D0) ≈ (1×1.61) + (1×0.51) + (1×0.00) = 2.12** — driven almost entirely by “grass.” The word “is” contributes **nothing** because it appears in every document (IDF = 0). TF-IDF ranks D0 first, and for the right reason: the rare, meaningful word did the work.

### 8. Step 4 — BM25: the workhorse
**BM25** improves TF-IDF with two common-sense fixes:
- **Term saturation** (parameter **k₁**, ~1.2–2.0): seeing a word 10 times isn’t 10× more relevant than once — diminishing returns. TF-IDF grows forever; BM25 flattens.
- **Length normalization** (parameter **b**, ~0.75): long documents naturally repeat words, so BM25 compares a document to the *average* document length so long docs don’t win unfairly.
BM25 has been the default first-stage ranking function for decades: fast, robust, and it needs no training. (In words: for each query term, BM25 adds up IDF(t) times a saturating, length-normalized version of the term frequency.)

### 9. Pitfalls & gotchas
- **Mismatched tokenization** — the query and documents must be normalized the same way, or matches disappear.
- **Over-aggressive stop-word removal** — dropping “not” or “no” can flip meaning.
- **Raw counts without length normalization** — long documents dominate; use BM25, not plain TF.
- **Expecting synonyms** — keyword search fundamentally cannot match meaning. If the answer is phrased differently (e.g., query “strong pain in the side of the head” vs. a passage “a sharp sensation localized to one temple”), keyword search misses it. This is the **vocabulary-mismatch problem** — the reason the course moves on to embeddings.

### 10. Recap and what’s next
Keyword search = tokenize → inverted index (speed) → BM25 (quality). It’s an excellent, fast baseline, but it matches *words*, not *meaning*. **Next: Chapter 3 — From Text to Vectors**, where we turn text into meaning-vectors so synonyms finally match.

---

## Key terms (define these on a slide as short chips)
lexical search; tokenization; stop words; stemming; inverted index; postings; term frequency (TF); document frequency (df); inverse document frequency (IDF); TF-IDF; BM25; term saturation (k₁); length normalization (b); vocabulary-mismatch problem.

---

## Check your understanding (good for a quiz slide or Q&A)
1. **Why is it called an *inverted* index, and what problem does it solve?** It maps term → documents (the inverse of document → words); it lets a query be answered by a direct lookup instead of scanning every document, which makes search fast.
2. **In the worked example, why does “is” contribute nothing to the score?** Its IDF is 0: “is” appears in every document, so ln(N/df) = ln(5/5) = 0. A term in every document can’t distinguish documents.
3. **What two problems does BM25 fix versus TF-IDF, and which parameter controls each?** Term saturation (k₁) and length normalization (b).
4. **What is the fundamental limitation of keyword search?** It matches words, not meaning, so it misses relevant documents that use different words (synonyms/paraphrases).

---

## Suggested slide outline (build ~12 slides to mirror this)
1. **Title** — “Keyword / Lexical Search” · Chapter 2 · Search Semantically. Subtitle: “Match the words — fast.”
2. **Why it matters** — lexical search powers most search boxes; strong baseline; two ideas: index + scoring.
3. **The task** — query → best documents, over millions, in milliseconds.
4. **Intuition: count shared words** — the “grass” example with the four documents and their counts; note stop-word problem.
5. **Tokenization** — lowercase → split → stop-words → stem; “normalize both sides the same way.”
6. **Inverted index** — the term → postings diagram; “single lookup, not a full scan.”
7. **TF & IDF** — two ideas, with IDF = ln(N/df).
8. **Worked example** — the df/IDF table and score(D0) ≈ 2.12; “‘is’ adds nothing.”
9. **BM25** — the two fixes: saturation (k₁) and length normalization (b); the default ranker for decades.
10. **Pitfalls** — mismatched tokenization; stop-word over-removal; no length norm; no synonyms.
11. **Key terms** — the chips list.
12. **Recap & next** — tokenize → index → BM25; matches words not meaning → Chapter 3 embeddings. Include the check-your-understanding questions.
