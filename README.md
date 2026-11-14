# From Scratch to Python

**🌐 Website: <https://setopy.github.io/JesusArrows-scratch2python/>**

**🇲🇽 Spanish edition, *De Scratch a Python*: <https://setopy.github.io/de-scratch-a-python/>** ([source](https://github.com/Setopy/de-scratch-a-python))

[![Open the notebook in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Setopy/JesusArrows-scratch2python/blob/main/My%20Python%20Adventures.ipynb)

A workbook for a 9-year-old who already knows [Scratch](https://scratch.mit.edu) and is ready for real Python. It maps every Scratch 3.0 block category to runnable Python in **Google Colab**, side by side, with turtle graphics standing in for the Scratch stage. Nothing needs installing: a browser and a Google account are enough.

> You already know how to code. Every time you snap Scratch blocks together, you are writing a program. Python uses the same ideas: you just type the words instead of dragging blocks.

| | |
|---|---|
| 📘 **The book** | [`scratch-to-python-workbook.pdf`](scratch-to-python-workbook.pdf): 258 pages, 35 missions, answers at the back |
| 🐢 **The notebook** | [`My Python Adventures.ipynb`](My%20Python%20Adventures.ipynb): every mission's code, with an empty cell to type into |
| 🔬 **The research** | [`research/`](research/): 20 notes on how each Scratch block maps to Python, with an overview in [`00-curriculum-map.md`](research/00-curriculum-map.md) |

## Quick start for grown-ups

1. **Print or open the PDF.** Read *For grown-ups* near the back first (about 10 minutes).
2. **Open the notebook in Colab** with the badge above, then choose *File → Save a copy in Drive* so your child's work is saved.
3. **Run the “In the beginning” cell** (`!pip install ColabTurtlePlus`) every time you open the notebook.
4. **Work through one mission per session** (20–30 minutes). Each mission has five steps: build it in Scratch, type it in Colab, read it line by line, run it, make it yours.

## What a mission looks like

| Scratch | Python |
|---|---|
| when green flag clicked | *(press the ▶ play button)* |
| repeat 4 | `for i in range(4):` |
| move 100 steps | `    forward(100)` |
| turn ↻ 90 degrees | `    right(90)` |

```python
from ColabTurtlePlus.Turtle import *
clearscreen()
initializeTurtle((480, 360))   # the same 480 x 360 stage as Scratch

for i in range(4):
    forward(100)
    right(90)
```

## What's inside the book

| Section | Scratch blocks | Python it teaches | Missions |
|---|---|---|---|
| Front pages | | Meet Colab, Scratch words and Python words, four new habits | |
| **Part 1: Motion and Pen** | Motion, Pen | `forward`, `right`, `goto`, `setheading`, `pencolor`, `stamp` | 3 |
| **Part 2: Loops** | Control (loops) | `for i in range()`, `while True`, nested loops, `time.sleep` | 4 |
| **Part 3: Variables and Lists** | Variables, Lists | `=`, `+=`, lists, `append`, counting from 0 | 4 |
| **Part 4: Operators** | Operators | maths, `random.randint`, `==`, joining text, `%`, `round` | 4 |
| **Part 5: Sensing and Decisions** | Sensing, Control (if) | `input()`, `int()`, `if`/`elif`/`else`, `while`, timers, touching | 4 |
| **Part 6: My Blocks** | My Blocks, clones | `def`, inputs, `return`, extra sprites with `Turtle()` | 4 |
| **Part 7: Looks, Sound and Events** | Looks, Sound, Events | costumes, `beep()` music, broadcasts as functions, the game loop | 4 |
| **Big Projects** | everything | eight games, from *Animate your name* to *Chase game* | 8 |
| **The Bug Zoo** | | reading errors, 12 common bugs, 10 bug hunts | |
| **Block Dictionary** | all 147 blocks | the Python for every Scratch block, plus a cheat sheet | |
| **For grown-ups** | | running a session, suggested pace, Colab tips, Thonny | |

Each part ends with a *Translate it yourself* exercise, a two-line puzzle and an "I can…" checklist.

### Why this order?

The parts don't follow Scratch's block palette. Research on moving from blocks to text (Weintrop & Wilensky, 2019; Dann et al., 2012) suggests starting with drawing and loops and leaving events and key presses until after functions. That's because events are the hardest Scratch idea to carry into text code. The book also says the link between each block and its line of code out loud, which that research found matters most. Details are in [`research/17-pedagogy.md`](research/17-pedagogy.md).

## About the Colab setup

The book uses [ColabTurtlePlus](https://pypi.org/project/ColabTurtlePlus/) in the `initializeTurtle()` style, which was tested in Colab on 8 Nov 2026 with Python 3.13 and ColabTurtlePlus 2.2.0. Things worth knowing:

- **Install `ColabTurtlePlus`, not `ColabTurtle`.** The similarly named original library has no `Turtle()`, a black 800×500 window and (0, 0) in the top-left corner.
- **Directions differ from Scratch.** Turning works the same, but for "point in direction" use `setheading(90 - d)`. Don't use `mode("logo")`: in version 2.2 it makes `setheading(90)` point down.
- **`distance()` and `towards()` take a position, not a sprite.** Write `cat.distance(dog.pos())`.
- **Colab can't hear key presses or mouse clicks**, so the Colab programs ask with `input()`. Real key-press games are in the Thonny section of Part 7.

## Repository layout

```
scratch-to-python-workbook.tex   main file: \input's the preamble and every chapter
scratch-to-python-workbook.pdf   the compiled book
preamble.tex                     shared look: colours, boxes, code listings, mission macros
My Python Adventures.ipynb       the Colab notebook (generated from the chapters)
chapters/
  00-front.tex ... 11-grown-ups.tex   one file per part, plus NN-*-answers.tex
  NN-colab-tests.py                   every drawing program from that chapter
  STYLE.md                            the style rules all chapters follow
  _make_mission_chart.py              rebuilds 00-mission-chart.tex
  _make_notebook.py                   rebuilds the notebook
  _colab/build_runner.py              packs the tests into one-line Colab cells
  _harness.tex, _test-NN.tex          compile one chapter on its own
research/
  00-curriculum-map.md                overview of the 20 research notes
  01-motion.md ... 20-projects.md     one note per Scratch area or topic
  18-sb3-tools/                       a small .sb3-to-turtle converter (proof of concept)
*-v2-backup.*                    the earlier, shorter edition
```

## Building and testing

**Build the PDF** with [Tectonic](https://tectonic-typesetting.github.io), which downloads the LaTeX packages it needs on the first run:

```bash
tectonic scratch-to-python-workbook.tex
```

**After editing a chapter**, rebuild the mission chart and the notebook:

```bash
python3 chapters/_make_mission_chart.py
```

```bash
python3 chapters/_make_notebook.py
```

**Check one chapter on its own**, for example Part 2:

```bash
mkdir -p chapters/_build-02 && tectonic -o chapters/_build-02 chapters/_test-02.tex
```

**Test every drawing program in Colab.** Run `python3 chapters/_colab/build_runner.py`, then paste each line from `chapters/_colab/cell_A.txt`, `cell_B.txt` and `cell_C.txt` into a Colab cell after the “In the beginning” cell. Each cell runs its chapters' programs against the real library and prints PASS or FAIL for each. Last run (8 Nov 2026): 91 pass and 2 skipped (one runs forever by design, one needs a local file). The one failure was the Bug Zoo's broken-on-purpose example, failing as intended.

## Credits

- [ColabTurtlePlus](https://github.com/mathriddle/ColabTurtlePlus) by Larry Riddle, building on Tolga Atam's [ColabTurtle](https://github.com/tolgaatam/ColabTurtle)
- Scratch block pictures drawn with the [`scratch3`](https://ctan.org/pkg/scratch3) LaTeX package
- The teaching approach draws on the Creative Computing Curriculum (Brennan, Balch & Chung), Brennan & Resnick (2012), PRIMM (Sentance et al., 2019) and the Raspberry Pi Foundation's Scratch-to-Python guidance. Full references are in the *For grown-ups* chapter.

This is an independent workbook. It is not made by or connected with Scratch, the Scratch Foundation, MIT or Google. Scratch is a project of the Scratch Foundation.
