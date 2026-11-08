# 14. The Stage, Sprites and the coordinate system

Research dimension: how the Scratch 3.0 Stage (480 x 360, centre origin, direction 90 = right) maps onto ColabTurtlePlus in Google Colab, desktop `turtle`, and later Pygame Zero.

## Summary

> **Correction (7 Nov 2026, added when the 20 reports were combined):** the `mode("logo")` advice below does not hold for ColabTurtlePlus. In the library's `setheading()` (line 1641 of `Turtle.py` on GitHub main), the logo branch tests `self.screen.mode == "logo"`, but `screen.mode` is a method, so the test is always false. The code falls through to the svg branch, and `setheading(90)` points **down**. `forward`, `left` and `right` are unaffected. In Colab, stay in standard mode and use `t.setheading((90 - d) % 360)` for "point in direction". Desktop turtle's logo mode works. Found by `01-motion.md` and confirmed by reading the source; it was not run.


- **The stage itself maps very well.** Scratch's stage is 480 x 360 with (0, 0) in the centre, x from -240 to 240 and y from -180 to 180. ColabTurtlePlus `setup(480, 360)` in `"standard"` or `"logo"` mode gives exactly the same coordinates: centre origin, y going up. `goto(x, y)` matches "go to x: () y: ()" one for one. Checked in the source of `Turtle.py`.
- **Use `mode("logo")` so directions match Scratch.** In logo mode, heading 0 = up, 90 = right, 180 = down, and positive turns go clockwise, just like Scratch. The source confirms it: `setheading(90)` stores SVG angle 270 + 90 = 360, which points right. The one difference is that `heading()` gives back 0 to 359, so Scratch's -90 comes back as 270. In the default `"standard"` mode, 0 = east and angles go anticlockwise, so you would have to convert with `turtle_heading = (90 - scratch_dir) % 360`. Tested with `python3` for every whole number from -720 to 720.
- **Order matters.** `mode()` resets the screen and `setup()` moves turtles back to the centre. Use this starter cell:

```python
from ColabTurtlePlus.Turtle import *
clearscreen()          # first line of any cell you re-run
setup(480, 360)        # the Scratch stage
mode("logo")           # 0 = up, 90 = right, clockwise, like Scratch
bgcolor("white")       # stands in for a plain backdrop
showborder()           # draws the stage edge
cat = Turtle()         # one "sprite"
cat.shape("turtle")
cat.setheading(90)     # Scratch sprites start pointing 90 (right)
```

- **Sprites map to `Turtle()` objects, but with fewer features.** Each `Turtle()` is a sprite with its own position, heading and pen. `clone()` exists. ColabTurtlePlus has **no image costumes** (its docs say it does not include shapes that are images). It has **no `bgpic`** for backdrops, **no layer commands**, **no edge fencing or "if on edge, bounce"**, and **no events** (`onclick`, `onkey`, `ontimer` are not in the source). Costumes become built-in shapes (`turtle`, `classic`, `arrow`, `circle`, `square`, `triangle`, `ring`, `turtle2`, `blank`) or your own polygons via `register_shape`/`addshape`. A backdrop becomes `bgcolor()` plus drawing.
- **The Stage is not a sprite in Python.** In Scratch, the Stage holds backdrops, global ("for all sprites") variables and its own scripts, but it cannot move. In Python, the "Stage" is just the screen (`bgcolor`, `setup`, `clearscreen`), its scripts are the main program, and its variables are ordinary top-level (global) variables.
- **Timing differs.** Scratch aims for 30 frames per second and redraws at the end of each loop pass. ColabTurtlePlus animates each move according to `speed()` (0 to 13; 0 = no animation, then call `done()`). It has no frame clock. Pygame Zero later brings back a frame loop (`update()`/`draw()`, about 60 per second) that feels much more like Scratch.

## Mapping table

