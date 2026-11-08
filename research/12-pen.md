# 12. Pen extension: Scratch to Python turtle

## Summary

The Pen extension is the easiest bridge from Scratch to Python, because turtle graphics *is* a pen. Almost every Pen block has a one-line turtle equivalent, and the names are nearly the same (`pen down` becomes `pendown()`).

There are three real differences.

1. **Colour numbers.** Scratch describes colour as four numbers from 0 to 100: colour (hue), saturation, brightness and transparency. Python turtle uses colour names (`"red"`), hex codes (`"#ff0000"`) or RGB numbers. A five-line helper using `colorsys.hsv_to_rgb` turns Scratch's numbers into Python colours. It was tested with `python3` below.
2. **Python keeps no "current pen colour number".** In Scratch, `change pen color by 10` works because Scratch remembers the number. In Python the child keeps it in a variable (`hue = hue + 10`) and sets the colour again. This is a good first use of variables.
3. **Transparency is missing.** Neither ColabTurtlePlus nor desktop turtle has pen transparency. ColabTurtlePlus does have *fill* opacity (`fillopacity()`, `begin_fill(opacity=...)`).

Python also adds something Scratch's Pen does not have: **filled shapes** with `begin_fill()` and `end_fill()`.

Setup used throughout (Colab):

```python
from ColabTurtlePlus.Turtle import *
clearscreen()
setup(480, 360)      # same size as the Scratch stage
t = Turtle()
```

On desktop, use `import turtle`, `t = turtle.Turtle()`, and `turtle.done()` at the end.

## Block-by-block mapping table

| Scratch block | ColabTurtlePlus (Colab) | Desktop `turtle` | Notes |
|---|---|---|---|
| `erase all` | `t.clear()` (one turtle), or `clearscreen()` (everything, and deletes all turtles) | `t.clear()` / `turtle.clearscreen()` | `clear()` removes drawings and leaves the turtle where it is, which matches `erase all`. `t.reset()` also sends the turtle home and resets its settings, so it is **not** the same. ColabTurtlePlus `clear()` also deletes stamps. Scratch's `erase all` does not reset pen colour or size; `clear()` does not reset them either. |
| `stamp` | `t.stamp()`, which returns an id | `t.stamp()`, which returns an id | Stamps the **turtle shape** (arrow, turtle, circle...), not a costume picture. `t.clearstamp(id)` and `t.clearstamps()` can remove stamps, which Scratch cannot do. In ColabTurtlePlus, `stamp(layer=1)` draws the stamp on top of filled shapes (the default `0` draws it underneath). |
| `pen down` | `t.pendown()` (also `pd()`, `down()`) | same | `t.isdown()` acts like a "pen is down?" question. |
| `pen up` | `t.penup()` (also `pu()`, `up()`) | same | Also use it for moving without drawing: `t.penup(); t.goto(x, y); t.pendown()`. Scratch's `go to x: y:` with the pen down draws a line, and turtle's `goto` does the same. |
| `set pen color to [colour picker]` | `t.pencolor("red")`, `t.pencolor("#ff8800")`, or `t.pencolor((255, 136, 0))` | `t.pencolor("red")`, `t.pencolor("#ff8800")`, or `t.pencolor((1.0, 0.53, 0))` | **Gotcha:** RGB tuples use 0 to 255 in ColabTurtlePlus (default `colormode(255)`), but **0 to 1** in desktop turtle (default `colormode(1.0)`, checked with `python3`). Call `colormode(255)` on desktop too (`turtle.colormode(255)`) so the same code works in both. Colour names and hex strings work the same in both. |
| `set pen (color) to (50)` | `t.pencolor(scratch_color(50))` | same, after `turtle.colormode(255)` | Uses the helper below. |
| `change pen (color) by (10)` | `hue = hue + 10` then `t.pencolor(scratch_color(hue))` | same | Python needs the variable `hue`, because turtle does not remember a hue number. |
| `set/change pen (saturation)` | `sat = ...` then `t.pencolor(scratch_color(hue, sat, bri))` | same | Scratch **clamps** saturation, brightness and transparency to 0 to 100. Its colour **wraps around**. |
| `set/change pen (brightness)` | `bri = ...` then `t.pencolor(scratch_color(hue, sat, bri))` | same | Brightness 0 is black. |
| `set/change pen (transparency)` | **Not available for the pen.** For fills: `t.fillopacity(0.5)` or `t.begin_fill(opacity=0.5)` (0 is invisible, 1 is solid) | **Not available** | Scratch transparency 0 to 100 matches opacity `1 - transparency/100`. The scratch-vm source uses that formula. |
| `change pen size by (1)` | `t.pensize(t.pensize() + 1)` | same | `pensize()` with no number *returns* the size. `width()` is another name for it. ColabTurtlePlus requires a positive size, so `pensize(0)` raises an error. Scratch clamps size to 1 to 1200. |
| `set pen size to (5)` | `t.pensize(5)` | same | Scratch's default size is 1, and turtle's is 1 too. |
| (no Scratch block) | `t.fillcolor("gold")`, `t.begin_fill()` ... `t.end_fill()` | same | A bonus. `t.color("red", "gold")` sets the pen and the fill colour at once. |
| (no Scratch block) | `bgcolor("black")` | `turtle.bgcolor("black")` | In Scratch you would paint a backdrop instead. |
| Turbo mode / no screen refresh | `t.speed(0)` or `t.animationOff()`, then `done()` | `t.speed(0)` or `turtle.tracer(0)` ... `turtle.update()` | In ColabTurtlePlus, speed 0 shows only the final picture, and you call `done()` to draw it. |

