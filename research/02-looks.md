# 02 – Looks blocks (purple) to Python

## Summary

Scratch's Looks blocks change **how a sprite or the stage looks**: speech bubbles, costumes, backdrops, size, graphic effects, visibility and layers. Python turtle covers about half of them directly:

- **Direct matches:** show/hide (`showturtle()` / `hideturtle()`), set size (`shapesize()`), switch costume (`shape()`), switch backdrop colour (`bgcolor()`), costume name reporter (`shape()` with no argument), visibility check (`isvisible()`).
- **Close with a small pattern:** say/think (use `print()` or `write()` on a hidden "speech turtle"), say for secs (`write` + `time.sleep` + `clear`), next costume / next backdrop (a list plus `% len(list)`), costume number (keep your own counter), colour effect (hue shift with `colorsys`), go to front (reorder the `turtles()` list in ColabTurtlePlus).
- **Real gaps:** no speech bubble shape, no ghost (transparency) on the turtle, no fisheye/whirl/pixelate/mosaic, no picture costumes or picture backdrops in ColabTurtlePlus (polygons only), no layer blocks in desktop turtle.

Key facts checked in the ColabTurtlePlus 2.2.0 source (downloaded from PyPI and run headless with a stub `display`): valid shapes are `turtle, ring, classic, arrow, square, triangle, circle, turtle2, blank` plus any `register_shape()` polygon; `shapesize(0)` raises `ValueError`; `write()` has `align` and `font=(name, size, 'normal'|'bold'|'italic'|'underline')` and draws in the turtle's **pen colour**; `turtles()` returns the live list that sets drawing order; `register_shape` docstring says "This version does NOT include shapes that are images"; there is no `bgpic`.

Key facts checked in scratch-vm (`scratch3_looks.js`, `rendered-target.js`): bubble text is cut to 330 characters and non-whole numbers are shown to 2 decimals; `say ""` removes the bubble; a newer bubble is not cleared by an older "for secs" timer; costume index wraps around; size is clamped between about 5 pixels and 1.5 times the stage; ghost is clamped 0 to 100, brightness -100 to 100; effects are cleared on green flag and stop; the size reporter is rounded.

## Block-by-block mapping table

Colour of every block: Looks purple, `#9966FF` (the shade used by Scratch 3.0). Below, `t` is the sprite turtle from `t = Turtle()`.

