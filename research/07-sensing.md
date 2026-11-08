# 07 Sensing blocks: Scratch 3.0 to Python

## Summary

Sensing blocks are light blue (cyan, `#5CB1D6` in the Scratch 3.0 palette). They are the program's "senses": what the sprite is touching, what the user typed, the keyboard and mouse, the clock, and other sprites' properties. They come in three shapes: stack blocks (`ask [] and wait`, `reset timer`, `set drag mode`), boolean hexagons (`touching?`, `key pressed?`, `mouse down?`) and round reporters (`answer`, `timer`, `mouse x`, and so on).

How each group maps to Python:

- **Easy and exact:** `ask and wait` + `answer` become `answer = input("question")`. `timer` becomes `time.perf_counter()`. `current [...]` becomes `datetime`. `days since 2000` is datetime arithmetic. `username` becomes `getpass.getuser()`. `[x position] of [Sprite2]` becomes `sprite2.xcor()`. `distance to [Sprite2]` becomes `t.distance(sprite2)`.
- **Possible with a pattern:** `touching [sprite]?` becomes `t.distance(other) < radius`, the "hitbox circle" idea.
- **Desktop turtle only (not ColabTurtlePlus):** key pressed, mouse down, mouse x/y and drag mode. These need events (`onkey`, `onscreenclick`, `ondrag`). In Colab, replace them with `input()` turns.
- **No simple equivalent:** `touching color?`, `color is touching color?` and `loudness`.

The biggest gotcha: **`input()` always returns text.** Scratch quietly turns "7" into the number 7. Python does not: `"7" + "3"` gives `"73"`. Use `int(answer)` or `float(answer)`.

All logic snippets below were run with `python3` (macOS, Python 3) on 7 Nov 2026. The turtle `distance`/`xcor` snippets were run with desktop `turtle`.

## Block-by-block mapping table

