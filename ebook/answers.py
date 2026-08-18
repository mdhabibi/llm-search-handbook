# -*- coding: utf-8 -*-
"""Single source of truth for the "Check your understanding" answers.

Keyed by chapter folder name -> ordered list of answer strings (Markdown).
Used to (a) inject collapsible <details> answers into each chapter README, and
(b) build the Answers appendix in the ebook PDF.
"""

ANSWERS = {
"00-introduction": [
 "Because it matches literal *words*, not *meaning*: if the best document phrases the same idea with different words, keyword search sees no overlap and misses it.",
 "**Retrieve** quickly pulls a small set of likely-relevant documents from the whole corpus. Making it *semantic* means comparing the *meaning* of the query and documents (via embeddings) instead of shared words, so paraphrases still match.",
 "**Re-rank** and **Generate** are optional. Skip re-ranking when first-stage results are already good enough or latency is tight; skip generation when you just want to return passages (a search box) rather than a written answer.",
],
"01-foundations-of-information-retrieval": [
 "An **information need** is what the user actually wants to know; the **query** is the short, imperfect text they type to express it. The query is a lossy stand-in for the need.",
 "So it can answer in milliseconds. Building the **index** ahead of time means the system doesn't have to re-read every document at query time — it just looks up the precomputed structure.",
 "**Retrieval** (stage 1) casts a wide, cheap net over the whole corpus, optimizing for speed and recall; **re-ranking** (stage 2) reorders the small candidate set precisely, optimizing for accuracy.",
 "Any true paraphrase works, e.g. *\"side of the head hurts\"* and *\"pain localized to one temple\"* — same meaning, essentially no shared content words.",
 "Common words like *the* and *is* appear in almost every document, so shared counts of them signal nothing about relevance — they inflate scores without indicating meaning. (IDF fixes this in Chapter 2.)",
],
"02-keyword-lexical-search": [
 "It maps term -> the documents containing it (the inverse of document -> words). This lets a query be answered by a direct lookup instead of scanning every document, which is what makes search fast.",
 "Its IDF is 0: *is* appears in every document, so ln(N/df) = ln(N/N) = 0. A term in every document carries no power to distinguish documents, so it adds nothing to the score.",
 "**Term saturation** (extra occurrences give diminishing returns) — controlled by **k1**; and **length normalization** (long documents shouldn't win just for being long) — controlled by **b**.",
 "**D1 (sky) scores higher.** *blue* appears twice in D1 but once in D4, and D1 is shorter, so BM25's TF and length-normalization both favor D1. It would flip if D4 repeated *blue* more often or were much shorter than D1.",
 "*\"strong pain in the side of the head\"* — the answer (the migraine passage) says *\"sharp sensation localized to one temple\"* and shares almost no words, so keyword search buries it.",
],
"03-text-to-vectors": [
 "Every one-hot vector has a single 1 in a unique slot, so any two distinct words differ in exactly two coordinates and sit the same distance apart. That means the representation encodes identity but zero similarity of meaning.",
 "It throws away **word order** (and grammar); it keeps **which words appear and how often**. So \"dog bites man\" and \"man bites dog\" look identical.",
 "Cosine isolates **direction** (the angle), ignoring vector **length/magnitude**; the raw dot product mixes both, so it grows with length even when the direction (meaning) is unchanged.",
 "**1.0** — same direction means a cosine of 1 regardless of length. (The dot product would differ, but cosine divides out magnitude.)",
 "When the vectors are **L2-normalized** (scaled to unit length): then nearest-by-cosine and nearest-by-Euclidean produce the identical ranking.",
],
"04-embeddings-deep-dive": [
 "To map text to a dense vector so that texts humans consider similar get vectors that are close (high cosine), and dissimilar texts get vectors that are far apart.",
 "word2vec assigns **one fixed vector per word** regardless of context, so both senses of *bank* collapse to the same vector; BERT produces **contextual** vectors that depend on the surrounding sentence, so the two *banks* differ.",
 "A bi-encoder embeds each document **independently of the query**, so document vectors never change per query and can be computed once and reused. That's essential because at search time you only embed the short query and do fast vector math over the precomputed index.",
 "The model was trained (contrastively) to place related texts close together, and a question and its answer are strongly related, so the answer's embedding is typically the nearest neighbor — even without shared words.",
 "You must **re-embed the entire corpus** (and the queries) with the new model. Vectors from different models live in different spaces and aren't comparable, so the old 384-dim index is unusable.",
],
"05-dense-retrieval-semantic-search": [
 "(1) Embed every document once into a matrix (indexing); (2) embed the query; (3) score documents by similarity to the query vector and return the top-k nearest.",
 "Because a bi-encoder embeds documents without seeing the query, their vectors are query-independent and can be computed once and reused for every search. Without that, you couldn't search a large corpus fast.",
 "Exact terms it doesn't understand semantically — e.g. a product code like `SKU-4471-B`, a rare proper name, or the exact string `Lucene`; keyword search matches these exactly while a dense model may drift.",
 "So that the dot product equals cosine similarity. Normalizing removes magnitude effects (which often just reflect length), leaving direction (meaning) — and it's faster than computing full cosine each time.",
 "\"Brute force\" means scoring the query against **every** document (exact, O(N)). It stops being good enough when N grows large (hundreds of thousands+), where the per-query cost becomes too slow — motivating ANN (Chapter 6).",
],
"06-vector-databases-and-ann": [
 "Its cost is proportional to N (corpus size) x dimensions, so every query scans the whole corpus. As N grows to millions, that linear cost blows past the milliseconds users expect.",
 "It approximates the **true set of nearest neighbors** — you may miss a few. The cost of that approximation is measured by **recall@k**: the fraction of the exact top-k that the approximate index actually returns.",
 "It builds a navigable graph linking each vector to near neighbors (with express-lane upper layers), so a query greedily hops toward its neighborhood, visiting only a small subset instead of all vectors.",
 "**Persistence** (save/reload the index), **metadata + filtering**, **CRUD** (add/update/delete), and serving/scaling — everything around the raw ANN index needed to run it as a real service.",
 "No — with only 5,000 vectors, exact search is already fast (sub-millisecond) and simpler. ANN pays off at much larger scales; under ~100k vectors, exact search is usually fine.",
],
"07-reranking": [
 "A cross-encoder reads the query and a document **together**, giving a far more accurate relevance score; the cost is it must run the model for every query-document pair, so it can't be precomputed.",
 "Because it can't precompute: scoring N documents means N model runs **per query**, which is hopelessly slow over a full corpus. The bi-encoder narrows the field first so the cross-encoder only scores a few candidates.",
 "**First-stage recall.** A re-ranker only reorders the candidates it's given; if the relevant document never made the first-stage top-k, no re-ranker can surface it.",
 "Either (a) the right document isn't in the top-10 -> improve **first-stage retrieval** (bigger k, hybrid, better embeddings); or (b) it is but ranked wrong -> use a **stronger/better-matched re-ranker**. Diagnose by checking whether the relevant doc is in the candidate set.",
 "In the **re-ranking** stage — it's the natural place to blend extra signals (recency, popularity, business rules) with the relevance score, on the small candidate set, without slowing first-stage retrieval.",
],
"08-hybrid-search": [
 "They live on different scales (BM25 is unbounded positive; cosine is roughly [-1, 1]), so summing lets BM25's larger numbers dominate arbitrarily and swamp the semantic signal.",
 "It uses each document's **rank** in each list (via 1/(k+rank)), not the raw scores — so it never compares incompatible score scales and is robust to outliers; documents ranked highly by multiple retrievers win.",
 "Because both retrievers ranked D2 and D4 highly, so they accumulate reciprocal-rank contributions from both lists; D10 and D7 appear in only one list, contributing from a single source and scoring lower.",
 "A query mixing an exact term with fuzzy intent, e.g. *\"Lucene for semantic search\"* or *\"SKU-4471-B waterproof jacket\"*: keyword nails the exact token, dense captures the intent, and RRF keeps documents both liked on top.",
 "**After** fusion: hybrid (BM25 ∪ dense -> RRF) produces the candidate set, then the cross-encoder re-ranks those candidates for the final order (BM25 ∪ dense -> RRF -> re-rank -> RAG).",
],
"09-evaluating-search": [
 "**Precision@k**: of the top-k I showed, how many were relevant? **Recall@k**: of all relevant docs, how many did I find in the top-k? **MRR**: how high was the first relevant result? **nDCG**: are the most relevant results near the top?",
 "Because raw DCG grows with the number of relevant documents and isn't comparable across queries; dividing by the **ideal DCG** (the best possible ordering) rescales it to [0, 1] so queries are comparable.",
 "Right when only the single best answer matters (e.g. one passage for RAG, an \"I feel lucky\" result). Misleading when there are many relevant documents and you care about finding all of them or their overall order — MRR only looks at the first hit.",
 "The results are too noisy: with so few queries, one lucky or unlucky query swings the average, and differences between systems aren't statistically significant. Real evaluations use hundreds+ of queries.",
 "You **overfit** to those queries — you'll pick settings that look good on the test set but don't generalize. Tune on a separate dev/validation split and report on a held-out test set.",
],
"10-rag-retrieval-augmented-generation": [
 "**Hallucination** (fluent but false answers) and **stale/missing knowledge**. RAG retrieves relevant, current passages and instructs the model to answer *from them*, so answers are grounded in real evidence and can include your private/up-to-date documents.",
 "**Retrieve** relevant passages for the question; **augment** the prompt with those passages (plus instructions); **generate** an answer grounded in that context. Retrieval supplies the facts; the prompt enforces grounding; generation writes the answer.",
 "The **grounding instruction** (\"use ONLY the context\") stops the model from drawing on unverified memory, and the **refusal clause** (\"say I don't know if it's not there\") gives it permission to decline instead of inventing an answer.",
 "Because the LLM can only answer from what it's given: if the retriever didn't surface the passage containing the answer, the model has nothing correct to work from — so fixing retrieval (chapters 6-8) usually matters more than tweaking the prompt.",
 "When knowledge changes often, must be **citable/verifiable**, or is private/large — RAG injects it at query time and is easy to update. Fine-tuning bakes knowledge into weights (fast at inference, hard to update) and suits fixed style/behavior more than fast-changing facts.",
],
"11-chunking-and-production-pipelines": [
 "(1) Embedding models have **input limits** and silently truncate long text; (2) one vector for a long document **blurs many topics**, hurting retrieval precision; (3) for RAG you want to hand the LLM the **relevant paragraph**, not a whole document (cheaper, less distracting).",
 "Overlap prevents a thought that **straddles a chunk boundary** from being cut in half so neither chunk contains it. Without overlap, answers spanning a seam are lost because no single chunk holds the complete context.",
 "**Load -> Clean -> Chunk -> Embed -> Index.** (Read raw text, strip boilerplate/normalize, split into chunks with metadata, encode each chunk, store vectors + text + metadata in a vector DB.)",
 "**What was actually retrieved.** Most RAG failures are retrieval failures; if the right chunk wasn't retrieved, fix retrieval/chunking, not the prompt. Only if the right chunk *was* retrieved do you debug the generation step.",
 "Because it depends on your documents and queries: too small loses context, too large blurs topics and wastes tokens. Find a good value by **measuring** (Chapter 9 metrics) across a few sizes/overlaps on your own data.",
],
"12-advanced-topics": [
 "HyDE asks an LLM to write a **hypothetical answer** to the query and retrieves using that answer's embedding. It helps because a full answer-like passage sits closer in embedding space to the real answer passages than a short, sparse question does.",
 "It keeps **token-level (per-token) vectors** instead of squashing the text into one vector. **MaxSim** scores a pair by, for each query token, taking its best-matching document token's similarity and summing — preserving fine-grained matches.",
 "Because ColBERT embeds each document's tokens **independently of the query**, so those token vectors can be precomputed and stored. A cross-encoder must read query and document jointly, so nothing can be precomputed.",
 "A multimodal model (e.g. CLIP) embeds images and text into **one shared space**, so a text query vector can be compared to image vectors with the **same nearest-neighbor search** used for text-to-text retrieval in Chapter 5.",
 "When a single retrieve-then-answer pass isn't enough — e.g. **multi-hop** questions needing several lookups, or queries requiring reasoning/tools between retrievals. It costs more latency and complexity, so reserve it for questions single-shot RAG genuinely can't handle.",
],
"13-capstone-project": [
 "*(Reflective — model answer.)* Choose **retrieval only** if users just need to find and read source passages (a search box); choose **RAG** if they need a synthesized, direct answer. Justify by the user's task and whether a written, citable answer adds value over a ranked list.",
 "*(Reflective.)* Report it from your own measurements. Typically **hybrid** helps most when queries mix exact terms and intent; **re-ranking** helps most when first-stage recall is good but ordering is off; **RAG** helps when users want answers, not passages. The right answer is whichever moved your Chapter 9 metrics most on *your* data.",
 "*(Reflective.)* Identify the failing query type, then map it to a technique: missed synonyms -> better embeddings/hybrid (Ch4/8); wrong ordering -> re-ranking (Ch7); answer not in a chunk -> chunking (Ch11); hallucinated answers -> prompt grounding (Ch10); missed exact terms -> hybrid (Ch8).",
 "*(Reflective.)* Usually drop the most expensive stage first — the **cross-encoder re-ranker** (or shrink its candidate set), then consider ANN over exact search. Accept the resulting small drop in nDCG/MRR; measure it so the latency/quality trade-off is explicit.",
 "*(Reflective.)* In plain terms: \"We turn every document into numbers that capture meaning, find the ones closest to the question, [optionally re-check the top few carefully], and [optionally] let an AI write an answer using only those documents.\" Tie each piece back to the words-vs-meaning idea from Chapter 1.",
],
}
