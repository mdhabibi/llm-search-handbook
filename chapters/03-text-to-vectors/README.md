# Chapter 3 — From Text to Vectors

> **Level:** 🟢 Beginner  ·  **Status:** 🟩 Complete
> **Prerequisites:** Chapter 2.
> **You'll build:** intuition and code for turning text into numbers, plus the similarity
> measures every semantic system depends on.

---

## At a glance

Computers compare numbers, not words. To search by *meaning*, we first have to turn text into
**vectors** — lists of numbers — in a way where "close in meaning" becomes "close in space."
This chapter walks the ladder from the crudest representations (one-hot, bag-of-words) up to
the idea of a **dense embedding**, and teaches the tool that makes "close" precise: **cosine
similarity.** Chapter 4 then shows how a real model produces those vectors.

---

## The motivation

In Chapter 2 keyword search failed on *"strong pain in the side of the head"* because it only
sees words, not meaning. To fix that we need a representation where *temple* and *side of the
head* end up near each other. That representation is a vector. So the question of this chapter
is simple: **how do we convert text into numbers, and how do we measure whether two pieces of
text are "close"?**

---

## Rung 1 — One-hot encoding (words as isolated symbols)

The simplest way to give a word a number is to assign it a slot. Build a vocabulary, then
represent each word as a vector that is all zeros except a single 1 in its slot.

```
vocabulary: [apple, banana, car, castle, joy]

apple  → [1, 0, 0, 0, 0]
banana → [0, 1, 0, 0, 0]
car    → [0, 0, 1, 0, 0]
```

It works, but look at what it *can't* do. Every pair of different words is **exactly equally
far apart**. "apple" is no closer to "banana" than it is to "car." One-hot vectors encode
*identity* but zero *meaning*. They're also **sparse** and huge — one dimension per word in the
language (millions).

---

## Rung 2 — Bag-of-words (documents as word counts)

To represent a *document*, add up the one-hot vectors of its words — i.e., just count how
often each vocabulary word appears. Order is thrown away (hence "bag").

```
vocab: [apple, fruit, is, an, red]

"an apple is a fruit"  → [1, 1, 1, 1, 0]
"apple is red"         → [1, 0, 1, 0, 1]
```

This is exactly what TF-IDF and BM25 operate on under the hood. It's great for keyword matching
— but it inherits one-hot's blindness: two documents that say the same thing with *different
words* share no dimensions, so they look unrelated. Synonyms are invisible. **Meaning still
isn't captured.**

---

## Rung 3 — Dense vectors (meaning as location)

The breakthrough: instead of one dimension per word, use a *few hundred* dimensions, and let a
model choose the numbers so that **similar meanings land near each other.** These are **dense**
vectors (every dimension carries information, few zeros) — the **embeddings** we build in
Chapter 4.

Picture a 2-D version of the idea (real ones have hundreds of dimensions):

```
        fruit axis ▲
                   │      🍎 apple      🍌 banana
                   │        🍊 orange
        ───────────┼─────────────────────────▶ vehicle axis
                   │   🏰 castle
                   │      🏠 house        🚗 car   🚲 bike
```

Now "apple" sits next to "banana" and "orange" — close in space because close in meaning — and
far from "car." *That's* what we couldn't do before. Given only the neighborhood, you could
guess a new word's location from its meaning. (This is precisely the "where would you put
*apple*?" intuition from the lesson.)

---

## Measuring "closeness"

Once text is vectors, we need a number for how similar two vectors are. Three common measures:

### Dot product
Multiply matching components and sum: $\mathbf{a}\cdot\mathbf{b}=\sum_i a_i b_i$. Larger =
more aligned, but it grows with vector *length*, so long vectors can dominate.

### Cosine similarity (the default for text)
The cosine of the angle between two vectors — it measures **direction, ignoring length**:

$$\text{cosine}(\mathbf{a},\mathbf{b}) = \frac{\mathbf{a}\cdot\mathbf{b}}{\lVert\mathbf{a}\rVert\,\lVert\mathbf{b}\rVert}$$

- **1.0** → same direction (as similar as possible)
- **0.0** → perpendicular (unrelated)
- **−1.0** → opposite

We use cosine because in text the *direction* of a vector encodes meaning, while its magnitude
often just reflects length or word count — which we usually don't want to matter.

### Euclidean distance
Straight-line distance $\lVert\mathbf{a}-\mathbf{b}\rVert$. Smaller = closer. For
**normalized** vectors (scaled to length 1), Euclidean distance and cosine similarity rank
neighbors identically — which is why many systems normalize first and then just use dot
product.

### Worked mini-example

