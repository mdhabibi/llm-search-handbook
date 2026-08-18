#!/usr/bin/env bash
# Produce a restricted "distribution" copy of the e-book.
#
# Readers can OPEN and PRINT it, but copying text and modifying the file are
# disabled. This is a deterrent, not unbreakable DRM — but combined with the
# per-page footer + watermark + embedded author metadata, any copy stays clearly
# attributed to Dr. Mahdi Habibi.
#
# Requires: qpdf.  The protected file is NOT committed (see .gitignore).
#
# Usage:
#   OWNER_PW='your-secret' ebook/protect.sh
#   # or
#   ebook/protect.sh 'your-secret'
set -e
cd "$(dirname "$0")/.."
OWNER_PW="${OWNER_PW:-$1}"
if [ -z "$OWNER_PW" ]; then
  echo "Set an owner password, e.g.:  OWNER_PW='secret' ebook/protect.sh"
  exit 1
fi
qpdf --encrypt "" "$OWNER_PW" 256 \
     --modify=none --extract=n --annotate=n --print=full -- \
     Search-Semantically-ebook.pdf Search-Semantically-ebook-protected.pdf
echo "Wrote Search-Semantically-ebook-protected.pdf"
echo "  - opens without a password; printing allowed"
echo "  - copying text and editing are disabled (owner password required to change permissions)"
