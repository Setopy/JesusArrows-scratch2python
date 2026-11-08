# 01 Motion blocks: Scratch 3.0 to Python (ColabTurtlePlus first, desktop turtle second)

## Summary

The Motion category (blue, `#4C97FF`) has 18 blocks: 15 command blocks and 3 round reporters. Most of them map onto turtle methods one-to-one. A sprite is a turtle, `move` is `forward`, `turn` is `right`/`left`, and `go to x: y:` is `goto`. Four differences cause most of the confusion for a Scratch kid:

1. **Direction numbers are different.** In Scratch, 0 is up, 90 is right, and positive turns go clockwise. In turtle's default "standard" mode, 0 is right, 90 is up, and angles go counter-clockwise. `right(15)` and `left(15)` behave the same in both, because they are relative turns. Only absolute headings (`point in direction`, `direction` reporter, `point towards`) need converting: `turtle_heading = (90 - scratch_direction) % 360`.
2. **The pen is down by default.** A Scratch sprite never draws unless the Pen extension says `pen down`. A turtle draws a line on every move. Use `penup()` for "just moving", or ColabTurtlePlus's `jumpto(x, y)` / `teleport(x, y)`.
3. **No stage walls.** Scratch "fences" sprites so at least min(15 px, half the sprite) stays on stage, and it has `if on edge, bounce`. Turtles walk off the canvas and keep going. Bouncing has to be written as an `if` (this is a good lesson).
4. **No mouse, no seconds-based glide in ColabTurtlePlus.** `go to mouse-pointer` and `point towards mouse-pointer` have no Colab equivalent; use `input()` to ask for a target. `glide` becomes `goto` with `speed()` (the speed is approximate, not seconds), or a loop of small steps with `time.sleep`.

**ColabTurtlePlus warning (tested against the source, v2.2.0 on PyPI and current GitHub main):** `mode("logo")` would match Scratch's 0 = up and clockwise angles, but its `setheading()` has a bug. Line ~1527 tests `self.screen.mode == "logo"`, which compares a *method* to a string and is always False. So in logo mode `setheading(90)` points the turtle **down** (`heading()` then reports 180), not right. `towards()`, `heading()` and `goto()` are correct in logo mode; only `setheading/seth/face` is broken. **Recommendation:** in Colab, stay in standard mode and use a helper `point_in_direction(t, d)` that does `t.setheading((90 - d) % 360)`. Desktop `turtle.mode("logo")` works correctly, if you want Scratch-style numbers there.

Recommended start cell for the Motion lessons (Colab):

```python
!pip install ColabTurtlePlus
from ColabTurtlePlus.Turtle import *
clearscreen()
setup(480, 360)        # same size as the Scratch stage: x -240..240, y -180..180
t = Turtle()
t.shape("turtle")
t.penup()              # Scratch sprites don't draw; put the pen down only when you want lines
t.setheading(0)        # turtle 0 = Scratch 90 (pointing right), the same start as a new sprite

def point_in_direction(t, d):      # Scratch direction -> turtle heading
    t.setheading((90 - d) % 360)

def scratch_direction(t):          # turtle heading -> Scratch direction (-179..180)
    d = (90 - t.heading()) % 360
    return d - 360 if d > 180 else d
```

## Block-by-block mapping table

Scratch internals come from `scratch-vm/src/blocks/scratch3_motion.js` and `rendered-target.js`. `t` is a turtle from `t = Turtle()` (ColabTurtlePlus) or `t = turtle.Turtle()` (desktop). The same method names work in both unless the notes say otherwise.

