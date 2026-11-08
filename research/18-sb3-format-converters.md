# 18. The .sb3 format and automatic Scratch to Python translation

Research agent 18 of 20. Researched 7 November 2026.

## Summary

- An `.sb3` file is an ordinary zip. Inside is one `project.json` and one file per costume (`.svg` or `.png`) and per sound (`.wav` or `.mp3`). Each asset file is named by the MD5 hash of its contents. You can open the zip with Python's standard `zipfile` module. Scratch's own editor exports it with **File > Save to your computer**. MIT offers no "export as Python" option.
- The code lives in `project.json` as a **flat dictionary of blocks**, not a tree. Each block has an `opcode` (such as `motion_movesteps`) plus `next` and `parent` links. Its `inputs` hold numbers and nested reporters, and its `fields` hold dropdown choices. A script starts at a block with `topLevel: true`, which is usually a hat block such as `event_whenflagclicked`. You get the script back by following `next`, and the loop body by following `SUBSTACK`.
- **No existing tool gives a child clean, plain Python.** The two Scratch-to-Python converters both depend on their own runtime library:
  - sb3topy (BSD-3) compiles the whole project to Pygame and keeps every Scratch behaviour.
  - PyStage (MIT, "pre alpha", last pushed August 2024) writes `sprite.move(10)` style code against its own engine.
  - Leopard (MIT, active in 2026) gives the most readable output, but it is JavaScript.
- A plain translator for the pen and motion subset is easy to write. The proof of concept below is about 330 lines, uses only the standard library, and turns a child's "green flag, repeat 4, move 100, turn 90" project into five lines of ordinary `turtle` code. Scratch's stage and Python's turtle share the same coordinates (origin at the centre, y pointing up), so the drawings come out the same.
- **Verdict:** a parent can use it to show "here is YOUR Scratch project as Python". This works well for drawing, loop, variable, ask and My Block projects. It does not work for games built on costumes, sprites touching each other, clones or sound. For those, show the child the structure (a loop is a `for`, a My Block is a `def`) and do not try to run the result.

## project.json anatomy

Top level: `targets` (the Stage first, then the sprites), `monitors` (variable displays on the stage), `extensions` (such as `"pen"` or `"music"`) and `meta` (`semver` is always `"3.0.0"`).

Each **target** (the Stage or a sprite) has:

| Key | Meaning |
|---|---|
| `isStage`, `name` | The stage is always named `"Stage"` |
| `variables` | `{id: [name, value]}`. A third element `true` marks a cloud variable. Stage variables are "for all sprites". |
| `lists`, `broadcasts` | `{id: [name, [items]]}` and `{id: name}` |
| `blocks` | `{blockId: block}`: **all the code, flat** |
| `costumes`, `sounds` | `assetId` (MD5), `md5ext` (the file name inside the zip), `dataFormat`, plus `rotationCenterX/Y` for costumes |
| `x`, `y`, `direction`, `size`, `visible`, `rotationStyle` | Sprite state. `direction` 90 means pointing right. |

Each **block** has:

```json
"rep": {
  "opcode": "control_repeat",
  "next": null,              // block below this one
  "parent": "flag",          // block above (or the C-block around it)
  "inputs": {
    "TIMES":    [1, [6, "4"]],   // [shadowState, value]
    "SUBSTACK": [2, "mv"]        // first block inside the C
  },
  "fields": {},              // dropdowns: {"VARIABLE": ["score", "varId"]}
  "shadow": false,
  "topLevel": false          // true only for the first block of a script (has x, y)
}
```

Input arrays work like this:

- **First element:** `1` means the slot holds only its default shadow value. `2` means a block with no shadow (C-block bodies and boolean slots). `3` means a reporter dropped over a shadow, and the hidden shadow comes third: `[3, "answerBlockId", [10, ""]]`.
- **Second element:** either a block ID or a compact primitive. Primitive codes: `4` number, `5` positive number, `6` positive integer, `7` integer, `8` angle, `9` colour `"#ff0000"`, `10` text, `11` broadcast `[11, name, id]`, `12` variable `[12, name, id]`, `13` list.
- **Numbers are stored as text** (`"100"`), so a translator has to convert them back.

My Blocks:

- `procedures_definition` holds a `procedures_prototype` shadow.
- The prototype's `mutation` carries `proccode` (`"draw polygon %s"`), `argumentids`, `argumentnames` and `warp` ("run without screen refresh").
- Inside the definition, parameters are `argument_reporter_string_number` blocks.
- `procedures_call` blocks match a definition by the same `proccode`.

## Opcode to Python mapping (30 most common blocks)

