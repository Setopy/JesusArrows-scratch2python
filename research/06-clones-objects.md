# 06 Clones → objects and classes

## Summary

In Scratch, a clone is a live copy of a sprite. It shares the sprite's scripts, costumes and sounds, and gets its own copy of the sprite's state. In Python, the same idea is an **object**: each `Turtle()` is already a separate "sprite", and a **class** is the blueprint that says what every copy has and can do.

Verified facts from Scratch 3.0 (scratch-vm source, `rendered-target.js` `makeClone` and `scratch3_control.js`):

- A new clone copies **x, y, direction, draggable, visible (shown or hidden), size, current costume, rotation style, graphic effects**, and **all "for this sprite only" variables and lists** (`duplicateVariables()`). After that, each clone's copy changes on its own.
- "For all sprites" (global) variables are not copied. There is only one, and every clone reads and writes the same value.
- A new clone is layered **directly behind** its parent (`goBehindOther`).
- The limit is **300 clones at once** for the whole project (`clonesAvailable()`). When the limit is reached, "create clone" silently does nothing and gives no error.
- The Stage cannot be cloned (`makeClone` returns null for the stage), but the Stage *can* run "create clone of [Sprite1]".
- `delete this clone` does nothing in the original sprite (`if (util.target.isOriginal) return;`). Clones are also removed by the green flag and the stop sign.
- Clones can make clones ("create clone of myself" inside a clone script). This is useful for recursion, and it is the quickest way to hit the 300 limit.

Python support (checked in the source code):

- **ColabTurtlePlus 2.2.0** supports many turtles at once (the object-oriented interface since v2.0). It provides `t.clone()`, `t.hideturtle()`/`ht()`, `t.showturtle()`/`st()`, `t.isvisible()`, `t.shape()`, a screen-level `turtles()` list, and `t.delete()`, which really removes a turtle from the drawing. Its `clone()` copies **position, shape and pen settings** (colour, pen size, pen up or down, shown or hidden). It **does not copy heading (direction)**, and it does **not** copy any extra attributes you added (such as `t.score`).
- **Desktop `turtle`** (Python 3.13 stdlib): `t.clone()` makes a `deepcopy`. It copies position, **heading**, shape, pen, and **also any extra attributes** such as `t.score` or `t.speed_y`, which is the closest match to Scratch's "for this sprite only" variables. It has no `delete()`. Use `t.hideturtle()`, then remove the turtle from your own list.

The recommended teaching order is: (a) a list of `Turtle()` objects → (b) a `make_clone()` function → (c) a small `class` with `__init__` and a method → (d) `list.remove()` as "delete this clone".

## Block-by-block mapping table

| Scratch block / idea | Python (ColabTurtlePlus, `from ColabTurtlePlus.Turtle import *`) | Notes |
|---|---|---|
| A sprite | `t = Turtle()` | Each `Turtle()` is its own sprite with its own position and pen. |
| `create clone of [myself]` | `c = t.clone()` | Colab copies position, shape and pen, but not heading, so add `c.setheading(t.heading())`. Desktop copies the heading too. |
| `create clone of [myself]` (step a, no clone()) | `c = Turtle(); c.goto(t.pos()); c.setheading(t.heading())` | Shows the kid exactly what "copy" means. |
| `create clone of [Enemy]` from another sprite | `enemies.append(make_enemy())` or `enemies.append(Enemy(x, y))` | In Python, any code can make an object. There is no "only the sprite itself" rule. |
| `when I start as a clone` | Code at the end of `make_clone()`, or the class's `__init__` | `__init__` runs once, the moment each object is born, just like the clone hat. |
| Scripts every clone runs (e.g. `forever: change y by -5`) | A method, `def move(self): ...`, called in a loop: `for e in enemies: e.move()` | Scratch runs all clones "at the same time". Python takes turns in a `for` loop. |
| `delete this clone` | `enemies.remove(e)` (plus `e.delete()` in Colab or `e.hideturtle()` on desktop) | Removing from the list is the "delete". Hiding or deleting removes the picture. |
| Delete all clones (green flag / stop) | `for e in enemies: e.delete()` then `enemies = []` (Colab); `clearscreen()` also resets | |
| 300-clone limit | `if len(enemies) < 300: enemies.append(...)` | Python has no limit, but a kid-made cap teaches the idea (and stops Colab slowing down). |
| "For this sprite only" variable | An attribute: `self.speed`, `self.lives` | Each object has its own value. It is copied at birth in Scratch and in desktop `clone()`, but **not** in Colab `clone()`. |
| "For all sprites" variable | An ordinary variable outside the class, e.g. `score = 0` | Shared by everyone, as in Scratch. Changing it inside a function needs `global score`. |
| `(clone id)` trick (local variable set at birth) | `self.id = n` passed to `__init__` | Python objects can simply be numbered. |
| `hide` / `show` | `t.hideturtle()` / `t.showturtle()` | Same names in Colab and desktop. |
| Costume (copied to clone) | `t.shape("turtle")`; copied by `clone()` in both libraries | |
| `go to front layer` (clone sits behind parent) | No real layers | Later turtles are usually drawn on top. Don't promise layering. |
| `when this sprite clicked` (each clone) | Desktop: `t.onclick(func)`; Colab: no mouse events | Colab gap. Keep clone games keyboard-free or turn-based in Colab. |

