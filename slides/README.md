# Slides

Presentation decks for the course — one per chapter. Great for teaching, talks, or a quick
visual tour. They follow the same visual identity as the rest of the repo (indigo→blue→violet
gradient, a "semantic space" dot motif, dark title/closing slides with light content slides).

> **Sample so far:** Chapter 2 (Keyword / Lexical Search). More chapters follow the same template.

## What's here

| File | Use |
|------|-----|
| `Chapter-02-Keyword-Search.pptx` | **Branded** editable PowerPoint (open in PowerPoint, Keynote, or Google Slides) |
| `Chapter-02-Keyword-Search.pdf` | Branded deck — ready-to-present / preview PDF |
| `Chapter-02-Keyword-Search-NotebookLM.pptx` | **Illustrated "blueprint" deck** generated with NotebookLM (watermark removed) |
| `Chapter-02-Keyword-Search-NotebookLM.pdf` | NotebookLM deck — preview PDF |
| `gamma/Chapter-02-Keyword-Search.md` | Paste-in outline for [Gamma](https://gamma.app) to auto-design slides |
| `notebooklm/Chapter-02-Keyword-Search.source.md` | Upload to [NotebookLM](https://notebooklm.google.com) to generate a deck (see `notebooklm/README.md`) |
| `build/` | Scripts + assets used to generate the branded deck (reproducible) |

> **Two visual styles per chapter:** a clean *branded* deck (matches the repo's identity) and an
> *illustrated* deck (NotebookLM's schematic style). Pick whichever fits your talk.

## Two ways to make/edit slides

**1. Use the PowerPoint (recommended for editing).** Open the `.pptx`, tweak any text — it's
real editable text, not images. The gradient backgrounds and diagrams are embedded images.

**2. Use Gamma (for AI-designed variety).** Open [gamma.app](https://gamma.app) → *New* →
**Paste in text**, and paste the contents of `gamma/Chapter-02-Keyword-Search.md`. Gamma turns
the outline into a polished deck you can restyle with one click. The outline already has titles,
bullets, a table, the formulas, key-term chips, and layout hints.

## Deck structure (per chapter)

Title → the problem → intuition (analogy) → the mechanics (diagram) → worked example →
key formula → pitfalls → key terms → check-your-understanding → recap / next.

## Rebuilding the PowerPoint

The deck is generated with [pptxgenjs](https://gitbrent.github.io/PptxGenJS/); the branded
backgrounds, diagrams, and formulas are rendered with `cairosvg` + `matplotlib`.

```bash
cd build
python3 gen_assets.py          # renders backgrounds, diagrams, formula images → assets/
node   build_deck.js           # writes the .pptx  (needs: npm i pptxgenjs)
# preview: soffice --headless --convert-to pdf Chapter-02-Keyword-Search.pptx
```

(The shipped `.pptx` is self-contained — the images are embedded, so you don't need to rebuild
to present it.)