### The Scratch colour helper (tested)

Scratch's source (scratch-vm `scratch3_pen`) turns the pen state into HSV like this: hue = `color * 360 / 100`, saturation = `saturation / 100`, value = `brightness / 100`. The default pen colour is 66.66 (blue), with saturation 100, brightness 100 and transparency 0. Python's `colorsys` does the same maths:

```python
import colorsys

def scratch_color(color, saturation=100, brightness=100):
    """Turn Scratch pen numbers (0 to 100) into an (r, g, b) tuple, 0 to 255."""
    hue = (color % 100) / 100                     # colour wraps around like Scratch
    r, g, b = colorsys.hsv_to_rgb(hue, saturation / 100, brightness / 100)
    return (round(r * 255), round(g * 255), round(b * 255))
```

Output from `python3`:

| Scratch colour | RGB | Hex | Looks like |
|---|---|---|---|
| 0 | (255, 0, 0) | #ff0000 | red |
| 8 | (255, 122, 0) | #ff7a00 | orange |
| 16 | (255, 245, 0) | #fff500 | yellow |
| 33 | (5, 255, 0) | #05ff00 | green |
| 50 | (0, 255, 255) | #00ffff | cyan |
| 66.66 (Scratch default) | (0, 0, 255) | #0000ff | blue |
| 75 | (128, 0, 255) | #8000ff | purple |
| 100 | (255, 0, 0) | #ff0000 | red again |
| 120 | (204, 255, 0) | #ccff00 | wraps to 20 |
| -10 | (255, 0, 153) | #ff0099 | wraps to 90 |
| 0, saturation 50 | (255, 128, 128) | | pink (paler) |
| 0, brightness 50 | (128, 0, 0) | | dark red |

ColabTurtlePlus accepts this tuple directly, because its default `colormode` is 255. On desktop, call `turtle.colormode(255)` once at the top. Alternatively, turn the tuple into a hex string, `"#%02x%02x%02x" % rgb`, which works in both without changing `colormode`.

## Gaps and gotchas

