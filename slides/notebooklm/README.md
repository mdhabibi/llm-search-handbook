# NotebookLM slide sources

[NotebookLM](https://notebooklm.google.com) generates decks (and audio/video overviews) that are
**grounded strictly on the sources you upload** — so the output is only as good as the source.
These `*.source.md` files are clean, self-contained "slide scripts" written for exactly that:
each has learning objectives, the narrative broken into slide beats, the exact examples and
numbers, diagram descriptions, key terms, a Q&A, and a suggested slide outline for NotebookLM to
mirror.

> Sample so far: `Chapter-02-Keyword-Search.source.md`.

## How to generate the slides (5 steps)

1. Open **notebooklm.google.com** → **New notebook**.
2. **Add source** → upload the chapter's `*.source.md` from this folder
   (or paste its contents via *Add source → Copied text*).
3. Open the **Studio** panel (right side).
4. Choose the slide/deck or **Video Overview** option (NotebookLM's Studio formats vary by
   region/rollout; pick the visual/slides one).
5. Click **Customize** and paste the prompt below, then generate. Regenerate if you want a
   different length or emphasis.

## Prompt to paste into NotebookLM's "Customize" box

```
Create about 12 slides that follow the "Suggested slide outline" in the source exactly, one
concept per slide. Keep it beginner-friendly and visual: a short title, 3–4 concise bullets,
and one diagram or example per slide. Preserve the concrete examples and numbers — the "grass"
shared-words example, the inverted-index term→postings diagram, the TF-IDF table with
score(D0) ≈ 2.12, and BM25's two knobs (k1 = term saturation, b = length normalization). End
with the key terms and the check-your-understanding questions. Avoid dense paragraphs.
```

## Tips for the best result

- **One chapter per notebook** keeps the deck focused (NotebookLM blends all sources together).
- You can also upload the whole **e-book PDF** (`../../Search-Semantically-ebook.pdf`) and tell
  it which chapter to focus on — but a single `*.source.md` gives tighter, on-message slides.
- NotebookLM won't import our branded PNG diagrams; it generates its own visuals from the
  **descriptions** in the source (that's why each diagram is described in words).
- Want the branded look instead? Use the PowerPoint/Gamma decks in the parent `slides/` folder.