## Gaps and gotchas

1. **The Colab `clone()` loses direction.** In the ColabTurtlePlus `clone()` source, a new `Turtle()` copies `position`, `shape` and `pen()`, but never `heading`. A kid who turns the parent and then clones will see the clone facing the default way. Fix: `c.setheading(t.heading())`.
2. **The Colab `clone()` does not copy your own variables.** `t.lives = 3; c = t.clone(); c.lives` raises `AttributeError` in Colab, but works on desktop (deepcopy). Teach the class route (`Enemy(...)`) for anything with variables, and keep `clone()` for "same look, same place".
3. **`clone()` returns a plain `Turtle` in Colab, even when you clone a subclass.** On desktop, deepcopy keeps the class. Another reason to make copies with `Enemy(...)` rather than `.clone()`.
4. **Deleting while looping skips clones.** `for e in enemies: enemies.remove(e)` leaves half of them behind (tested: 4 in, 2 left). Loop over a copy (`for e in enemies[:]`) or rebuild the list: `enemies = [e for e in enemies if e.y > -180]`. Scratch has no equivalent bug, so this is genuinely new.
5. **Hiding is not deleting.** On desktop, `hideturtle()` leaves the turtle in `screen.turtles()`, and it still costs memory. Remove it from *your* list too. Colab's `t.delete()` does remove it from the screen's list.
6. **There is no parallelism.** Scratch clones each run their own `forever`. Python runs one loop that moves each object in turn. With `speed(0)`/`animationOff()` in Colab this looks smooth enough. With animation on, 20 turtles will crawl.
7. **ColabTurtlePlus redraws the whole SVG on every move**, so dozens of turtles get slow. Suggest a soft cap of about 20 to 30 objects in Colab, not 300.
8. **Global vs per-clone variables.** In Scratch, the "for all sprites / this sprite only" choice is made once in a dialog. In Python it is decided by *where* you write it (`self.x` vs `score`), and changing a global inside a function needs `global`. This is a likely confusion point.
9. **There is no `isOriginal`.** In Python, the "original" is just the first object. There's no special rule that it can't be deleted.
10. **Not tested here:** the ColabTurtlePlus graphics themselves need the Colab/IPython display. Its behaviour was read from the v2.2.0 source (`Turtle.py`: `clone`, `delete`, `hideturtle`, `turtles`). Desktop `clone()` was read from the CPython 3.13 source. Only the logic snippet below was executed.

### Tested logic snippet (no graphics, `python3 -I`)

```python
import random, copy
MAX_CLONES = 300
class Enemy:                             # the cookie cutter
    def __init__(self, x, y, speed):     # "when I start as a clone"
        self.x = x; self.y = y; self.speed = speed   # "for this sprite only"
    def move(self):
        self.y = self.y - self.speed
    def clone(self):                     # "create clone of myself"
        return copy.copy(self)

score = 0                                # "for all sprites"
enemies = []
for i in range(5):
    if len(enemies) < MAX_CLONES:
        enemies.append(Enemy(random.randint(-200, 200), 180, random.randint(10, 40)))
for step in range(10):
    for e in enemies[:]:                 # loop over a COPY
        e.move()
        if e.y < -180:
            enemies.remove(e)            # "delete this clone"
            score = score + 1
```