1. **The colour scale is not degrees or 0 to 255.** Scratch hue runs from 0 to 100 and goes all the way round the rainbow. Children who have seen "0 to 360" or "0 to 255" elsewhere will mix them up. Keep the `scratch_color` helper as the bridge, then later show plain names and hex.
2. **Wrap versus clamp.** In Scratch, colour wraps (110 behaves like a value near 10), but saturation, brightness and transparency stop at 0 and 100. The helper wraps the colour with `% 100`. A child must clamp saturation and brightness themselves, for example `min(100, max(0, bri))`. Very small detail: scratch-vm's `wrapClamp(value, 0, 100)` wraps over 101 steps, so 101 maps to 0, not 1. This is invisible in practice.
3. **RGB ranges differ between targets.** ColabTurtlePlus uses 0 to 255 and desktop uses 0 to 1. A tuple like `(255, 0, 0)` gives an error on desktop unless `colormode(255)` is set. This is the most likely "it worked in Colab but not at home" bug.
4. **No pen transparency.** ColabTurtlePlus rejects `rgba(...)` colours and `"transparent"`. Only fills have opacity (`fillopacity`). Desktop turtle has neither.
5. **`stamp` stamps the turtle shape, not a costume.** ColabTurtlePlus cannot use images as shapes (its source says images are not supported). Use built-in shapes (`t.shape("turtle")`, `"circle"`, `"square"`, `"triangle"`, `"arrow"`, `"classic"`), or draw a custom polygon shape with `register_shape`. Setting `t.color(...)` and `t.shapesize(...)` before `stamp()` gives coloured, sized stamps.
6. **`clear` vs `reset` vs `clearscreen`.** `t.clear()` = erase all. `t.reset()` = erase all, then go home and reset colour and size. `clearscreen()` deletes the turtles too, so call `t = Turtle()` again after it. In ColabTurtlePlus, `reset` exists only as a turtle method, and the screen version is `resetscreen()`.
7. **Pen size 0 or negative.** Scratch quietly clamps it to 1, but ColabTurtlePlus raises "New width value must be positive". Guard against it: `t.pensize(max(1, size))`.
8. **Pen size and line ends.** Scratch draws thick lines with round ends. SVG turtle lines in Colab can look slightly different at corners. This is cosmetic only.
9. **Coordinates match.** `setup(480, 360)` gives the same stage size as Scratch, with (0, 0) in the centre and y going up in both libraries. That makes `goto(x, y)` code from Scratch carry straight over. (Direction differs: Scratch 90 means right, turtle 0 means right. See the motion report.)
10. **Speed.** Big pen projects (hundreds of lines) are slow in Colab with animation on. Use `t.speed(0)` with `done()`, or a speed of 10 to 13 so the child can still watch.

## Three classic Scratch pen projects in Python

Each project is written for ColabTurtlePlus. For desktop, swap the first three lines for `import turtle`, `turtle.colormode(255)` and `t = turtle.Turtle()`, and add `turtle.done()` at the end. All functions used were checked against the ColabTurtlePlus source: `pencolor` with a tuple, `pensize`, `stamp`, `begin_fill`/`end_fill`, `fillcolor`, `speed`, `bgcolor`, `hideturtle` and `shape`.

### 1. Square spiral

Scratch version: `pen down`, then `repeat 100` containing `move (step) steps`, `turn right 90` (or 91 for a twist), `change step by 2`, and `change pen color by 1`.

```python
from ColabTurtlePlus.Turtle import *
import colorsys
clearscreen()
setup(480, 360)
t = Turtle()

def scratch_color(color, saturation=100, brightness=100):
    hue = (color % 100) / 100
    r, g, b = colorsys.hsv_to_rgb(hue, saturation / 100, brightness / 100)
    return (round(r * 255), round(g * 255), round(b * 255))

bgcolor("black")
t.speed(13)
t.pensize(2)
step = 2
hue = 0
t.pendown()
for i in range(100):
    t.pencolor(scratch_color(hue))
    t.forward(step)
    t.right(91)          # try 90, 89, 121
    step = step + 2      # change step by 2
    hue = hue + 1        # change pen color by 1
t.hideturtle()
```

### 2. Rainbow flower (stamp and pen together)

Scratch version: `repeat 36` containing a petal (`repeat 2`: `repeat 18` of `move 5, turn 5`, then `turn 90`), followed by `turn right 10` and `change pen color by 3`. A `stamp` at the end puts the sprite in the middle.

```python
from ColabTurtlePlus.Turtle import *
import colorsys
clearscreen()
setup(480, 360)
t = Turtle()

def scratch_color(color, saturation=100, brightness=100):
    hue = (color % 100) / 100
    r, g, b = colorsys.hsv_to_rgb(hue, saturation / 100, brightness / 100)
    return (round(r * 255), round(g * 255), round(b * 255))

t.speed(0)            # draw instantly
t.pensize(2)
hue = 0
for petal in range(36):
    t.pencolor(scratch_color(hue))
    for side in range(2):        # one petal = two curved sides
        for k in range(18):
            t.forward(5)
            t.right(5)
        t.right(90)
    t.right(10)                  # 36 petals x 10 = 360
    hue = hue + 3                # change pen color by 3
t.shape("turtle")
t.color("gold")
t.stamp(layer=1)                 # stamp the turtle in the centre
done()                           # needed after speed(0) in ColabTurtlePlus
```

