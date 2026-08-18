<!--
GAMMA IMPORT — Chapter 2: Keyword / Lexical Search
How to use: gamma.app → New → "Paste in text" (or Import) → paste everything below the line.
Each "---" is a new slide/card. Keep bullets short; Gamma designs the visuals.
Suggested theme: dark indigo→violet gradient, one accent (electric blue), sans-serif.
Lines in [brackets] are art/layout hints for Gamma or for you — delete if you like.
-->

# Keyword / Lexical Search
### Chapter 2 · Search Semantically — a course on LLMs & semantic search
Match the words — fast. The workhorse behind decades of search.
[Title slide, dark gradient background, abstract "dot cluster" / network motif]

---

## The task: connect a query to the right documents — in milliseconds
- A user gives a **query**; we return the documents that match
- It has to be **fast** — potentially millions of documents
- Keyword search scores documents by their **shared words**
- Two ideas make it work: an **index** (speed) + a **scoring function** (quality)
[Right side: a simple pipeline — Query → Match + score → Ranked results]

---

## Intuition: count the shared words
Query: *what color is the grass*
- **D0** "the grass is green" → shares 3 words ✅ best
- **D1** "the sky is blue" → 2
- **D2** "the capital of canada is ottawa" → 2
- **D3** "a whale is a mammal" → 1
Takeaway: common words like "the" and "is" dominate the count — we must weight them.
[Show four document cards with a count badge each; highlight D0]

---

## Step 1 — Tokenization: turn text into comparable tokens
- **Lowercase** — "Grass" = "grass"
- **Split** on non-letters
- **Drop stop-words** — the, is, of
- **Stem** — running → run
Tokenize the query the **same way** as the documents, or matches silently vanish.
[4 numbered circles in a row with arrows between them]

---

## Step 2 — The inverted index: how search is instant
- Map every **term → the documents that contain it**
- Built once, ahead of time (at indexing)
- A query becomes a **single lookup**, not a full scan
- This is why results come back in **milliseconds**
[Diagram: term boxes (grass, blue, whale) → arrows → posting lists {D0}, {D1,D4}, {D4}]

---

## Step 3 — TF-IDF: weight words by how informative they are
- **Term Frequency (TF)** — frequent in a document → probably matters to it
- **Inverse Document Frequency (IDF)** — rare across the corpus → more distinctive
- **TF-IDF = TF × IDF** — frequent here AND rare overall = a high score
[Two callout cards (TF, IDF) with icons in colored circles; show IDF = ln(N / df)]

---

## Worked example: why "is" scores nothing and "grass" wins
N = 5 documents.  IDF = ln(N / df)

| term | df | IDF |
|------|----|-----|
| is | 5 of 5 | 0.00 |
| the | 3 of 5 | 0.51 |
| grass | 1 of 5 | 1.61 |

**score(D0) ≈ 2.12** — driven almost entirely by "grass". "is" is in every doc → IDF 0 → adds nothing.
[Table on the left, big stat callout on the right]

---

## Step 4 — BM25: the workhorse ranking function
BM25(q,d) = Σ IDF(t) · [ f(t,d)·(k₁+1) ] / [ f(t,d) + k₁·(1 − b + b·|d|/avgdl) ]
- **k₁** — term saturation (diminishing returns for repeats)
- **b** — length normalization (fairness for long documents)
The default first-stage ranker for decades — fast, robust, no training.
[Dark slide; render the formula large on a light card; two "knob" chips below]

---

## Pitfalls & gotchas
- **Mismatched tokenization** — query and docs must be normalized the same way
- **Over-aggressive stop-words** — dropping "not"/"no" can flip meaning
- **Raw counts, no length norm** — long documents dominate; use BM25
- **Expecting synonyms** — keyword search can't match meaning (that needs embeddings)
[Icon rows: a warning "!" in a colored circle + bold header + one line each]

---

## Key terms
lexical search · tokenization · stop words · stemming · inverted index · postings · term frequency (TF) · document frequency (df) · IDF · TF-IDF · BM25 · term saturation · length normalization
[Render each as a rounded "chip"; full definitions in the course glossary]

---

## Check your understanding
- Why is it called an *inverted* index, and what problem does it solve?
- In the worked example, why does "is" contribute nothing?
- What two problems does BM25 fix, and which parameter controls each?

**Next → Chapter 3: From Text to Vectors** — where meaning-vectors finally solve the synonym problem.
[Closing slide, dark gradient, dot motif; footer: github.com/mdhabibi/llm-search-handbook]
