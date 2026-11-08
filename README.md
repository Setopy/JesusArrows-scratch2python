# From Scratch to Python

A workbook for a 9-year-old who already knows [Scratch](https://scratch.mit.edu) and is moving to real Python in **Google Colab**. Every Scratch 3.0 block category is mapped side by side to runnable Python, with turtle graphics standing in for the Scratch stage.

**Download the book:** [`scratch-to-python-workbook.pdf`](scratch-to-python-workbook.pdf) (258 pages, 35 missions)
**Colab notebook to go with it:** [`My Python Adventures.ipynb`](My%20Python%20Adventures.ipynb) (open it in Colab with File, Upload notebook)

## What's inside

| Section | Covers |
|---|---|
| Front pages | Meet Colab, Scratch words and Python words, four new habits |
| Part 1: Motion and Pen | `forward`, `right`, `goto`, pen colour and size |
| Part 2: Loops | `repeat` to `for`, `forever` to `while True`, nested loops |
| Part 3: Variables and Lists | labelled boxes, `append`, counting from 0 |
| Part 4: Operators | maths, `random.randint`, joining text, Python's fussier rules |
| Part 5: Sensing and Decisions | `input()`, `if`/`elif`/`else`, timers, touching |
| Part 6: My Blocks | `def`, inputs, `return`, more sprites with `Turtle()` |
| Part 7: Looks, Sound and Events | costumes, `beep()` music, the game loop, key presses in Thonny |
| Big Projects | eight games, from Animate your name to a Chase game |
| The Bug Zoo | reading errors, 12 common bugs, bug-hunt exercises |
| Block Dictionary | 147 Scratch blocks and their Python, plus a cheat sheet |
| For grown-ups | how to run a session, a suggested pace, Colab tips |

## The Colab setup

The book uses the [ColabTurtlePlus](https://pypi.org/project/ColabTurtlePlus/) library (tested in Colab on 8 Nov 2026: Python 3.13, ColabTurtlePlus 2.2.0):

```python
!pip install ColabTurtlePlus

from ColabTurtlePlus.Turtle import *
clearscreen()
initializeTurtle((480, 360))   # the same stage as Scratch
forward(100)
```

Install `ColabTurtlePlus`, not the similarly named `ColabTurtle`, which has no `Turtle()`, a different stage and a different compass.

## Building the PDF

```bash
tectonic scratch-to-python-workbook.tex
```

`preamble.tex` holds the shared look; each part is a file in `chapters/` (style rules in `chapters/STYLE.md`).

- `chapters/_make_mission_chart.py` rebuilds the missions star chart.
- `chapters/_make_notebook.py` rebuilds the Colab notebook from the chapters.
- `chapters/NN-colab-tests.py` holds each chapter's drawing programs. `chapters/_colab/build_runner.py` packs them into single-line cells that run every program in Colab and print PASS or FAIL.

`research/` holds the 20 research notes the book was built from, with `research/00-curriculum-map.md` as the overview.

---

This is an independent workbook. It is not made by or connected with Scratch, the Scratch Foundation, MIT or Google. Scratch is a project of the Scratch Foundation.