Translations target Python's `turtle` module (or ColabTurtlePlus in Colab, which uses the same function names), `print`, `input` and `time.sleep`.

| # | Scratch block | opcode | Python |
|---|---|---|---|
| 1 | when green flag clicked | `event_whenflagclicked` | top of the program (or `def when_flag_clicked():` and a call) |
| 2 | when [space] key pressed | `event_whenkeypressed` | `def when_space_key_pressed(): ...` then `onkey(f, 'space'); listen()` |
| 3 | when I receive [msg] | `event_whenbroadcastreceived` | `def when_i_receive_msg():` |
| 4 | broadcast [msg] | `event_broadcast` | `when_i_receive_msg()` (a function call) |
| 5 | move (10) steps | `motion_movesteps` | `forward(10)` |
| 6 | turn ↻ (15) degrees | `motion_turnright` | `right(15)` |
| 7 | turn ↺ (15) degrees | `motion_turnleft` | `left(15)` |
| 8 | go to x: () y: () | `motion_gotoxy` | `goto(x, y)` |
| 9 | point in direction (90) | `motion_pointindirection` | `setheading(90 - d)` (Scratch 0 = up, turtle 0 = right) |
| 10 | change x by (10) | `motion_changexby` | `setx(xcor() + 10)` |
| 11 | set x to () | `motion_setx` | `setx(x)` |
| 12 | x position | `motion_xposition` | `xcor()` |
| 13 | say [Hello!] | `looks_say` | `print('Hello!')` |
| 14 | say [] for (2) seconds | `looks_sayforsecs` | `print(...)` then `sleep(2)` |
| 15 | show / hide | `looks_show` / `looks_hide` | `showturtle()` / `hideturtle()` |
| 16 | pen down / pen up | `pen_penDown` / `pen_penUp` | `pendown()` / `penup()` |
| 17 | erase all | `pen_clear` | `clear()` |
| 18 | set pen size to () | `pen_setPenSizeTo` | `pensize(n)` |
| 19 | set pen color to [■] | `pen_setPenColorToColor` | `pencolor('#ff0000')` |
| 20 | wait (1) seconds | `control_wait` | `sleep(1)` (`from time import sleep`) |
| 21 | repeat (10) | `control_repeat` | `for count in range(10):` |
| 22 | forever | `control_forever` | `while True:` |
| 23 | if <> then | `control_if` | `if condition:` |
| 24 | if <> then / else | `control_if_else` | `if ...:` / `else:` |
| 25 | repeat until <> | `control_repeat_until` | `while not (condition):` |
| 26 | set [score] to (0) | `data_setvariableto` | `score = 0` (plus `global score` inside a function) |
| 27 | change [score] by (1) | `data_changevariableby` | `score = score + 1` |
| 28 | ask [] and wait / answer | `sensing_askandwait` / `sensing_answer` | `answer = input('...')` / `answer` |
| 29 | ( ) + ( ), −, ×, /, mod; < > = ; and/or/not; join; pick random | `operator_add` … `operator_random` | `a + b`, `a % b`, `a < b`, `a == b`, `and`, `not`, `'Hi ' + str(x)`, `randint(1, 10)` |
| 30 | define / call My Block | `procedures_definition` / `procedures_call` | `def draw_polygon(sides):` / `draw_polygon(6)` |

Translations that need care: `control_stop`, which becomes `return` or `sys.exit()`, and lists (`data_addtolist`, which becomes `my_list.append(x)`; `data_itemoflist`, which becomes `my_list[i - 1]` because Scratch lists start at 1).

## Existing tools compared