| Scratch block | Python (ColabTurtlePlus; desktop the same unless noted) | Notes / exact Scratch behaviour |
|---|---|---|
| `move (10) steps` | `t.forward(10)` (`fd`) | 1 step = 1 pixel in both. Scratch computes `dx = steps*cos(90-dir)`, `dy = steps*sin(90-dir)`, the same maths as turtle. Negative steps move backward; turtle also has `t.back(10)`. Turtle draws a line unless `penup()`. Scratch then fences the sprite at the edge; turtle doesn't. |
| `turn ↻ (15) degrees` | `t.right(15)` (`rt`) | Identical in every mode, since it is relative. Scratch wraps direction into -179..180; turtle `heading()` gives 0..360. |
| `turn ↺ (15) degrees` | `t.left(15)` (`lt`) | Identical. |
| `go to (random position)` | `from random import randint` then `t.goto(randint(-240, 240), randint(-180, 180))` | Scratch uses `round(480*(random()-0.5))`, i.e. -240..240 by -180..180. Use `t.jumpto(...)` (ColabTurtlePlus) or `penup()` first to avoid a line. |
| `go to (mouse-pointer)` | No equivalent in Colab. Use `x = int(input("x? "))`, `y = int(input("y? "))`, `t.goto(x, y)`. | Desktop: `screen.onclick(t.goto)` moves the turtle where you click (event style, like "when stage clicked"). |
| `go to (Sprite2)` | `t.goto(t2.pos())` or `t.goto(t2.xcor(), t2.ycor())` | Scratch silently does nothing if the sprite doesn't exist; Python gives a NameError. |
| `go to x: (0) y: (0)` | `t.goto(0, 0)` (`setpos`, `setposition`); also `t.home()` for (0,0) | `home()` also resets the heading to turtle 0 = Scratch 90, so it matches a fresh Scratch sprite. ColabTurtlePlus `jumpto(x, y)` / `teleport(x, y)` moves without drawing even if the pen is down. |
| `glide (1) secs to (random position)` | `t.goto(randint(-240,240), randint(-180,180))` with `t.speed(3)` | Same as "go to" but animated. See the glide row below for real seconds. |
| `glide (1) secs to (mouse-pointer / Sprite2)` | `t.goto(t2.pos())` (sprite); mouse: none in Colab | |
| `glide (1) secs to x: (0) y: (0)` | Simple: `t.speed(2); t.goto(0, 0)`. Exact seconds: a loop (below). | Scratch interpolates linearly by elapsed time: `pos = start + (elapsed/duration)*(end-start)`, snapping to the end when time is up. 0 or negative seconds means jump instantly. `speed()` in ColabTurtlePlus is 0..13 (0 = no animation, 1 = slowest, 13 = fastest; `'slow'`=3, `'normal'`=5, `'fast'`=10). Desktop turtle speed is 0..10. Neither is in seconds. |
| `point in direction (90)` | `t.setheading((90 - 90) % 360)` or the helper `point_in_direction(t, 90)` | **Needs conversion** in standard mode: Scratch 90 (right) = turtle 0, Scratch 0 (up) = turtle 90, Scratch 180 (down) = turtle 270, Scratch -90 (left) = turtle 180. Desktop `turtle.mode("logo")` makes `setheading(90)` mean right, like Scratch. **Do not use `mode("logo")` with ColabTurtlePlus** (setheading bug, see Summary). Alias in ColabTurtlePlus: `seth`, `face`. |
| `point towards (mouse-pointer / Sprite2)` | `t.setheading(t.towards(t2.pos()))` | `towards()` returns an angle in the *current mode's* units, so no conversion is needed when you feed it straight back into `setheading` (standard mode). Scratch formula: `dir = 90 - atan2(dy, dx)`. `point towards (random direction)` gives `round(random()*360) - 180`; Python: `t.setheading(randint(0, 359))`. Mouse: none in Colab. |
| `change x by (10)` | `t.setx(t.xcor() + 10)` | No single "change x" method; this read-modify-write is a nice first look at `x = x + 10`. |
| `set x to (0)` | `t.setx(0)` | Keeps y. |
| `change y by (10)` | `t.sety(t.ycor() + 10)` | |
| `set y to (0)` | `t.sety(0)` | Keeps x. |
| `if on edge, bounce` | No built-in. Write an `if` (see Gaps). | Scratch: finds the nearest edge the sprite's *costume bounds* touch, flips the matching part of the direction (keeping at least 0.2 of it pointing away from the wall), then fences the sprite back on stage. |
| `set rotation style [left-right / don't rotate / all around]` | No equivalent. Closest: choose a symmetric shape (`t.shape("circle")`) for "don't rotate"; ColabTurtlePlus `tilt`/`settiltangle` change only how the shape is drawn. | Scratch only changes how the costume is *drawn*: "left-right" draws the costume facing 90 and flips it when direction < 0; "don't rotate" always draws it at 90. The real direction still changes, and moving still follows it. Turtle shapes always point where they're going. |
| `(x position)` reporter | `t.xcor()` (ColabTurtlePlus alias `getx()`) | Scratch rounds away float noise (`round` if within 1e-9), otherwise keeps decimals. Turtle may show `99.99999999999999`; use `round(t.xcor())` when printing. |
| `(y position)` reporter | `t.ycor()` (alias `gety()`); `t.pos()` gives both | |
| `(direction)` reporter | `scratch_direction(t)` helper, or `t.heading()` raw | Scratch reports -179..180 with 0 = up; turtle `heading()` reports 0..360 with 0 = right (standard). They match only when pointing at 45 degrees (both say 45). |

