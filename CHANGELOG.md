# Changelog

All notable changes to this project are documented here. The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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

[1.0.0]: https://github.com/mdhabibi/llm-search-handbook/releases/tag/v1.0.0
