# Scratch → Python: combined curriculum map

Combined on 7 Nov 2026 from 20 research reports (`01` to `20` in this folder). Written for the parent. The child-facing wording lives in the workbook.

Target: a 9-year-old who knows Scratch 3.0 and is learning Python in **Google Colab with ColabTurtlePlus 2.2.x**. Desktop **Thonny** is the second tool.

---

## 1. The ten rules that came up again and again

| # | Rule | Reports |
|---|---|---|
| 1 | **`input()` always gives text.** `"7" + "3"` is `"73"`. Use `int(answer)`. Typing a word into `int()` gives a ValueError. | 07, 08, 09, 16 |
| 2 | **Python cares about capitals; Scratch doesn't.** `"A" == "a"` is False. Use `.lower()`. Variable names are case-sensitive too. | 08, 09, 10 |
| 3 | **Counting starts at 0.** Scratch `item 1` / `letter 1` is `[0]` in Python. `lst[0-1]` quietly gives the *last* item, with no error. | 08, 10 |
| 4 | **Indentation is the C-block's mouth.** The colon opens it, the 4-space lines go inside, and the first line back at the margin is after the C. Indenting a line at the wrong level gives *no* error. | 05 |
| 5 | **One game loop, not many scripts.** Scratch only fakes running scripts at once. In Colab use `for frame in range(N):` that updates every sprite. Never `while True` (it freezes the cell); never `sleep` inside one sprite's update. | 05, 15 |
| 6 | **Colab can't do key presses, clicks or timers.** ColabTurtlePlus has no `onkey`, `onclick`, `ontimer` or `mainloop`. Key-press games become `input()` turns. Real key games move to Thonny. | 04, 07, 19, 20 |
| 7 | **Directions differ.** Scratch: 0 = up, clockwise. Turtle standard: 0 = right, anticlockwise. Use `setheading((90 - d) % 360)`. **Don't use `mode("logo")` in Colab** (bug, see §6). | 01, 14 |
| 8 | **`return` is the new superpower.** Scratch custom blocks can't report a value. No `return` gives `None`; `print` is not `return`. | 11 |
| 9 | **Errors are clues, not failures.** Scratch never shows an error, so the child has never seen one. Read the last line first, then the line number and the `^^^`. Python 3.10+ hints ("Did you mean 'score'?") help a lot. | 16 |
| 10 | **Drawing fast needs `done()`.** With `speed(0)` nothing shows until `done()` at the end. Colour names must be lowercase (`"red"`). | 11, 20 |

---

## 2. Teaching order

The pasted 8-module plan follows Scratch's block palette. The teaching research (17) recommends a **different order for Python**. Events and parallelism are cheap in Scratch but the *hardest* thing in text, and they need functions first. Loops should come early because drawing shapes needs `repeat` straight away.

Keep the module names, but **teach in this order**:

| Teach | Original module | What to cover | Project that ends it (20) | Main reports |
|---|---|---|---|---|
| 1 | M6 Motion and Looks (+ "say" from M1) | Run cell = green flag; `print`, `time.sleep`; `forward`, `right`, `goto`; pen, colour | Animate Your Name | 01, 02, 12, 14 |
| 2 | M5 Control, part A | `for i in range(n):`, indentation, nested loops; `while` with an end | Pen Flower | 05, 12 |
| 3 | M2 Variables and lists | `=`, `+=`, f-strings, names; lists, `.append`, 0-based | (feeds the quiz) | 09, 10 |
| 4 | M3 Operators | Maths, `random.randint`, comparisons, `and/or/not`, joining text | Quiz | 08 |
| 5 | M4 Sensing + M5 Control part B | `input()` + `int()`, `if/elif/else`, `while not`, `break`, timer | Guess the Number, Story with Choices | 05, 07 |
| 6 | M8 My Blocks | `def`, parameters, `return`, calling; a class as a cookie-cutter for clones | Virtual Pet | 06, 11 |
| 7 | M7 Sound and events | Game loop; broadcast = function call; sound in Colab; key presses in Thonny | Chase Game, Catch Game | 03, 04, 13, 15 |
| 8 | Remix / hackathon | A project of the child's own design, shown to the family | Own choice | 17, 18 |

