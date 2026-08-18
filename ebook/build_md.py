import re, os
import os as _os
OUT=_os.path.dirname(_os.path.abspath(__file__))
ROOT=_os.path.dirname(OUT)
import sys; sys.path.insert(0, OUT)
from answers import ANSWERS

# --- unicode sanitizer: replace glyphs xelatex/main-font can't render ---
REPL = {
 "🟢":"","🟡":"","🔴":"","🟩":"","🟨":"","⬜":"","🎉":"","💡":"","✅":"[yes] ","❌":"[no] ",
 "⚠️":"[!] ","⚠":"[!] ","✓":"(check)","➡":"->",
 "→":" -> ","←":" <- ","⟶":" -> ",
 "▶":">","▲":"^","●":"*","◀":"<",
 "╲":"\\","╱":"/","∪":" U ","∈":" in ","×":"x","−":"-",
 "≈":"~=","≥":">=","≤":"<=","≠":"!=",
 "α":"alpha","β":"beta","·":"-",
 "⁰":"0","¹":"1","²":"2","³":"3","⁴":"4","⁵":"5","⁶":"6","⁷":"7","⁸":"8","⁹":"9",
 "½":"1/2","¼":"1/4","¾":"3/4","•":"-","…":"...",
 "₀":"0","₁":"1","₂":"2","₃":"3","₄":"4","₅":"5","₆":"6","₇":"7","₈":"8","₉":"9",
 "“":'"',"”":'"',"‘":"'","’":"'",
}
def sanitize(s):
    for k,v in REPL.items(): s=s.replace(k,v)
    s=re.sub(r"[\U0001F000-\U0001FAFF\U00002190-\U000021FF\U00002600-\U000027BF\uFE0F]","",s)
    return s

def strip_answer_blocks(md):
    return re.sub(r"<!-- cyu-answers:start -->.*?<!-- cyu-answers:end -->\n?", "", md, flags=re.DOTALL)

def unnumber_headings(md):
    out=[]; infence=False
    for ln in md.split("\n"):
        if ln.lstrip().startswith("```"):
            infence=not infence; out.append(ln); continue
        if not infence:
            m=re.match(r"^(#{1,6})\s+(.*\S)\s*$", ln)
            if m and not ln.rstrip().endswith("}"):
                ln=f"{ln.rstrip()} {{.unnumbered}}"
        out.append(ln)
    return "\n".join(out)

def load(p): return open(os.path.join(ROOT,p),encoding="utf-8").read()

def chapter_title(md):
    m=re.search(r"^#\s+(.*\S)\s*$", md, flags=re.MULTILINE)
    return m.group(1) if m else "Chapter"

def extract_questions(md):
    """Pull the numbered questions under '## Check your understanding'."""
    m=re.search(r"^## Check your understanding\s*$", md, flags=re.MULTILINE)
    if not m: return []
    tail=md[m.end():]
    stop=re.search(r"(^## |<!-- cyu-answers)", tail, flags=re.MULTILINE)
    block=tail[:stop.start()] if stop else tail
    qs=re.findall(r"^\s*\d+\.\s+(.*\S)\s*$", block, flags=re.MULTILINE)
    return qs

chapters = [
 "chapters/00-introduction/README.md",
 "chapters/01-foundations-of-information-retrieval/README.md",
 "chapters/02-keyword-lexical-search/README.md",
 "chapters/03-text-to-vectors/README.md",
 "chapters/04-embeddings-deep-dive/README.md",
 "chapters/05-dense-retrieval-semantic-search/README.md",
 "chapters/06-vector-databases-and-ann/README.md",
 "chapters/07-reranking/README.md",
 "chapters/08-hybrid-search/README.md",
 "chapters/09-evaluating-search/README.md",
 "chapters/10-rag-retrieval-augmented-generation/README.md",
 "chapters/11-chunking-and-production-pipelines/README.md",
 "chapters/12-advanced-topics/README.md",
 "chapters/13-capstone-project/README.md",
]

preface = """# Preface {.unnumbered}

**Search Semantically** is a hands-on course on how modern search works — from classic keyword
matching to embeddings, dense retrieval, re-ranking, evaluation, and Retrieval-Augmented
Generation (RAG). Every chapter pairs intuitive explanations (analogies, diagrams, worked
examples) with runnable code, so you learn the idea *and* how to build it.

The toolkit is open-source and key-free (sentence-transformers, FAISS, Chroma, rank-bm25), so
everything runs locally. Difficulty is marked per chapter: Beginner, Intermediate, Advanced.

By the end you will be able to: explain how keyword search works and why it falls short; turn
text into meaning-vectors with embeddings; build a semantic search engine; scale it with a vector
database; sharpen it with re-ranking and hybrid search; evaluate it properly; and plug it into an
LLM to build a grounded question-answering system.

Each chapter ends with *Check your understanding* questions; **model answers are collected in the
Answers appendix** near the end of this book. This is the companion text to the code repository of
the same name; each chapter maps to a folder with a notebook you can run.
"""

parts=[preface]
answers_sections=["# Answers to Check Your Understanding {.unnumbered}",
 "",
 "*Model answers to the end-of-chapter questions. Try each question yourself before reading these.*",
 ""]

for c in chapters:
    raw=load(c)
    d=c.split("/")[1]  # chapter folder name
    # collect Q&A for the appendix (from raw, before sanitize)
    qs=extract_questions(raw)
    ans=ANSWERS.get(d,[])
    title=chapter_title(raw)
    answers_sections.append(f"## {sanitize(title)} {{.unnumbered}}")
    answers_sections.append("")
    for i in range(max(len(qs),len(ans))):
        q=qs[i] if i<len(qs) else ""
        a=ans[i] if i<len(ans) else ""
        if q: answers_sections.append(f"**Q{i+1}. {sanitize(q)}**")
        answers_sections.append("")
        if a: answers_sections.append(sanitize(a))
        answers_sections.append("")
    # chapter body for the PDF: strip the collapsible answers, then sanitize
    parts.append(sanitize(strip_answer_blocks(raw)))

parts.append("\n".join(answers_sections))
parts.append(sanitize(load("GLOSSARY.md")))

book="\n\n\\newpage\n\n".join(unnumber_headings(p) for p in parts)
open(os.path.join(OUT,"book.md"),"w",encoding="utf-8").write(book)
print("book.md written:", len(book), "chars; chapters:", len(chapters))