| Scratch block | What it really does (edge cases) | ColabTurtlePlus (Colab) | Desktop `turtle` | Gap |
|---|---|---|---|---|
| `say [Hello!]` | Shows a speech bubble that stays until another say/think or `say []`. Max 330 characters. Numbers like 3.14159 show as `3.14`. Bubble hides when sprite hides. | Simplest: `print("Hello!")`. On the canvas: speech turtle `s` (hidden, pen up) then `s.goto(t.xcor(), t.ycor()+30)`, `s.clear()`, `s.write("Hello!", align="center", font=("Arial", 16, "normal"))` | Same as Colab | No bubble outline; text does not follow the sprite when it moves |
| `say [Hello!] for (2) seconds` | Shows bubble, waits, then removes it. Script waits too. | `s.write("Hello!", align="center")`, `time.sleep(2)`, `s.clear()` | Same | `clear()` wipes everything that turtle drew, so use a separate speech turtle |
| `think [Hmm...]` | Like say, but a cloud bubble | `print("(thinks) Hmm...")` or `s.write("Hmm...", font=("Arial", 14, "italic"))` | Same | No cloud shape; italic is a nice stand-in |
| `think [Hmm...] for (2) seconds` | Like say for secs | `write` + `time.sleep(2)` + `clear()` | Same | As above |
| `switch costume to [costume2]` | By name, or by number (1-based); numbers wrap around; also accepts `next costume` / `previous costume` | `t.shape("turtle")` (built-in) or `register_shape("star", ((0,10),(3,3),...))` then `t.shape("star")` | `t.shape(...)`; picture costumes: `screen.register_shape("cat.gif")` then `t.shape("cat.gif")` | Colab: polygons only, no images. Desktop: GIF only, image costumes do not rotate or resize |
| `next costume` | Next in the list; after the last one it goes back to the first | `costumes = ["turtle","circle","square"]`, `n = (n + 1) % len(costumes)`, `t.shape(costumes[n])` | Same | You build the costume list yourself |
| `switch backdrop to [backdrop1]` | Changes the stage picture; starts `when backdrop switches to` scripts; accepts `next/previous/random backdrop` (random never picks the current one) | `bgcolor("lightblue")` (also `bgcolor(r, g, b)` with 0-255) | `bgcolor(...)` or `screen.bgpic("forest.gif")` (`"nopic"` removes it) | Colab: colour only, no pictures. No backdrop event (just call your own function) |
| `switch backdrop to [ ] and wait` | Stage only: also waits for the scripts it started to finish | Call your function directly; Python already waits | Same | Not needed: Python runs one step at a time |
| `next backdrop` | Wraps around | `backdrops = ["white","lightblue","black"]`, `b = (b + 1) % len(backdrops)`, `bgcolor(backdrops[b])` | Same | — |
| `change size by (10)` | Adds to size %; clamped (smallest about 5 px, largest 1.5 times the stage) | `size = size + 10`, `t.shapesize(size / 100)` | Same | `shapesize(0)` is an error; Scratch would clamp. Desktop GIF costumes ignore shapesize |
| `set size to (100) %` | Sets size; 100 % = normal | `t.shapesize(1)` (150 % = `t.shapesize(1.5)`) | Same | 100 % in Scratch = costume's own size; in turtle it is the default 20-pixel arrow |
| `change [color] effect by (25)` | Shifts hue; 200 = full circle back to start | Keep `hue` number; `colorsys.hsv_to_rgb(...)`; `t.color(r, g, b)` (see recipe below) | Same, but call `colormode(255)` first | Only recolours the shape; multi-colour costumes do not exist |
| `set [ghost] effect to (50)` | 0 = solid, 100 = invisible but still touchable | No turtle opacity. Fake it: blend the colour toward the background (recipe below). `fillopacity()` exists but only for `begin_fill` shapes | No transparency | Real gap |
| `brightness` effect | -100 black ... 100 white | Mix colour with black or white | Same | Approximate only |
| `fisheye`, `whirl`, `pixelate`, `mosaic` | Image distortions | None | None | Real gap; say "turtle can't do this" |
| `clear graphic effects` | Sets all effects to 0. Green flag and stop also do this | Reset your own variables and `t.color("black")` | Same | — |
| `show` | Makes sprite visible | `t.showturtle()` (alias `t.st()`) | Same | — |
| `hide` | Hidden sprites cannot be touched and their bubbles go away | `t.hideturtle()` (alias `t.ht()`) | Same | Hidden turtle still "exists" for distance checks |
| `go to [front] layer` | Sprite drawn on top of other sprites (sprites only) | `lst = turtles()`, `lst.remove(t)`, `lst.append(t)` (last in list is drawn on top; tested) | No simple way | Colab trick touches library internals; lines and text are always under turtles |
| `go to [back] layer` | Drawn behind other sprites | `lst.remove(t)`, `lst.insert(0, t)` | No simple way | As above |
| `go [forward] (1) layers` / `[backward]` | Moves n places in the order | `i = lst.index(t)`, `lst.insert(i + 1, lst.pop(i))` | No simple way | Rarely needed for beginners |
| `(costume [number])` | 1-based number, or `(costume [name])` | Number: `n + 1` from your own counter. Name: `t.shape()` | Same | Python lists count from 0: `n + 1` is the Scratch number |
| `(backdrop [number])` / `[name]` | Global reporter | `b + 1` and `backdrops[b]`; `bgcolor()` with no argument returns the colour | Same; `screen.bgpic()` returns picture name | — |
| `(size)` | Rounded size % | Keep `size` variable; or `round(t.shapesize()[0] * 100)` | Same | `shapesize()` returns a 3-tuple `(wid, len, outline)` |
| (checkbox) show reporter on stage | Monitor shows value live | `print(size)` or write it on screen with a turtle | Same | No live monitors |

### Tested recipes (ran in Python 3.13 with ColabTurtlePlus 2.2.0)

```python
import colorsys, time

# colour effect: Scratch uses 200 units for a full trip round the colour wheel
def color_effect(base_rgb, effect):
    h, s, v = colorsys.rgb_to_hsv(*[c / 255 for c in base_rgb])
    h = (h + effect / 200) % 1
    return tuple(round(c * 255) for c in colorsys.hsv_to_rgb(h, s, v))

color_effect((255, 0, 0), 200)   # (255, 0, 0): back to red, like Scratch
color_effect((255, 0, 0), 66)    # (5, 255, 0): green
t.color(color_effect((255, 0, 0), 66))

# fake ghost: mix the colour with the background colour
def fake_ghost(rgb, bg, ghost):
    g = max(0, min(100, ghost)) / 100          # clamp 0..100 like Scratch
    return tuple(round(c * (1 - g) + b * g) for c, b in zip(rgb, bg))

fake_ghost((255, 0, 0), (255, 255, 255), 50)   # (255, 128, 128): pale red

# say for 2 seconds with a speech turtle
s = Turtle(); s.hideturtle(); s.penup()
s.goto(t.xcor(), t.ycor() + 30)
s.write("Hello!", align="center", font=("Arial", 16, "normal"))
time.sleep(2)
s.clear()
```

## Gaps and gotchas