| Scratch 3.0 | ColabTurtlePlus (Colab) | Desktop `turtle` | Pygame Zero (later) |
|---|---|---|---|
| Stage 480 x 360, origin at centre | `setup(480, 360)` (integers only; default is 800 x 600) | `Screen().setup(480, 360)`; also `screensize(480, 360)` for the canvas | `WIDTH = 480`, `HEIGHT = 360`; origin **top-left**, y goes **down** |
| x: -240 to 240, y: -180 to 180 | Same in `"standard"` and `"logo"` modes | Same | `px = x + 240`, `py = 180 - y` |
| go to x: () y: () | `t.goto(x, y)`; `t.jumpto(x, y)` (alias `teleport`) moves with no line and no animation | `t.goto(x, y)` / `t.teleport(x, y)` (Python 3.12+) | `actor.pos = (x + 240, 180 - y)` |
| set x to / set y to | `t.setx(x)`, `t.sety(y)` | same | `actor.x = ...`, `actor.y = ...` (screen coordinates) |
| x position / y position | `t.xcor()`, `t.ycor()` | same | `actor.x - 240`, `180 - actor.y` |
| direction 90 = right, 0 = up, clockwise | `mode("logo")` gives the same convention | `mode("logo")` also exists | `actor.angle`: 0 = right, **anticlockwise**, so `angle = 90 - dir` |
| point in direction (d) | logo: `t.setheading(d)`; standard: `t.setheading((90 - d) % 360)` | same | `actor.angle = 90 - d` |
| direction (reporter, -179 to 180) | logo: `t.heading()` returns 0 to 359; to get Scratch's value use `h - 360 if h > 180 else h` | same | `wrap(90 - actor.angle)` |
| turn right / turn left (n) degrees | `t.right(n)` / `t.left(n)` (works the same in every mode) | same | `actor.angle -= n` / `+= n` |
| move (n) steps | `t.forward(n)` | same | `dx = n*sin(dir)`, `dy = -n*cos(dir)` in screen coordinates |
| point towards (x, y) | `t.setheading(t.towards(x, y))` (mode-aware) | same | `actor.angle = actor.angle_to(target)` |
| sprite | `t = Turtle()` | `t = turtle.Turtle()` | `cat = Actor("cat")` |
| sprite list (one or more) | `turtles()` returns the list; Python list `[cat, dog]` | `screen.turtles()` | Python list of Actors |
| create clone of myself | `t.clone()` | `t.clone()` | `Actor(...)` added to a list |
| costume / next costume | `t.shape("turtle")`, `register_shape("star", [(0,10), ...])` (no images) | `screen.addshape("cat.gif")`, `t.shape("cat.gif")` (GIF only, does not rotate) | `actor.image = "cat_b"` (PNG in `images/`) |
| backdrop | `bgcolor("skyblue")`; draw scenery with a hidden turtle | `screen.bgpic("room.gif")`, `bgcolor` | `screen.blit("room", (0, 0))` or `screen.fill(...)` in `draw()` |
| show / hide | `t.showturtle()` / `t.hideturtle()` | same | only draw the actor when `visible` is true |
| go to front / back layer | none; whatever is drawn last is on top | none (the newest drawing is on top) | draw order in `draw()` (the last one drawn is in front) |
| if on edge, bounce | none built in: check `abs(t.xcor()) > 240` yourself | same | check `actor.left < 0` and so on yourself |
| sprite fencing (stays on stage) | none: turtles can leave the window | none | none |
| stage edge visible | `showborder("gray")` / `hideborder()` | none (the window frame) | none |
| erase all (pen) | `clearscreen()` / `t.clear()` | `t.clear()`, `screen.clear()` | `screen.clear()` |
| stamp | `t.stamp()`, `t.clearstamps()` | same | `screen.blit(...)` |
| Stage scripts | the main program/cell | the main program | top-level code plus `update()`/`draw()` |
| "for all sprites" variable (lives on the Stage) | top-level variable; use `global` inside functions | same | same |
| "for this sprite only" variable | attribute such as `cat.lives = 3` | same | `cat.lives = 3` |
| 30 frames per second | no frame loop; `speed(0)` + `done()` draws instantly | `screen.ontimer(fn, 33)`, `tracer(0)` + `update()` | `update()` runs about 60 times a second; `clock.schedule_interval(fn, 1/30)` |