Results: the cap stopped at exactly 300 out of 1000 attempts; `b = a.clone(); b.x = 99` left `a.x == 0` (copies are independent); the buggy remove-while-looping left 2 of 4.

### Colab version (for the workbook; not executed here)

```python
from ColabTurtlePlus.Turtle import *
clearscreen(); setup(400, 400)
import random

class Raindrop:
    def __init__(self):
        self.t = Turtle()
        self.t.shape("circle"); self.t.color("blue"); self.t.penup()
        self.t.speed(0)
        self.t.goto(random.randint(-180, 180), 180)
        self.speed = random.randint(5, 20)
    def fall(self):
        self.t.goto(self.t.xcor(), self.t.ycor() - self.speed)

drops = [Raindrop() for i in range(8)]
for step in range(30):
    for d in drops[:]:
        d.fall()
        if d.t.ycor() < -180:
            d.t.delete()          # picture gone
            drops.remove(d)       # clone gone
```

(Uses "has-a turtle" rather than `class Raindrop(Turtle)`. This works the same in Colab and on desktop, and avoids the `clone()` subclass gotcha.)

## Teaching ideas for a 9-year-old

**Analogy: cookie cutter and cookies.** The class is the cookie cutter: it decides the shape and what every cookie has (chocolate chips = `self.speed`). Each `Enemy(...)` is a cookie. You can decorate one cookie (change its `x`) and the others don't change. Eating a cookie is `enemies.remove(cookie)`, which is "delete this clone". The cookie jar is the list. In Scratch, the jar can hold 300 cookies at most.

Also map the words: "clone" = "object", "when I start as a clone" = `__init__`, "this sprite only" = `self.`, "all sprites" = a normal variable.

**Steps:**
1. *Ten turtles:* `team = [Turtle() for i in range(10)]`, then turn each one by `i * 36` and move forward. This makes a starburst, which shows that every turtle is its own sprite.
2. *My first clone:* `c = t.clone()`, then try turning `t` before cloning and spot the bug (the direction isn't copied in Colab). Fix it with `setheading`.
3. *Write a `make_star(x, y)` function* that builds and returns a turtle. This is "when I start as a clone", written by hand.
4. *Upgrade to a class* with `__init__` and one method (`fall`, `wiggle`).

**Mini-challenges:**
1. **Rainstorm (clones + delete):** make 10 raindrops at random x positions. Each step they fall by their *own* speed, and a drop that reaches the bottom is deleted. Bonus: create a new drop each time one is deleted, but never more than 15.
2. **Clone counter (300 limit):** keep a list and make clones in a loop until `len(clones) == 300`, then print "Scratch would stop here!". Do it with plain numbers or dicts, not turtles, so Colab stays fast. Then ask: what happens if a clone makes a clone of itself each time (1, 2, 4, 8...)? How many rounds until 300?
3. **Lives per clone ("for this sprite only"):** three `Enemy` objects each start with `self.lives = 3`. A "hit" function picks a random enemy and takes 1 life. When `lives == 0`, remove it. Keep a shared `score` (for all sprites) of how many are gone. Print each enemy's lives after every hit to see that they're separate.

## Sources

- Scratch Wiki, Cloning: https://en.scratch-wiki.info/wiki/Cloning
- Scratch Wiki, Create Clone of () (block): https://en.scratch-wiki.info/wiki/Create_Clone_of_()_(block)
- Scratch Wiki, When I Start as a Clone (block): https://en.scratch-wiki.info/wiki/When_I_Start_as_a_Clone_(block)
- Scratch Wiki, Delete This Clone (block): https://en.scratch-wiki.info/wiki/Delete_This_Clone_(block)
- scratch-vm `makeClone` (what is copied, 300 limit, stage excluded): https://github.com/scratchfoundation/scratch-vm/blob/develop/src/sprites/rendered-target.js
- scratch-vm control blocks (`createClone` → `goBehindOther`, `deleteClone` original guard): https://github.com/scratchfoundation/scratch-vm/blob/develop/src/blocks/scratch3_control.js
- ColabTurtlePlus on PyPI (v2.2.0; multiple turtles, `clone()` example): https://pypi.org/project/ColabTurtlePlus/
- ColabTurtlePlus documentation: https://larryriddle.agnesscott.org/ColabTurtlePlus/documentation2.html
- Python `turtle` docs, `clone()`, `hideturtle()`, `turtles()`: https://docs.python.org/3/library/turtle.html
