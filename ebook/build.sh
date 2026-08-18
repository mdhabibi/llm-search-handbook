#!/usr/bin/env bash
# Rebuild the ebook PDF from the chapter READMEs. Requires pandoc + xelatex + DejaVu fonts.
# (Regenerate the cover/graphics first with: python3 ../assets/make_graphics.py)
set -e
cd "$(dirname "$0")"
python3 build_md.py
pandoc book.md -o ../Search-Semantically-ebook.pdf --pdf-engine=xelatex \
  --toc --toc-depth=1 -V documentclass=report -V papersize=a4 -V geometry:margin=2.4cm \
  -V fontsize=11pt --highlight-style=tango  -H header.tex -B cover.tex
echo "Rebuilt ../Search-Semantically-ebook.pdf"