| Tool | What it does | Output | Licence | Maintenance (GitHub push date) | Readable for a 9-year-old? |
|---|---|---|---|---|---|
| **sb3topy** (BirdLogics/sb3topy; fork autonabee/sb3topy) | Compiles the whole `.sb3` (code, costumes, sounds) into one Python file that runs on its own engine with Pygame. Has a GUI. | Python + Pygame + sb3topy runtime | BSD-3-Clause | Last pushed Oct 2024; "Beta"; no releases; 80 stars | **No.** Aims for faithful behaviour, not teaching. Needs cairosvg. Its README warns that bugs "may allow arbitrary Python code to run". |
| **PyStage** (pystage/pystage) | Converts an `.sb3` with `python -m pystage.convert.sb3 file.sb3 -l en`, or online at convert.pystage.org. English and German block names. | Python against the PyStage API: `sprite.move(10)`, `sprite.turn_left(90)`, `when_program_starts(f)` | MIT | Last pushed Aug 2024; "pre alpha"; 153 stars | **Fairly.** Method names mirror the blocks, and the project's stated goal is learning Python "by Scratch". But it needs the PyStage engine (Pygame), so it does not run in Colab. |
| **Leopard + sb-edit** (leopard-js) | Drop an `.sb3` at leopardjs.com (now leopardjs.vercel.app), then "Edit as JavaScript". `sb-edit` is the converter library (sb3 in and out, Leopard out, scratchblocks export in progress). | JavaScript classes: `this.move(10)`, `yield* this.wait(1)` | MIT | Active, last pushed Jan 2026 | Good model of readable output, but the wrong language. `yield*` generators confuse beginners. |
| **sb3** (apple502j, PyPI) | Reads `.sb3` / `.sprite3` into Python objects | Data only, no code generation | GPL-3.0 | Stale (2020, v0.1, no docs) | n/a |
| **sbeditor** (PyPI), **py-pmp-manip** (PyPI) | Read and write `.sb3` as Python objects (py-pmp-manip also handles PenguinMod and needs Node for some features) | Data only | see PyPI | Work in progress | n/a (for adults building tools) |
| **scratch-parser** (scratchfoundation) | Official validator and unpacker used by the Scratch editor | JavaScript, schema validation | AGPL-3.0 | Active (Nov 2026) | n/a (useful as the authoritative schema) |
| **scratch-vm** (scratchfoundation) | Official runtime that defines every opcode | JavaScript | AGPL-3.0 | **Archived June 2026**, moved to the `scratch-editor` monorepo (`@scratch/scratch-vm` on npm) | n/a (the reference for what each opcode does) |
| Older prototypes ("sb-to-py", "S.To.P" on PyPI, forum projects) | Partial converters | Various | various | Abandoned or unclear | Not recommended |

Bottom line: for teaching, the useful idea is PyStage's (Python names that match the blocks), but with plain `turtle` underneath so it runs in Colab. That is what the proof of concept below does. I ran none of the third-party code.

## Proof of concept and its output

Folder: `research/18-sb3-tools/`

- `scratch2turtle.py`: the converter. Standard library only. Reads `project.json` or `.sb3`. `--colab` writes a ColabTurtlePlus header instead of `from turtle import *`.
- `square.json`: a hand-written minimal project (green flag, repeat 4, move 100, turn 90) built from the documented schema. `square.sb3` is the same JSON zipped by me, to show that the `.sb3` path works.
- `spiral.json`: ask/answer, if/else, join, variables, pen, a key-press script and a loose block.
- `myblock.json`: a My Block with a parameter, a broadcast, and a divide reporter.
- `out_*.py`: the generated Python.

Run: `python3 scratch2turtle.py square.json`

```python
from turtle import *

# ---- Sprite: Sprite1 ----
# when green flag clicked
for count in range(4):
    forward(100)
    right(90)
```

`spiral.json` produces:

```python
from turtle import *
from time import sleep

# Scratch variables
side = 0   # variable for all sprites

# ---- Sprite: Pencil ----
def when_flag_clicked_1():
    global answer, side
    answer = input('What is your name?')
    if answer == 'Ada':
        print('Hello, programmer!')
        sleep(2)
    else:
        print('Hi ' + str(answer))
    pendown()
    side = 5
    for count in range(20):
        forward(side)
        left(90)
        side = side + 5
    penup()

def when_space_key_pressed():
    goto(0, 0)
    clear()

onkey(when_space_key_pressed, 'space')
listen()
when_flag_clicked_1()   # the green flag
# (skipped 1 loose block(s) with no hat: motion_movesteps)
```

`myblock.json` produces:

```python
# My Block: define draw polygon (sides)
def draw_polygon(sides):
    for count in range(sides):
        forward(50)
        right(360 / sides)

def when_flag_clicked_1():
    when_i_receive_draw()   # broadcast

def when_i_receive_draw():
    draw_polygon(6)
    draw_polygon(3)

when_flag_clicked_1()   # the green flag
```

**Verification:** I ran each generated program against a stand-in `turtle` module that records every call (no window).

- The square makes 8 calls (4 × forward 100, right 90) and returns to (0, 0) facing its start heading.
- The spiral makes 43 calls; with the answer "Ada" it prints "Hello, programmer!".
- The polygons make 18 calls (a hexagon, then a triangle) and return to (0, 0).

How it works:

1. Find `topLevel` hat blocks and sort them by their `x`, `y` position on the canvas.
2. Walk each `next` chain, and recurse into `SUBSTACK` and `SUBSTACK2` for C-blocks.
3. Fill a template per opcode from a lookup table, resolving inputs recursively: a primitive array becomes a literal, and a block ID becomes a reporter expression.
4. If there is exactly one green-flag script and nothing else, write it flat with no `def`, like a child's first Python program.