| Scratch block (exact text) | Shape | What it does in Scratch | Python (Colab / desktop) | Notes |
|---|---|---|---|---|
| `ask [What's your name?] and wait` | stack | Shows the question (in the sprite's speech bubble if it is visible, otherwise at the bottom of the stage) and pauses the script until the user presses Enter | `answer = input("What's your name? ")` | Works the same in Colab and desktop. `input()` also pauses. |
| `(answer)` | reporter | Holds the most recent reply. It is shared by all sprites and is cleared only when the green flag starts the project | the variable you saved, e.g. `answer` | In Python you name it yourself. You can keep many answers (`name`, `age`), which Scratch can't do without extra variables. |
| `<touching (mouse-pointer / edge / Sprite2) ?>` | boolean | Pixel-perfect check of whether the costumes overlap | `t.distance(other) < 20` (hitbox circle). Edge: `abs(t.xcor()) > 240 or abs(t.ycor()) > 180` (use your screen size) | Not pixel-perfect: it treats each sprite as a circle. Pick a radius about the sprite's size. |
| `<touching color [ ] ?>` | boolean | Checks whether any pixel of the sprite overlaps that colour on stage | **No simple equivalent** | Turtle can't read screen pixels. Instead, store where coloured things are, e.g. "the lava is the strip `y < -100`", and test coordinates. |
| `<color [ ] is touching [ ] ?>` | boolean | Checks whether a colour on the sprite touches a colour on stage | **No simple equivalent** | Same work-around: coordinates and distances. |
| `(distance to (mouse-pointer / Sprite2))` | reporter | Straight-line distance in steps from this sprite's centre | `t.distance(other)` or `t.distance(x, y)`. Without turtle: `math.dist((x1, y1), (x2, y2))` | Tested: (0,0) to (30,40) gives `50.0`. In Scratch, the distance to a missing sprite or the stage is 10000. |
| `<key (space) pressed?>` | boolean | True while that key is held down; it can be checked inside a loop | Colab: `input("Press Enter to jump, q to quit ")`. Desktop: `screen.onkeypress(jump, "space")` + `screen.listen()` | Python flips the idea: instead of "keep asking whether it is pressed", you say "when pressed, run this function", like the `when [space] key pressed` hat block. To get "is held?", set a flag with `onkeypress`/`onkeyrelease`. |
| `<mouse down?>` | boolean | True while the mouse button is held | Desktop: `screen.onscreenclick(func)` (fires once per click). Colab: none | There is no built-in "is held" check. Use a click event. |
| `(mouse x)` / `(mouse y)` | reporter | Mouse position in stage coordinates | Desktop: `def clicked(x, y): ...` with `screen.onscreenclick(clicked)`. You get x and y **only at the moment of a click** | Live tracking needs tkinter (`screen.cv.winfo_pointerx()`...), which is too advanced. Colab: ask for numbers with `input`. |
| `set drag mode [draggable / not draggable]` | stack | Lets the player drag the sprite in the full-screen/player view | Desktop: `t.ondrag(t.goto)` | Colab: none. |
| `(loudness)` | reporter | Microphone volume from 0 to 100 (-1 if there is no microphone) | **No simple equivalent** | It would need the `sounddevice` + `numpy` packages and microphone permission. Skip it for a 9-year-old. |
| `(timer)` | reporter | Seconds (with decimals) since the green flag or the last reset | `start = time.perf_counter()` once, then `timer = time.perf_counter() - start` | Python has no automatic timer. You make your own "stopwatch". `time.time()` also works; `perf_counter` is steadier for measuring. |
| `reset timer` | stack | Sets the timer back to 0 | `start = time.perf_counter()` again | "Reset" = write down a new start time. |
| `([x position] of (Sprite2))` | reporter | Reads another sprite's x position, y position, direction, costume #, costume name, size, volume, or one of its variables. For the Stage: backdrop #, backdrop name, volume, or its variables | `sprite2.xcor()`, `sprite2.ycor()`, `sprite2.heading()`, `sprite2.position()`; for variables, just use the variable (`sprite2_score`) | In Python one program can see everything, so "of" is just a dot: `sprite2.xcor()`. **Direction is different:** Scratch 90 = right, measured clockwise. Turtle `heading()` 0 = right, measured counter-clockwise (in standard mode). |
| `(current [year / month / date / day of week / hour / minute / second])` | reporter | Local clock values. Month 1–12; day of week **1 = Sunday … 7 = Saturday** | `now = datetime.datetime.now()` then `now.year`, `now.month`, `now.day`, `now.hour`, `now.minute`, `now.second`; day of week the Scratch way: `now.isoweekday() % 7 + 1` | Python's own `weekday()` uses 0 = Monday, so the numbers differ. Colab clocks are usually in **UTC**, not your home time. |
| `(days since 2000)` | reporter | Days (with decimals) since midnight, 1 Jan 2000 | `(datetime.datetime.now() - datetime.datetime(2000, 1, 1)).total_seconds() / 86400` | Tested: 9807.0 on 7 Nov 2026. |
| `(username)` | reporter | The Scratch username of the person viewing the project (blank if not logged in) | `getpass.getuser()` (gives the computer's login name, e.g. `ada`) | In Colab it returns `root`, which is not the child's name. Better: `name = input("What's your name? ")`. |
| `<online?>` (not in your list; a newer block, wiki-listed) | boolean | True if the computer is online | Not needed | Mention only if the child spots it. |

### Tested snippets

```python
answer = input("Pick a number: ")   # suppose the child types 7
print(answer + "3")       # 73   <- text glued together!
print(int(answer) + 3)    # 10   <- real maths
print(float("2.5") * 2)   # 5.0
int("seven")              # ValueError: invalid literal for int() with base 10: 'seven'
int(" 12 ")               # 12  (spaces are OK)
```

```python
import time
start = time.perf_counter()            # "reset timer"
time.sleep(0.2)
timer = time.perf_counter() - start    # "(timer)"
print(round(timer, 1))                 # 0.2
```

```python
import datetime
now = datetime.datetime.now()
print(now.year, now.month, now.day, now.isoweekday() % 7 + 1, now.hour, now.minute, now.second)
# 2026 11 7 7 0 27 38   (Saturday -> 7, same as Scratch)
```

```python
import turtle                     # desktop; ColabTurtlePlus has the same distance/xcor/ycor
a = turtle.Turtle(); b = turtle.Turtle(); b.goto(30, 40)
print(a.distance(b))             # 50.0   "distance to Sprite2"
print(b.xcor(), b.ycor())        # 30 40  "x position of Sprite2"
if a.distance(b) < 60:           # "touching Sprite2?"
    print("touching!")
```

Desktop-only events (instead of key pressed / mouse):

```python
screen = turtle.Screen()
def jump(): t.sety(t.ycor() + 50)
screen.onkeypress(jump, "space")   # like "when space key pressed"
def clicked(x, y): t.goto(x, y)    # x, y = mouse x / mouse y at the click
screen.onscreenclick(clicked)
t.ondrag(t.goto)                   # set drag mode [draggable]
screen.listen()
turtle.done()
```

## Gaps and gotchas

1. **Text vs number.** Scratch's `answer` is sometimes text and sometimes a number, and `(answer) + (1)` just works. In Python, `input()` always gives a string. You need `int(...)`, and if the child types a word you get a `ValueError` crash. For older kids, add `if answer.isdigit():` before converting.
2. **Uppercase and lowercase.** In Scratch, `answer = hello` is true even if the user typed "Hello". In Python, `"Hello" == "hello"` is `False`. Use `answer.lower() == "hello"`.
3. **Polling vs events.** `key pressed?` and `mouse down?` are questions you ask inside a forever loop. Python turtle uses events instead (`onkeypress`, `onscreenclick`), which are like Scratch hat blocks. ColabTurtlePlus has **no events at all**, so in Colab every interaction is turn-based with `input()`.
4. **Touching is approximate.** `distance < radius` treats sprites as circles. That is good enough for games, but explain that it is a "pretend bubble" around each turtle.
5. **No colour sensing or microphone.** Say this to the child: *"Scratch can look at the screen's colours and listen to the microphone. Plain Python turtle can't see or hear. It only knows the numbers you give it. So instead of 'touching red', we say 'is my y below -100, where the lava is?'"*
6. **The timer doesn't start by itself.** There is no green flag, so you must write down `start` yourself.
7. **Direction numbers differ.** Scratch direction 90 points right (clockwise from up). Turtle heading 0 points right (counter-clockwise). `ColabTurtlePlus` and desktop `turtle.mode("logo")` use up = 0, clockwise, which is closer to Scratch but still offset by 90.
8. **Colab time and username.** Colab runs on a Google server: `datetime.now()` is usually UTC and `getpass.getuser()` says `root`. That isn't a bug in the child's code.
9. **Day-of-week numbering.** Scratch: Sunday = 1. Python `weekday()`: Monday = 0. Use `isoweekday() % 7 + 1` to match Scratch.
10. **Only one `answer` in Scratch.** Each `ask` overwrites it. In Python each `input()` can go into its own named variable, which is a nice "upgrade" moment.

## Teaching ideas for a 9-year-old

**Analogy:** Sensing blocks are the sprite's **eyes, ears and watch**. In Python, `input()` is the program's **ears** (it waits and listens to you), `distance()` is its **measuring tape**, and `time` and `datetime` are its **stopwatch and calendar**. Python turtle has no "colour eyes" or "microphone ears", so we describe the world with numbers instead.

**Mini-challenge 1: Age Calculator (ask, answer, int, current year)**
```python
import datetime
age = int(input("How old are you? "))
year = datetime.datetime.now().year
print("You will be 100 in the year", year - age + 100)
```
Extension: remove `int(...)` first so they see the error, then fix it. That one moment teaches the biggest gotcha.

**Mini-challenge 2: Reaction Timer (timer, reset timer)**
```python
import time, random
input("Press Enter to get ready...")
time.sleep(random.uniform(1, 3))
start = time.perf_counter()               # reset timer
input("NOW! Press Enter!")
print("Your time:", round(time.perf_counter() - start, 3), "seconds")
```
Extension: three tries and print the best one (links to loops and variables).

**Mini-challenge 3: Treasure Hunt (distance to, touching via distance)**
A hidden "treasure" turtle at a random spot. Each turn the child types x and y with `input()`, the explorer turtle `goto`s there, and the program prints `"Distance to treasure:", round(explorer.distance(treasure))`. When `distance < 20`, it says "You found it!" and shows the treasure. This works in ColabTurtlePlus because it only uses `input()`. It recreates `distance to` and `touching?` without events.

## Sources

- Scratch Wiki, Sensing Blocks: https://en.scratch-wiki.info/wiki/Sensing_Blocks
- Scratch Wiki, individual blocks (Ask () and Wait, Answer, Timer, Days Since 2000, Current (), () of (), Distance to (), Loudness, Username): https://en.scratch-wiki.info/wiki/Ask_()_and_Wait_(block), https://en.scratch-wiki.info/wiki/Timer_(block), https://en.scratch-wiki.info/wiki/Days_Since_2000_(block), https://en.scratch-wiki.info/wiki/Current_()_(block), https://en.scratch-wiki.info/wiki/Of_(block), https://en.scratch-wiki.info/wiki/Distance_to_()_(block), https://en.scratch-wiki.info/wiki/Loudness_(block), https://en.scratch-wiki.info/wiki/Username_(block)
- scratch-vm source, sensing blocks (behaviour of ask queue, answer reset, current menu with dayofweek = getDay()+1, attribute-of options, distance 10000 fallback, days since 2000): https://github.com/scratchfoundation/scratch-vm/blob/develop/src/blocks/scratch3_sensing.js
- Scratch 3.0 block colours (scratch-blocks): https://github.com/scratchfoundation/scratch-blocks/blob/develop/core/colours.js
- Python docs: `input` https://docs.python.org/3/library/functions.html#input, `time.perf_counter` https://docs.python.org/3/library/time.html#time.perf_counter, `datetime` https://docs.python.org/3/library/datetime.html, `getpass.getuser` https://docs.python.org/3/library/getpass.html, `math.dist` https://docs.python.org/3/library/math.html#math.dist, turtle `distance`/`onkeypress`/`onscreenclick`/`ondrag` https://docs.python.org/3/library/turtle.html
- ColabTurtlePlus: https://github.com/mathriddle/ColabTurtlePlus