**How each session runs** (17: PRIMM, Use-Modify-Create, Dann et al. 2012 "mediated transfer"):
1. Show the Scratch script and the Python **side by side** and draw a line from each block to its Python line.
2. Give working starter code: *predict → run → investigate → change one thing → make something new*.
3. End with "translate this Scratch script you haven't seen" and something working to show.

Research warning (Weintrop & Wilensky 2019): knowing Scratch does **not** help with text code by itself unless someone links the two out loud. The side-by-side step is the part that matters most.

---

## 3. Colab starter cell

```python
!pip install ColabTurtlePlus
from ColabTurtlePlus.Turtle import *
import colorsys, math, random, time

clearscreen()
setup(480, 360)          # same stage as Scratch: x -240..240, y -180..180
t = Turtle()
t.penup()                # Scratch sprites don't draw unless the pen is down

def point_in_direction(t, d):          # Scratch direction -> turtle (standard mode)
    t.setheading((90 - d) % 360)

def scratch_color(c, sat=100, bright=100):   # Scratch pen colour 0-100 -> hex
    r, g, b = colorsys.hsv_to_rgb((c % 100) / 100, sat / 100, bright / 100)
    return "#%02x%02x%02x" % (round(r * 255), round(g * 255), round(b * 255))

def scratch_round(x):                  # Scratch rounds 2.5 up to 3; Python's round() gives 2
    return math.floor(x + 0.5)
```

