# Environment Setup

This is a **one-time** setup. After this you can run every notebook in the course locally,
with no paid API keys required (we use open-source models).

## 1. Prerequisites

- **Python 3.10–3.12** (`python --version`)
- **git**
- ~3–5 GB free disk space (embedding models download on first use)
- A CPU is fine for everything in the course. A GPU just makes it faster.

## 2. Create a virtual environment

```bash
cd "Search Semantically"
python -m venv .venv

# Activate it:
source .venv/bin/activate        # macOS / Linux
# .venv\Scripts\activate         # Windows (PowerShell)
```

## 3. Install dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

> First run note: the first time you load an embedding model (e.g.
> `sentence-transformers/all-MiniLM-L6-v2`), it downloads (~90 MB) and caches locally.

## 4. Launch Jupyter

```bash
jupyter lab        # or: jupyter notebook
```

Open any chapter's `notebooks/` folder and run the cells top to bottom.

## 5. Verify your install

Run this in a Python shell or a notebook cell:

```python
from sentence_transformers import SentenceTransformer
model = SentenceTransformer("all-MiniLM-L6-v2")
print(model.encode("hello world").shape)   # -> (384,)
```

If that prints `(384,)`, you're ready.

## Optional: the LLM for the RAG chapters

Chapters 10–11 use a text-generation model. We default to a **small open-source** model so it
runs locally. If you'd rather use a hosted API, each RAG notebook notes where to swap it in —
but it's never required to complete the course.

## Troubleshooting

- **`pip` is slow or fails on torch** — install the CPU build first:
  `pip install torch --index-url https://download.pytorch.org/whl/cpu`, then re-run
  `pip install -r requirements.txt`.
- **Out of memory** — close other notebooks; the small models here need < 2 GB RAM.
- **Behind a proxy / offline** — pre-download models on a connected machine; Hugging Face
  caches under `~/.cache/huggingface`.
