#!/usr/bin/env python3
"""Assemble the mkdocs `docs/` tree from the repository.

The course content is authored in place (chapters/, GLOSSARY.md, ...) so it renders
on GitHub. mkdocs cannot use the repo root as its `docs_dir`, so we mirror the
relevant files into `docs/` — preserving folder structure so every relative link
(../../slides, ../../src, ../../GLOSSARY.md) keeps resolving. `docs/` is generated
and git-ignored; run this before `mkdocs build` / `mkdocs serve`.
"""
from __future__ import annotations

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"

# Top-level files and directories to publish, mirrored 1:1 into docs/.
INCLUDE = [
    "README.md",
    "ROADMAP.md",
    "GLOSSARY.md",
    "CONTRIBUTING.md",
    "CODE_OF_CONDUCT.md",
    "CHANGELOG.md",
    "CONTENT-LICENSE.md",
    "CITATION.cff",
    "LICENSE",
    "VERSION",
    "scripts",
    "Search-Semantically-ebook.pdf",
    "ebook/build.sh",
    "ebook/protect.sh",
    "chapters",
    "slides",
    "src",
    "data",
    "assets",
    "setup",
]

# Junk never worth copying into a built site.
IGNORE = shutil.ignore_patterns(
    "__pycache__", "*.pyc", ".ipynb_checkpoints", ".DS_Store"
)


def main() -> None:
    if DOCS.exists():
        shutil.rmtree(DOCS)
    DOCS.mkdir(parents=True)

    for name in INCLUDE:
        src = ROOT / name
        if not src.exists():
            print(f"skip (missing): {name}")
            continue
        dst = DOCS / name
        if src.is_dir():
            shutil.copytree(src, dst, ignore=IGNORE)
        else:
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
        print(f"copied: {name}")

    print(f"\ndocs/ assembled at {DOCS}")


if __name__ == "__main__":
    main()
