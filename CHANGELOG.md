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
- **`assets/make_embedding_maps.py`** — reproducible generator for all four figures.
- **Slide decks for all 14 chapters** in `slides/`, linked from each chapter README and from
  the learning-path table.
- **Notebook and slides columns** in the main README's learning-path table.

### Changed
- `ebook/build_md.py` now rewrites chapter figure paths and pins figure widths, so images from
  the chapter READMEs render correctly in the e-book.
- E-book rebuilt with the new Chapter 4 figures (69 -> 76 pages).

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