1. **`write()` is permanent ink, not a bubble.** Text stays until that turtle's `clear()`, and `clear()` also rubs out that turtle's lines. Always say with a separate hidden speech turtle. Text is in the speech turtle's pen colour, so `s.color("black")`.
2. **Text does not follow the sprite.** After the sprite moves, clear and rewrite the text.
3. **Counting from 0.** Python lists start at 0, Scratch costumes at 1. `costume number = n + 1`. The `% len(list)` trick gives Scratch's wrap-around.
4. **Size is a fraction, not a percent.** `set size to 150 %` is `t.shapesize(1.5)`. `shapesize(0)` crashes (Scratch would quietly clamp to a tiny size). Negative numbers are not clamped either (untested how they draw), so keep `size` at 5 or more yourself.
5. **No picture costumes in Colab.** ColabTurtlePlus `register_shape` takes polygon points only, and there is no `bgpic`. Desktop turtle takes GIF files (`register_shape("cat.gif")`, `bgpic("forest.gif")`), but image costumes do not turn with the heading and ignore `shapesize`.
6. **No ghost, fisheye, whirl, pixelate, mosaic.** Only the colour, and roughly brightness and ghost, can be faked by changing the colour.
7. **Effects do not reset by themselves.** Scratch clears effects on green flag. In Colab start each cell with `clearscreen()` and set colours again.
8. **Numbers look different.** Scratch shows `7`, Python `print(7.0)` shows `7.0`; Scratch rounds 3.14159 to `3.14` in a bubble, Python prints all digits. Use `round(x, 2)` or `int(x)`.
9. **Layers.** ColabTurtlePlus draws turtles in the order of `turtles()` (last = on top) and draws all turtles above lines, dots and text. The reorder trick works but is not an official function. Desktop turtle has no layer command.
10. **"and wait" and backdrop events.** Python has no events for "when backdrop switches to"; call a function instead. Because Python runs line by line, "and wait" is automatic.
11. **Animation speed.** With `t.speed(0)` ColabTurtlePlus skips screen updates, so shape and colour changes may only appear at the end of the cell; keep speed above 0 when the child wants to see costume changes.
12. **Colour names.** ColabTurtlePlus accepts its 140 named colours (`getcolor(n)` picks one by number 0 to 139) or `(r, g, b)` with 0 to 255. Desktop turtle needs `colormode(255)` for 0-255 numbers.

## Teaching ideas for a 9-year-old

**Analogy: the costume wardrobe.** A Scratch sprite has a wardrobe of costumes it can change into. In Python you build the wardrobe yourself: a list `["turtle", "circle", "square"]` is the rail of clothes, and `n` is the hanger you are pointing at. `next costume` is "move to the next hanger, and when you reach the end, go back to the start" (that is what `% len(costumes)` does). The speech turtle is a friend who holds up a sign; to change the sign, he wipes his whiteboard (`clear()`) and writes again.

**Mini-challenge 1: Costume parade (next costume).** Make the turtle change costume 8 times, half a second apart, and print the costume number each time. Stretch: ask `input("How many changes? ")`.

```python
from ColabTurtlePlus.Turtle import *
import time
clearscreen(); setup(480, 360)
t = Turtle()
costumes = ["turtle", "circle", "square", "triangle"]
n = 0
for i in range(8):
    n = (n + 1) % len(costumes)
    t.shape(costumes[n])
    print("costume", n + 1, costumes[n])
    time.sleep(0.5)
```

**Mini-challenge 2: Talking turtle (say for secs).** The turtle says "Hi!" for 2 seconds, then "What's your name?". Use `input()` for the answer, then say "Nice to meet you, NAME!". Stretch: think "Hmm..." in italics before answering.

**Mini-challenge 3: Grow and rainbow (size and colour effect).** In a loop of 10, `change size by 20` (`size += 20; t.shapesize(size / 100)`) and `change color effect by 20` using `color_effect`. After 10 steps the colour has gone all the way round the wheel (10 x 20 = 200). Question to ask: "Why is it red again at the end?" Stretch: make it shrink back with `-20`, and switch the backdrop colour each step.

## Sources (URLs)

- Scratch VM Looks blocks source: https://github.com/scratchfoundation/scratch-vm/blob/develop/src/blocks/scratch3_looks.js
- Scratch VM rendered target (size limits, effects list, layers, costume wrap): https://github.com/scratchfoundation/scratch-vm/blob/develop/src/sprites/rendered-target.js
- Scratch Wiki, Graphic Effects: https://en.scratch-wiki.info/wiki/Graphic_Effects
- Scratch Wiki, Looks Blocks: https://en.scratch-wiki.info/wiki/Looks_Blocks
- Scratch Wiki block pages (Say, Think, Switch Costume To, Next Costume, Set Size To, Go to Front/Back Layer): https://en.scratch-wiki.info/wiki/Say_()_(block) and linked pages
- ColabTurtlePlus on PyPI (version 2.2.0 source inspected): https://pypi.org/project/ColabTurtlePlus/
- ColabTurtlePlus GitHub and docs: https://github.com/mathriddle/ColabTurtlePlus , https://larryriddle.agnesscott.org/ColabTurtlePlus/documentation2.html
- Python turtle docs (shape, shapesize, register_shape, bgpic, write, showturtle): https://docs.python.org/3/library/turtle.html
