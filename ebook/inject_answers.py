import re, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from answers import ANSWERS

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # repo root
START, END = "<!-- cyu-answers:start -->", "<!-- cyu-answers:end -->"

def build_block(ans_list):
    parts = [START,
             "",
             "> 💡 *Try answering each question yourself first, then expand to check.*",
             ""]
    for i, a in enumerate(ans_list, 1):
        parts += ["<details>",
                  f"<summary><b>Show answer — {i}</b></summary>",
                  "",
                  a,
                  "",
                  "</details>",
                  ""]
    parts.append(END)
    return "\n".join(parts)

for d, ans in ANSWERS.items():
    p = os.path.join(ROOT, "chapters", d, "README.md")
    s = open(p, encoding="utf-8").read()
    # remove any previous injected block (idempotent)
    s = re.sub(re.escape(START)+r".*?"+re.escape(END)+r"\n?", "", s, flags=re.DOTALL)
    # locate the "Check your understanding" section
    m = re.search(r"^## Check your understanding\s*$", s, flags=re.MULTILINE)
    if not m:
        print("!! no CYU section in", d); continue
    # find the next "## " heading after it -> insert block just before it
    nxt = re.search(r"^## ", s[m.end():], flags=re.MULTILINE)
    insert_at = m.end() + nxt.start() if nxt else len(s)
    block = build_block(ans) + "\n\n"
    s = s[:insert_at] + block + s[insert_at:]
    open(p, "w", encoding="utf-8").write(s)
    print(f"injected {len(ans)} answers -> {d}")
print("done")