## Gaps and gotchas

1. **Heading reporter range.** In logo mode, `heading()` returns 270 where Scratch says -90. Directions themselves are fine; only the reported numbers differ. Teach the "if bigger than 180, take away 360" rule, or wrap it in a helper `direction(t)`.
2. **Standard mode is a trap.** Without `mode("logo")`, `setheading(90)` points **up** and `setheading(0)` points **right**: the opposite of what a Scratch user expects. `right()` and `left()` still behave the same in both modes, so a program that only uses turns looks "fine" until `setheading` is used. Always use `mode("logo")` in the starter cell.
3. **`mode()` resets the screen.** Call it before drawing anything, and before making extra turtles. `setup()` puts every turtle back in the middle. `setup()` only accepts integers (`setup(480.0, 360)` raises `ValueError`).
4. **Re-running cells.** In Colab, put `clearscreen()` first in any cell that will be run again, or the old drawing stays. This is like the Scratch green flag when "erase all" is missing.
5. **No image costumes or backdrops in Colab.** `ColabTurtlePlus` draws SVG shapes only. `register_shape` takes polygon points, not image files. A Scratch "costume" becomes a turtle shape, a colour, or a polygon you design. Desktop `turtle` can use GIF images via `addshape`, but those GIFs do **not rotate** with the heading (like Scratch's "don't rotate" rotation style).
6. **No fencing.** Scratch keeps at least part of a sprite on the stage (the Wiki says large sprites keep at least 15 pixels visible). In turtle, `goto(1000, 0)` just disappears off-screen. Kids must write their own edge checks, which is also a good lesson.
7. **No layers.** Scratch has the Stage at layer 0, a pen layer above it, and sprites stacked in front. Turtle draws everything in time order, and turtles appear above lines. There is no "go to front".
8. **Rotation style.** Scratch has "all around", "left-right" and "don't rotate". Turtle shapes always rotate. `tiltangle()`/`settiltangle()` can fake "don't rotate" by tilting the shape against the heading.
9. **The Wiki's normalise formula.** The Scratch Wiki Direction page gives a formula for wrapping directions. As summarised for this research, `((180 - dir) mod 360) - 180`, it gives the wrong sign (90 becomes -90). The tested formula is `wrap(d) = d % 360, minus 360 if above 180` (see the test below). Check the page directly before quoting it.
10. **Pygame Zero flips y.** The origin moves to the top-left and y grows **downward**. `actor.angle` is anticlockwise with 0 = right. So the Scratch-to-Pygame Zero step needs two conversions: `px = x + 240`, `py = 180 - y`, and `angle = 90 - direction`. Plan a "translator" helper at that stage rather than asking a 9-year-old to remember it.
11. **Speed is not frames.** `speed(13)` is fast but still animated. Scratch's "forever" loop redraws about 30 times a second. To mimic smooth Scratch animation in Colab, use small steps with `speed(0)`/`done()` per frame, or accept turtle's built-in animation.

### Heading conversion test (run with `python3`)

```python
def wrap_scratch(d):            # Scratch keeps direction in (-180, 180]
    d = d % 360
    return d - 360 if d > 180 else d
def scratch_to_standard(d):     # turtle "standard": 0 = east, anticlockwise
    return (90 - d) % 360
def standard_to_scratch(h):
    return wrap_scratch(90 - h)
def scratch_to_logo(d):         # turtle "logo": 0 = north, clockwise
    return d % 360
```

Results: Scratch 0 becomes standard 90; 90 becomes 0; 180 becomes 270; -90 becomes 180; 45 stays 45; 30 becomes 60; 400 becomes 50 (and wraps back to 40). In logo mode the number is the same except that negatives become 0 to 359 (-90 becomes 270, -45 becomes 315). "Move 10 steps" gave the same dx and dy in Scratch maths (`dx = n*sin(d)`, `dy = n*cos(d)`) and standard turtle maths (`dx = n*cos(h)`, `dy = n*sin(h)`). Round trip checked for every whole number from -720 to 720: **all checks pass**. The ColabTurtlePlus logo internals (`setheading`: SVG angle = 270 + a; `heading()` = (SVG angle - 270) % 360) round-trip cleanly too.

## Teaching ideas for a 9-year-old

**Analogy: "The stage is a map with a treasure X in the middle."** (0, 0) is the X. x is "how many steps east or west", y is "how many steps north or south". Scratch and Python use the *same map*. The only thing Python changes is which way the compass points: you tell it `mode("logo")` to use the Scratch compass (0 = up, 90 = right). Without it, Python uses a "maths compass" where 0 points right. Later, Pygame Zero uses a "book map": you start reading at the top-left corner and go down the page, so y counts downward.

**Mini-challenge 1: Draw the Scratch stage.** Use `setup(480, 360)`, `mode("logo")` and `showborder()`. With a hidden turtle, draw the x-axis and y-axis and a light grid line every 60 pixels. Then `write()` the corner labels "(-240, 180)", "(240, 180)" and so on. Check: does `goto(240, 180)` land exactly on the top-right corner? (It should, like the Scratch "xy-grid" backdrop.)

**Mini-challenge 2: Compass game.** Predict, then test: `setheading(0)`, `setheading(90)`, `setheading(180)`, `setheading(-90)` and `forward(100)` each time. Print `heading()` after each one. Why does -90 print 270? Then switch to `mode("standard")` and run it again. Which way is "0" now? Write a helper `def point_in_direction(t, d): t.setheading(d)` that works like the Scratch block.

**Mini-challenge 3: Bounce off the edge (build your own "if on edge, bounce").** Move a turtle `forward(10)` in a loop of 200 steps. If `abs(xcor()) > 230`, set heading to `-heading()` (a left/right bounce in logo mode). If `abs(ycor()) > 170`, set heading to `180 - heading()` (an up/down bounce). This teaches why Scratch's block is handy and what it does secretly. Extra: make two turtles (two sprites) bounce at once using a list `[cat, dog]`.

Extra idea: a "costume change" can be `t.shape("turtle")`, then `t.shape("arrow")`, then `t.shape("circle")` in a loop, like "next costume".

## Sources

- Scratch Wiki, Coordinate System: https://en.scratch-wiki.info/wiki/Coordinate_System
- Scratch Wiki, Direction (value): https://en.scratch-wiki.info/wiki/Direction_(value)
- Scratch Wiki, Stage: https://en.scratch-wiki.info/wiki/Stage
- Scratch Wiki, Layer (value): https://en.scratch-wiki.info/wiki/Layer_(value)
- Scratch Wiki, Frame Rate (30 FPS target): https://en.scratch-wiki.info/wiki/Frame_Rate
- ColabTurtlePlus source (`setup`, `mode`, `setheading`, `heading`, `towards`, shapes, `showborder`; no `bgpic` or events): https://github.com/mathriddle/ColabTurtlePlus/blob/main/ColabTurtlePlus/Turtle.py
- ColabTurtlePlus documentation (no image shapes, `clearscreen`, `speed` 0 to 13, `jumpto`, `done`): https://larryriddle.agnesscott.org/ColabTurtlePlus/documentation2.html
- Python `turtle` docs (desktop: `mode("logo")`, `bgpic`, `addshape` GIFs, `teleport`): https://docs.python.org/3/library/turtle.html
- Pygame Zero built-ins (Actor positions, anchors, anticlockwise `angle`, `screen.blit`, `clock`): https://pygame-zero.readthedocs.io/en/stable/builtins.html