I checked the three helpers in `python3` (they don't need turtle). `scratch_color(0)` gives red, `50` cyan and `66.66` blue, and values past 100 wrap round. `scratch_round(2.5)` gives 3 while `round(2.5)` gives 2. Directions 0, 90, 180 and -90 convert to 90, 0, 270 and 180. The cell as a whole has **not** been run in Colab.

---

## 4. Block-by-block highlights

The full tables are in each report. These are the points most likely to trip a child up.

- **Motion (01):** relative turns match; absolute directions need the helper. Turtle has no edge fence and no "if on edge, bounce", so write it as an `if`. "Glide" has no seconds; use a timed loop.
- **Looks (02):** no speech bubbles; use `print`, or a separate hidden "speech turtle" that `write()`s, because `clear()` also wipes that turtle's drawing. Costumes are polygon shapes only (no images, no `bgpic`). "Next costume" = a list + `n = (n + 1) % len(costumes)`. `shapesize(0)` crashes. Ghost, fisheye, whirl and pixelate aren't possible.
- **Sound (03):** Colab plays sound with `IPython.display.Audio(..., autoplay=True)`. Colab can't tell when a sound ends, so "play until done" = play, then `time.sleep(length)`. Use `normalize=False` or the volume setting does nothing. Pitch: 10 Scratch units = 1 semitone.
- **Events (04):** broadcast = calling a function, and a plain call already waits like "broadcast and wait". On desktop use `screen.onkeypress` (**not** `onkey`, which fires when the key is let go) + `screen.listen()` + `mainloop()`. Pass `jump`, not `jump()`. Click handlers need `(x, y)`.
- **Control (05):** `repeat (2.5)` runs 3 times in Scratch, but `range(2.5)` is an error. "Repeat until" becomes `while not`. "Stop" becomes `break`, `return` or `sys.exit()` depending on the option. "Stop other scripts in sprite" has no Python equivalent.
- **Clones (06):** teach a small class, not `clone()`. ColabTurtlePlus `clone()` doesn't copy direction or the child's own variables. When deleting clones from a list, loop over a copy, `enemies[:]`.
- **Sensing (07):** "touching sprite" = `t.distance(other) < radius`; "x position of Sprite2" = `sprite2.xcor()`; timer = `time.perf_counter()`. Touching colour and loudness have no simple equivalent. Colab's clock is UTC.
- **Operators (08):** Python trig uses radians (`math.sin(math.radians(90))`). Dividing by zero is an error, where Scratch gives Infinity. `%` behaves like Scratch's `mod`, even for negatives.
- **Variables (09):** "For all sprites" = a top-level variable; "for this sprite only" = an attribute like `cat.health`. Changing a top-level variable inside a function needs `global`, or Python gives an UnboundLocalError.
- **Lists (10):** a missing item gives IndexError or ValueError, where Scratch returns blank or 0. Report 10 has helper functions that behave like Scratch, if a softer start helps.
- **My Blocks (11):** calling a function before its `def` cell has run gives NameError. Use `speed(0)` + `done()` for "run without screen refresh"; there's no `tracer` in ColabTurtlePlus.
- **Pen (12):** pen is turtle's home ground. Fill (`begin_fill`/`end_fill`) is a bonus Scratch lacks. No pen transparency in either library. Desktop turtle needs `colormode(255)` for RGB 0–255.
- **Extensions (13):** Music is the best fit for Colab (5/5), about 15 lines with numpy. Video sensing, face sensing and all hardware extensions are impossible in Colab. If there's a micro:bit, its Python editor matches every Scratch micro:bit block.
- **Stage (14):** `setup(480, 360)` matches the Scratch stage one-to-one. See the logo-mode correction in §6.

---

## 5. Where to write Python (19)

| Use | Tool | Why |
|---|---|---|
| Teach 1 to 6 (drawing, loops, data, quizzes, functions) | **Colab + ColabTurtlePlus** | Already set up; strong for drawing and text games |
| Teach 7 (key presses, real games) | **Thonny** (free, offline, no account) | Plain `turtle` has real `onkeypress`/`ontimer`. Pygame Zero later has sprite-like `Actor`, `update()` and `on_key_down` |
| iPad / no install | micro:bit Python editor (simulator) | Browser-based fallback |

- **Not options any more:** Trinket.io shut down on 31 Aug 2026 (report 19 cites trinket's own shutdown notice). The Mu editor was archived on 31 Aug 2025. I didn't check either myself.
- **Test before teaching:** a reported Thonny issue (#3158) breaks Pygame Zero mode on newer Python.

**Show the child their own project as Python (18):** `18-sb3-tools/scratch2turtle.py` turns a simple Scratch *drawing* project's `project.json` into plain turtle code. It can't handle costumes, clones, touching, sound or scripts running at the same time. It was tested only on three hand-written sample projects. No existing tool gives a child readable plain Python.

---

## 6. Corrections and open checks

**Correction made:**
- **`mode("logo")` is broken in ColabTurtlePlus.** Report 14 recommended it, and I've added a correction note to that file. In `Turtle.py` line 1641, `setheading` tests `self.screen.mode == "logo"`. But `screen.mode` is a method (defined at line 840), so the test is always false and `setheading(90)` points down. Only `setheading` is affected.
- Evidence: I read the current GitHub source myself. Running the library here was blocked, so the bug is confirmed by reading only. `forward`, `left` and `right` still work in logo mode.
- **Fix:** use standard mode + `point_in_direction` in Colab. Desktop turtle's logo mode is fine.
- The converter (18) already writes standard-mode `setheading(90 - d)`, so it is unaffected.

**Not yet verified:**
- Nothing in any report was run inside Colab itself. Turtle code was checked against the library source or a stand-in (reports 02 and 20 built stand-ins from the real source).
- `t.shapesize()` in ColabTurtlePlus is unconfirmed (12).
- Error messages were captured on Python 3.13.5. Colab runs 3.12, so the wording should match but hasn't been checked (16).
- Some sources were cited without being opened: Scratch Wiki "Global Variable" (09), "Frame Rate" and "Broadcast" (15). Block colour hex codes came from memory (03, 04).
- Teaching research (17): four papers were read in full; the rest came from abstracts. The session-length and parent-role advice is the agent's own judgement, marked *(judgement)* in that file.
- Thonny + Pygame Zero on this family's computer (19).

---

## 7. Index of reports

01 Motion · 02 Looks · 03 Sound · 04 Events · 05 Control · 06 Clones → classes · 07 Sensing · 08 Operators · 09 Variables · 10 Lists · 11 My Blocks → functions · 12 Pen · 13 Extensions · 14 Stage and coordinates · 15 Scripts at once → game loop · 16 Errors ("Bug Zoo") · 17 Teaching research · 18 .sb3 format and converter · 19 Where to write Python · 20 Eight projects and capstone path
