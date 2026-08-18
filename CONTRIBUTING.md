# Contributing

Thanks for your interest in improving **Search Semantically**! This is an educational
resource, so contributions that make it clearer, more correct, or more complete are very
welcome.

## Ways to help

- **Fix errors** — a wrong formula, a broken link, a typo, a confusing sentence.
- **Improve explanations** — a better analogy, a clearer diagram, a sharper example.
- **Strengthen the code** — bugs in notebooks or `src/` modules, extra tests, clarity.
- **Add exercises or answers** — more *Check your understanding* items (with answers).
- **Suggest topics** — open an issue proposing a new section or *Going Deeper* note.

## Ground rules

- **Keep it original.** All content must be your own words, not copied from courses, books,
  or other sites. Cite primary sources (papers, docs) in the chapter's *References*.
- **Match the style.** Intuition first, then mechanics; short worked examples; a diagram
  where it helps; difficulty-appropriate depth. Prose over walls of bullet points.
- **Keep it runnable.** Code should run with the pinned `requirements.txt`, open-source and
  key-free by default. Verify notebooks execute top to bottom before submitting.
- **One idea per PR.** Small, focused pull requests are easier to review and merge.

## Workflow

1. Fork the repo and create a branch: `git checkout -b fix/chapter-2-idf-typo`.
2. Make your change. If you edit a chapter, keep the section template consistent.
3. If you change **answers**, edit `ebook/answers.py` (the single source), then run
   `python3 ebook/inject_answers.py` to update the README dropdowns.
4. If you change chapter content and want to refresh the e-book, run `ebook/build.sh`
   (requires `pandoc` + `xelatex` + DejaVu fonts).
5. Commit with a clear message and open a pull request describing what and why.

## Reporting issues

Open a GitHub issue with:
- the chapter/file and section,
- what's wrong or unclear,
- (if applicable) the corrected version or a suggestion.

By contributing, you agree that your contributions are licensed under the project's terms:
MIT for code and CC BY 4.0 for content (see [LICENSE](LICENSE) and
[CONTENT-LICENSE.md](CONTENT-LICENSE.md)).
