"""Rebuild 'My Python Adventures.ipynb' from the chapter files (missions, code, bug hunts)."""
import re, json, pathlib
root = pathlib.Path(__file__).resolve().parent.parent
ch = root / "chapters"
def md(text): return {"cell_type": "markdown", "metadata": {}, "source": text.strip("\n").splitlines(True)}
def code(text): return {"cell_type": "code", "metadata": {}, "execution_count": None, "outputs": [], "source": text.strip("\n").splitlines(True)}
def clean(t):
    t = re.sub(r"\\texttt\{([^{}]*)\}", r"`\1`", t); t = re.sub(r"\\textbf\{([^{}]*)\}", r"**\1**", t)
    t = re.sub(r"\\py\|([^|]*)\|", r"`\1`", t); t = t.replace("``", '"').replace("''", '"').replace("\\&", "&").replace("~", " ")
    return re.sub(r"\\[a-zA-Z]+\*?(\[[^]]*\])?", "", t).replace("{", "").replace("}", "").strip()
START = "from ColabTurtlePlus.Turtle import *\nclearscreen()\ninitializeTurtle((480, 360))"
cells = [md("""# 🐢 My Python Adventures
### The notebook that goes with your workbook *From Scratch to Python*

Hello, coder! Every mission in your workbook has a place here.

* The grey boxes are **code cells**. Click the round **▶ play button** on the left of a cell to run it. That's your green flag!
* You can also click inside a cell and press **Shift + Enter**.
* Each mission shows the code from the workbook. **Type it yourself** into the empty cell underneath, letter by letter. Typing it is how you learn!
* Made a mess? That's fine. Delete what you typed and try again."""),
 md("""## ⭐ The magic first cell
**Run this cell first, every time you open this notebook.** It downloads the turtle drawing tools, like clicking *Extensions* and adding *Pen* in Scratch.

⚠️ It must say **ColabTurtlePlus** (with *Plus*). A library called ColabTurtle is a different one and won't work with this book."""),
 code("!pip install ColabTurtlePlus"),
 md(f"""## 🟨 The three starting lines
Every drawing starts with these three lines. They do the job of **when green flag clicked**: they get the stage (480 by 360, just like Scratch) and the turtle ready.
```python
{START}
```
After them you just write commands like `forward(100)`. Run this cell to try:"""),
 code(START + "\nforward(100)")]
n = 0
for f in sorted(ch.glob("0[1-8]-*.tex")):
    if f.name.endswith("-answers.tex"): continue
    s = f.read_text()
    m = re.search(r"\\partopener\{[^}]*\}\{([^}]*)\}\{([^}]*)\}", s)
    head = (m.group(1).title() + ": " + m.group(2)) if m and m.group(1).upper().startswith("PART") else (m.group(2) if m else f.stem)
    cells.append(md(f"---\n# {head}"))
    marks = [(mm.start(), "mission", clean(mm.group(1))) for mm in re.finditer(r"\\mission\{((?:[^{}]|\{[^{}]*\})*)\}", s)]
    marks += [(mm.start(), "sub", clean(mm.group(1))) for mm in re.finditer(r"\\subsection\*\{((?:[^{}]|\{[^{}]*\})*)\}", s)]
    marks.sort()
    groups = []
    for bm in re.finditer(r"\\begin\{typethis\}(?:\[[^]]*\])?\n(.*?)\\end\{typethis\}", s, re.S):
        prev = [k for k in marks if k[0] < bm.start()]
        mission = next((k for k in reversed(prev) if k[1] == "mission"), None)
        label = prev[-1] if prev else (0, "sub", head)
        key = mission if (mission and not [k for k in prev if k[0] > mission[0] and k[1] == "sub" and "Translate" in k[2]]) else label
        if groups and groups[-1][0] == key: groups[-1][1].append(bm.group(1).rstrip())
        else: groups.append((key, [bm.group(1).rstrip()]))
    seen = set()
    for key, blocks in groups:
        title = key[2]
        if key[1] == "mission":
            if key not in seen: n += 1; seen.add(key)
            heading = f"## Mission {n}: {title}"
        else:
            heading = f"## {title}"
        src = "\n".join(blocks)
        cells.append(md(f"{heading}\n**Type this into the cell below** (it's on the mission's page in your workbook):\n```python\n{src}\n```"))
        cells.append(code("# Type your code here, then press the play button ▶"))
        cells.append(code("# Make it yours: try a challenge from the workbook here"))
bz = (ch / "09-bug-zoo.tex").read_text()
hunts = re.findall(r"\\bzhunt\{(\d+)\}\{((?:[^{}]|\{[^{}]*\})*)\}\s*\\begin\{code\}\n(.*?)\\end\{code\}", bz, re.S)
cells.append(md("---\n# 🐞 The Bug Hunt\nEach cell below has **one bug** (it's from the Bug Zoo in your workbook). Run it, read the **last line** of the red writing, fix the code and run it again. Some bugs are sneaky and show **no** red writing: check what the program really did!\n\nTip: Colab says a name is *not defined* but won't guess the right word, so check your spelling and capital letters very carefully."))
for num, desc, src in hunts:
    cells.append(md(f"**Bug hunt {num}.** {clean(desc)}"))
    cells.append(code(src.rstrip()))
cells.append(md("---\n# 🎨 Free play\nPick one of **your own** Scratch projects and write it in Python here. Keep the Block Dictionary in your workbook open to help you."))
cells.append(code(START + "\n\n# My own project"))
cells.append(md("""---
### If something goes wrong
* **A cell keeps running?** Click the ■ stop button where the play button was.
* **`No module named 'ColabTurtlePlus'`?** Run the magic first cell again.
* **`NameError`?** Check the spelling, or run the cells above first. You can also open the **Runtime** menu and choose **Run all**.
* Under an error, the **Explain error** button can help, but be the detective first!"""))
nb = {"cells": cells, "metadata": {"colab": {"provenance": [], "toc_visible": True}, "kernelspec": {"name": "python3", "display_name": "Python 3"}, "language_info": {"name": "python"}}, "nbformat": 4, "nbformat_minor": 0}
(root / "My Python Adventures.ipynb").write_text(json.dumps(nb, indent=1, ensure_ascii=False))
print(len(cells), "cells,", n, "missions,", len(hunts), "bug hunts")