Exact-seconds glide (works in Colab and desktop):

```python
import time
def glide(t, secs, x, y, frames=20):
    sx, sy = t.xcor(), t.ycor()
    t.speed(0)                         # no built-in animation; we animate ourselves
    for i in range(1, frames + 1):
        t.goto(sx + (x - sx) * i / frames, sy + (y - sy) * i / frames)
        time.sleep(secs / frames)
```

(The interpolation maths was checked with `python3`. In Colab each frame is redrawn, so the real time is a little longer than `secs`.)

## Gaps and gotchas

- **Two direction systems.** This is the biggest source of bugs. A table on the wall helps (Scratch to turtle): up 0 to 90, right 90 to 0, down 180 to 270, left -90 to 180. Formula: `(90 - d) % 360` both ways (it's its own inverse, mod 360). Checked with `python3` for 90, 0, 180, -90 and 45.
- **ColabTurtlePlus `mode("logo")` setheading bug.** In v2.2.0, `setheading()` checks `self.screen.mode == "logo"` (missing underscore), so logo-mode `setheading(90)` points down. Stay in `"standard"`. Also, `mode()` calls `resetscreen()`, so it would have to come before `Turtle()`.
- **Pen down by default.** Scratch sprites don't leave trails. Start every motion lesson with `t.penup()` and treat `pendown()` as "the Pen extension".
- **No fencing, no edge.** `t.goto(1000, 0)` moves the turtle off the visible canvas, and later `xcor()` really is 1000. Scratch would have stopped it so about 15 px stays visible (scratch-render `FENCE_WIDTH = 15`, or half the sprite if it is smaller).
- **Bounce must be hand-written.** A simple version that works well for a turtle treated as a point, in Scratch-direction thinking:
  ```python
  # moving with t.forward(5) inside a loop, standard mode (turtle headings)
  if t.xcor() > 240 or t.xcor() < -240:
      t.setheading(180 - t.heading())   # mirror left/right
  if t.ycor() > 180 or t.ycor() < -180:
      t.setheading(-t.heading())        # mirror up/down
  ```
  In Scratch numbers the same rules are `dir = -dir` (side wall) and `dir = 180 - dir` (top/bottom); both were checked with `python3`. Scratch's real version also stops sprites getting "stuck" in the wall; a kid version should also clamp: `t.setx(max(-240, min(240, t.xcor())))`.
- **Direction wrap.** Scratch keeps direction in -179..180 (`turn 200` from 90 shows -70). Turtle `heading()` is 0..360. Both are fine for moving; they only look different when printed.
- **Glide is not in seconds.** `speed()` controls how fast the animation runs, not how long it takes. ColabTurtlePlus uses 0..13; desktop uses 0..10; 0 means instant in both (a common surprise: 0 is *fastest*, not slowest).
- **Mouse blocks don't exist in Colab.** ColabTurtlePlus has no onclick/onkey or mouse position. Replace with `input()` coordinates. Desktop turtle has `screen.onclick(fn)` but no "where is the mouse now" reporter.
- **Missing sprites.** Scratch quietly ignores `go to (deleted sprite)`; Python raises an error. That's a good moment to explain error messages.
- **Rotation style has no turtle equivalent.** Skip it, or use a round shape. Don't spend a lesson on it.
- **Float noise.** After `right(60)` and `forward` steps, positions like `49.99999999999999` appear. Scratch hides this (limitPrecision); in Python use `round()`.
- **Each sprite is one turtle object.** Two Scratch sprites = `t1 = Turtle()`, `t2 = Turtle()`. Their code runs one line at a time, not in parallel like Scratch scripts (see the concurrency research file).
- **Canvas size.** ColabTurtlePlus default window is 800x600; call `setup(480, 360)` before `Turtle()` to match the stage. `setup()` accepts integers only.

## Teaching ideas for a 9-year-old

**Analogy: the robot with a compass that reads it differently.** The sprite and the turtle are the same robot, but the Python robot's compass was printed by someone who thinks "0" means "towards the sunrise (right)" and counts anticlockwise. Scratch's compass says 0 is "towards the ceiling" and counts clockwise, like a clock. "Turn right 15" means the same to both robots, because it doesn't need the compass. Only "face direction 90" needs translating, so we write a small translator function `point_in_direction` once and use it everywhere.

**Mini-challenge 1: Square dance (move and turn).** Rebuild the Scratch script `repeat 4: move 100 steps, turn ↻ 90 degrees` in Python with `for i in range(4): t.forward(100); t.right(90)`. Then: a triangle (turn 120), a hexagon (turn 60), and the question "what number of turns and degrees makes a circle-ish shape?" (36 turns of 10). Pen down is allowed here, so they see the path.

**Mini-challenge 2: Treasure teleporter (go to x:y, random, input).** The turtle starts at (0,0). The computer hides a treasure at `randint(-240,240), randint(-180,180)` and puts a dot there (`dot(10, "gold")`). The kid types x and y with `input()`, the turtle `goto`s there, and Python prints the `distance()` to the treasure: "hot" if under 50, "cold" otherwise. This replaces the mouse with typing and practises coordinates.

**Mini-challenge 3: Bouncy ball (if on edge, bounce, by hand).** In Scratch: `forever: move 5 steps, if on edge, bounce`. In Python: `for i in range(300):`, `t.forward(5)`, then the two `if` lines from Gaps. Ask: "Scratch did the bounce for you. What does the computer have to check to know it hit a wall?" Extension: count the bounces in a variable and print it at the end.

## Sources

- Scratch VM motion block implementation: https://github.com/scratchfoundation/scratch-vm/blob/develop/src/blocks/scratch3_motion.js
- Scratch VM rendered target (direction wrap -179..180, rotation styles, fencing call): https://github.com/scratchfoundation/scratch-vm/blob/develop/src/sprites/rendered-target.js
- Scratch renderer fencing (`FENCE_WIDTH = 15`, `getFencedPositionOfDrawable`): https://github.com/scratchfoundation/scratch-render/blob/develop/src/RenderWebGL.js
- Scratch Wiki, Motion Blocks: https://en.scratch-wiki.info/wiki/Motion_Blocks
- Scratch Wiki, If on Edge, Bounce: https://en.scratch-wiki.info/wiki/If_on_Edge,_Bounce_(block)
- Scratch Wiki, Glide () Secs to X: () Y: (): https://en.scratch-wiki.info/wiki/Glide_()_Secs_to_X:_()_Y:_()_(block)
- ColabTurtlePlus source (read directly; setheading bug at `elif self.screen.mode == "logo":`): https://github.com/mathriddle/ColabTurtlePlus/blob/main/ColabTurtlePlus/Turtle.py
- ColabTurtlePlus on PyPI (v2.2.0 wheel downloaded and checked; same bug): https://pypi.org/project/ColabTurtlePlus/
- ColabTurtlePlus documentation: https://larryriddle.agnesscott.org/ColabTurtlePlus/documentation2.html
- Python turtle documentation (modes, setheading, towards, onclick, speed 0..10): https://docs.python.org/3/library/turtle.html