On desktop, delete `layer=1` (desktop `stamp()` takes no arguments) and replace `done()` with `turtle.done()`.

### 3. Polygon maker (ask and answer, plus a fill)

Scratch version: `ask [How many sides?] and wait`, `set sides to (answer)`, then `repeat (sides)`: `move 100`, `turn (360 / sides)`.

```python
from ColabTurtlePlus.Turtle import *
clearscreen()
setup(480, 360)
t = Turtle()

sides = int(input("How many sides? "))     # ask and wait
colour = input("What colour? (e.g. red, gold, #00aaff) ")

t.pensize(3)
t.color("black", colour)    # black outline, your colour inside
t.begin_fill()              # Scratch can't do this!
for i in range(sides):
    t.forward(100)
    t.left(360 / sides)
t.end_fill()
t.hideturtle()
```

Note: in Colab, run `input()` before the drawing starts. Placing it at the top as above works. ColabTurtlePlus also has a built-in `t.regularPolygon(...)`, but writing the loop teaches more.

## Teaching ideas for a 9-year-old

**Analogy: the turtle is a sprite holding a felt-tip pen.** `pendown()` presses the pen on the paper and `penup()` lifts it to move without a line. `pencolor` swaps the felt-tip and `pensize` picks a fatter one. `stamp()` is a rubber stamp shaped like the turtle. `clear()` is the eraser, and the turtle stays where it is. Scratch's colour number is a **rainbow ruler** from 0 to 100: 0 is red, about 16 is yellow, 33 is green, 50 is cyan, 66 is blue, 75 is purple, and at 100 the ruler starts again at red.

**Mini-challenges:**

1. **Rainbow ruler (5 minutes).** Draw 10 thick lines next to each other. Before each line, add 10 to `hue`. "Which number gives your favourite colour?" This makes the 0 to 100 scale concrete and practises `hue = hue + 10`.
2. **Stamp trail (10 minutes).** Use `t.shape("turtle")` and `t.penup()`, then loop 12 times: `forward(30)`, `right(30)`, change colour, `stamp()`. The result is a ring of rainbow turtles. Bonus: use `t.clearstamps(6)` to remove the first six. This is something Scratch cannot do.
3. **Spiral detective (10 minutes).** Run the square spiral with `right(90)`, then `right(91)`, `right(120)` and `right(144)`. Predict each picture first and then check. Extension: make each line 1 pixel thicker with `t.pensize(t.pensize() + 1)`, which is `change pen size by 1`.

**Order of introduction:** first `pendown`, `penup`, `forward` and `right` (identical to Scratch). Then colour names, then `pensize`. Next comes the `scratch_color` helper with a variable, then stamp, and last fill (the Python bonus). Save hex and RGB for later. The helper hides them at first.

## Sources

- Scratch Wiki, Pen Extension: https://en.scratch-wiki.info/wiki/Pen_Extension
- scratch-vm Pen extension source (default pen state, `_updatePenColor` HSV maths, wrap vs clamp, pen size range 1 to 1200, transparency to alpha): https://github.com/scratchfoundation/scratch-vm/blob/develop/src/extensions/scratch3_pen/index.js
- ColabTurtlePlus source (stamp/clearstamp(s), clear/reset/clearscreen, pencolor/colormode 255 default, pensize must be positive, begin_fill(rule, opacity), fillopacity, speed 0 and done, animationOff, no image shapes): https://github.com/mathriddle/ColabTurtlePlus/blob/main/ColabTurtlePlus/Turtle.py
- ColabTurtlePlus documentation: https://larryriddle.agnesscott.org/ColabTurtlePlus/documentation2.html
- Python `turtle` documentation (desktop): https://docs.python.org/3/library/turtle.html
- Python `colorsys` documentation: https://docs.python.org/3/library/colorsys.html
- Local test: `scratch_color` run with `python3 -I` on macOS (results in the table above). The desktop `turtle` default `colormode()` was checked and returned `1.0`.