```
a = [1, 0]   ("apple", pointing along the fruit axis)
b = [2, 0]   ("banana", same direction, longer)
c = [0, 1]   ("car", pointing along the vehicle axis)

dot(a, b)    = 1·2 + 0·0 = 2
cosine(a, b) = 2 / (1 · 2) = 1.0     ← identical meaning, despite different lengths
cosine(a, c) = 0 / (1 · 1) = 0.0     ← unrelated
```

Notice cosine says apple≈banana are a perfect match (same direction) even though their raw
vectors differ in length — exactly the behavior we want.

---

## Hands-on

Notebook: [`notebooks/03_text_to_vectors.ipynb`](notebooks/03_text_to_vectors.ipynb)

You will:

1. Build **one-hot** and **bag-of-words** vectors by hand and see why they miss meaning.
2. Implement **cosine similarity** and **Euclidean distance** in a few lines of numpy.
3. Play with a **toy 2-D word map** (fruits / vehicles / buildings / sports) and confirm that
   *apple* really does land among the fruits by nearest-neighbor.
4. See that normalizing vectors makes cosine and Euclidean agree on the ranking.

Everything here is pure numpy + matplotlib — no models yet, so it runs instantly.

---

## Slides

📊 **[Chapter 3 slide deck (PDF)](../../slides/Chapter-03-From-Text-to-Vectors.pdf)** — a visual
summary of turning text into vectors.

---

## Going deeper 🔴

- **The curse of dimensionality.** In very high dimensions, distances between random points
  concentrate — most pairs look equally far. Good embeddings fight this by placing *meaningful*
  structure in the space; it's why learned embeddings beat random projections.
- **Why not just use bag-of-words with TF-IDF weights as "vectors"?** You can — that's the
  classic *vector space model*, and it's still sparse and meaning-blind to synonyms. Dense
  embeddings differ by being *learned* to capture semantics.
- **Distance metric choice matters.** Cosine is standard for text embeddings; some models are
  trained for dot product or Euclidean. Always match the metric the model was trained with
  (Chapter 4).

---

## Pitfalls & gotchas

- **Comparing un-normalized vectors with dot product** can let a long document beat a more
  relevant short one. Normalize, or use cosine.
- **Mixing metrics.** If a model was trained with cosine, don't rank with raw Euclidean on
  un-normalized vectors and expect the same neighbors.
- **Thinking dimensions are human-interpretable.** In real embeddings, no single dimension
  means "fruitiness." Meaning is distributed across all of them.

---

## Key terms

vector, one-hot encoding, sparse vector, bag-of-words, dense vector, embedding, dot product,
cosine similarity, Euclidean distance, normalization, vector space. *(See
[GLOSSARY](../../GLOSSARY.md).)*

---

## Check your understanding

1. Why are all distinct one-hot vectors equally far apart, and why is that a problem?
2. What information does bag-of-words throw away, and what does it keep?
3. In one sentence, what does cosine similarity measure that the dot product doesn't isolate?
4. Two vectors point the same way but one is twice as long. What is their cosine similarity?
5. When would Euclidean distance and cosine similarity give the *same* ranking of neighbors?

---

<!-- cyu-answers:start -->

> 💡 *Try answering each question yourself first, then expand to check.*

<details>
<summary><b>Show answer — 1</b></summary>

Every one-hot vector has a single 1 in a unique slot, so any two distinct words differ in exactly two coordinates and sit the same distance apart. That means the representation encodes identity but zero similarity of meaning.

</details>

<details>
<summary><b>Show answer — 2</b></summary>

It throws away **word order** (and grammar); it keeps **which words appear and how often**. So "dog bites man" and "man bites dog" look identical.

</details>

<details>
<summary><b>Show answer — 3</b></summary>

Cosine isolates **direction** (the angle), ignoring vector **length/magnitude**; the raw dot product mixes both, so it grows with length even when the direction (meaning) is unchanged.

</details>

<details>
<summary><b>Show answer — 4</b></summary>

**1.0** — same direction means a cosine of 1 regardless of length. (The dot product would differ, but cosine divides out magnitude.)

</details>

<details>
<summary><b>Show answer — 5</b></summary>

When the vectors are **L2-normalized** (scaled to unit length): then nearest-by-cosine and nearest-by-Euclidean produce the identical ranking.

</details>

<!-- cyu-answers:end -->

## References

- Jurafsky & Martin, *Speech and Language Processing*, chapter on vector semantics (free draft).
- Manning, Raghavan & Schütze, *Introduction to Information Retrieval*, the vector space model.
- DeepLearning.AI × Cohere, *Large Language Models with Semantic Search*, Lesson 2 (inspiration).
