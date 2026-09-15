# Changelog

All notable changes to this project are documented here. The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] — 2026-09-15

### Added
- **Embedding maps in Chapter 4** — four generated figures that make the vector space visible:
  question/answer pairs landing beside each other, a semantic atlas of ~150 everyday terms
  across eight themes, the same atlas in 3-D, and a UMAP-vs-PCA comparison.
- **UMAP section in the Chapter 4 notebook** — a `project()` helper offering both UMAP and PCA
  (UMAP optional; falls back to PCA automatically), 2-D and 3-D plots, a side-by-side
  comparison, and guidance on which projection to trust for which claim.
- **Chapter 7 depth on why re-ranking exists** — a new *"Similar is not the same as relevant"*
  section (similarity vs. answerhood vs. truth, with a distractor table showing how a *false*
  sentence can outrank the correct one), a *How a re-ranker learns relevance* section on
  positive pairs and hard-negative mining, and a notebook demo re-ranking a wide BM25 candidate
  list to rescue a weak keyword first stage. Two new questions, answers, and glossary entries
  (*relevance score*, *hard negative*).
- **Chapter 10 on the generation half's real behaviour** — a *Generation is not deterministic*
  section (sampling, temperature, judging a prompt over several runs rather than one), an
  explanation of `max_new_tokens` and mid-sentence truncation, and a *What people actually build
  with this* table mapping the RAG pattern to shipped products. Two notebook sections, two new
  questions and answers, and four glossary entries (*temperature*, *sampling / greedy decoding*,
  *max tokens*, expanded *context window*).
- **`assets/make_embedding_maps.py`** — reproducible generator for all four figures.
- **Slide decks for all 14 chapters** in `slides/`, linked from each chapter README and from
  the learning-path table.
- **Notebook and slides columns** in the main README's learning-path table.

### Changed
- `ebook/build_md.py` now rewrites chapter figure paths and pins figure widths, so images from
  the chapter READMEs render correctly in the e-book.
- `ebook/build_md.py` now joins multi-line *Check your understanding* questions (previously a
  wrapped question was truncated mid-sentence in the Answers appendix) and strips nested
  emphasis markers that rendered as literal asterisks.
- E-book rebuilt with the new Chapter 4, 7 and 10 material (69 -> 79 pages).

### Dependencies
- Added `umap-learn` (optional — the notebook falls back to PCA when it is absent).

## [1.0.0] — 2026-08-18

First complete release. The full course is written, verified, and publish-ready.

### Added
- **14 chapters** (0–13), each with a full written lesson (intuition, diagrams, worked
  examples, pitfalls, exercises, references) and a runnable Jupyter notebook.
- **Reusable modules** in `src/`: `corpus.py`, `semantic_search.py`, `metrics.py`,
  `chunking.py`, `search_stack.py`.
- **Shared data**: sample corpus and a labeled evaluation set.
- **Answer key** for every *Check your understanding* question — collapsible dropdowns on
  GitHub and a dedicated appendix in the e-book.
- **E-book**: a colorful, typeset PDF of the whole course (cover, TOC, callouts, math,
  diagrams, answers appendix) plus reproducible build scripts in `ebook/`.
- **E-book attribution**: per-page footer + diagonal watermark, embedded PDF author
  metadata, and an optional `qpdf` protection script (`ebook/protect.sh`).
- **Project metadata**: MIT (code) + CC BY 4.0 (content) licensing, `CITATION.cff`,
  `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, brand graphics, and this changelog.

[1.1.0]: https://github.com/mdhabibi/llm-search-handbook/releases/tag/v1.1.0
[1.0.0]: https://github.com/mdhabibi/llm-search-handbook/releases/tag/v1.0.0