Unknown blocks become `# TODO` comments rather than being dropped.

### Limits (what a parent should know)

1. **Sprites, costumes and the stage do not translate.** Turtle has one arrow or turtle shape. `switch costume`, `touching`, clones, layers, backdrops and sound have no plain-turtle equivalent. They come out as `# TODO`. Projects that are mainly games need Pygame, PyStage or sb3topy.
2. **Scratch runs scripts at the same time; Python runs one line after another.** Two green-flag scripts, `forever` loops alongside key handlers, or `broadcast and wait` become calls in sequence. A `while True:` with no screen update freezes Colab. This is the biggest conceptual gap, and a good thing to *talk about* rather than hide.
3. **Scratch is forgiving about types; Python is not.**
   - `answer` from `input()` is text, so `answer + 1` fails where Scratch would add.
   - `repeat (4.5)` works in Scratch, but `range(4.5)` is an error.
   - Scratch `=` ignores capitals (`"ada" = "Ada"` is true); Python's `==` does not.
   - Scratch lists start at 1, Python lists at 0.
   - Dividing by zero gives Infinity in Scratch and an error in Python.
4. **Each sprite in Scratch has its own position; turtle has one turtle.** For several sprites you would make `cat = Turtle()` and `dog = Turtle()` and prefix every call. The proof of concept does not do this yet.
5. **Keyboard events (`onkey`) work in desktop Python's turtle, but probably not in ColabTurtlePlus** (it draws into an SVG in the notebook). Check before relying on them in Colab.
6. **Timing.** Scratch draws at 30 frames per second, so a `repeat` animates. Turtle's speed is set separately with `speed()`.
7. **Getting the file.** The child saves it with File > Save to your computer, then uploads it to Colab (Files panel) and runs the converter. Only use `.sb3` files you or your child made. Converted code is ordinary Python and could do anything, so do not run converted projects from strangers.

## Teaching ideas

- **"Your project, translated."** The child builds the square in Scratch and saves the `.sb3`. Run the converter in Colab and put the two side by side. Ask: "Which line is the repeat block? Where did the move block go?" Then have the child change `100` to `50` in Python and predict the result.
- **Unzip it together.** Rename `project.sb3` to `project.zip`, open it, and look at the costume files and `project.json`. It shows that a program is just text, and that Scratch blocks are stored as words like `motion_movesteps`.
- **Opcode detective.** Print the opcodes in the child's own project (`for b in blocks.values(): print(b["opcode"])`) and match them to the blocks. The name tells you the category (`motion_`, `looks_`, `control_`), which is a gentle introduction to how libraries name things.
- **Fix the TODO.** Give the child a converted project that contains a `# TODO` line and ask them to write that line of Python themselves. Use the mapping table above as their cheat sheet.
- **The "two scripts" puzzle.** Convert a project with two green-flag scripts. Run it and notice that they happen one after the other instead of together. This leads into "computers do one thing at a time unless we ask otherwise", which is an honest explanation of the difference.
- **Reverse direction.** Show a short Python turtle program and ask the child to build it in Scratch. This checks understanding without the converter doing the work.
- **Parent caution:** present the converter's output as "a translation", not as "the right way to write it". Hand-written Python (for example `for side in range(4):` with a good variable name) is often nicer, and improving the translation is itself a good exercise.

## Sources

- Scratch Wiki, Scratch File Format: https://en.scratch-wiki.info/wiki/Scratch_File_Format
- scratch-parser (official schema and validator): https://github.com/scratchfoundation/scratch-parser
- scratch-vm (archived June 2026; now in scratch-editor): https://github.com/scratchfoundation/scratch-vm and https://github.com/scratchfoundation/scratch-editor
- sb3topy: https://github.com/BirdLogics/sb3topy, https://github.com/autonabee/sb3topy, forum announcement https://scratch.mit.edu/discuss/topic/600562
- PyStage: https://github.com/pystage/pystage (web converter convert.pystage.org)
- Leopard: https://github.com/leopard-js/leopard, https://github.com/leopard-js/sb-edit, https://leopardjs.vercel.app/
- sb3 (PyPI): https://pypi.org/project/sb3/
- sbeditor (PyPI): https://pypi.org/project/sbeditor/
- py-pmp-manip (PyPI): https://pypi.org/project/py-pmp-manip/
- GitHub REST API repo metadata (licence, push dates, archived flag), queried 7 Nov 2026: https://api.github.com/repos/{owner}/{repo}
