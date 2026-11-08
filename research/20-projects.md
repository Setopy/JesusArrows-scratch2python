# 20. Project patterns: rebuilding the classic Scratch starter projects in Python

## Summary

- The official Scratch starter projects (in-editor Tutorials and the Coding Cards) rely on four patterns: **keyboard or mouse events**, **forever loops with `if touching`**, **variables that hold a score or a stat**, and **`ask and wait`**. Only the first has no equivalent in ColabTurtlePlus. It has no `onkey`, `onclick` or `ontimer`, so every "when key pressed" game becomes a **turn-based `input()` loop**. Turn-based play keeps the game logic the same: move, check touching, change score. This turned out to be the main design decision for the whole capstone path.
- Eight projects were written, each under 40 lines with child-level comments: Animate a Name, Times Tables Quiz, Guess the Number, Virtual Pet, Pen Art Flower, Choose-Your-Own Story, Chase Game (turns), and Catch the Apple. Three use ColabTurtlePlus (1, 5, 8). Five are plain text, so they also run anywhere.
- **All 8 were run with `python3`.** The five text games were fed input through `printf`/`yes` pipes and through small auto-player bots. Bots typed the correct quiz answers, binary-searched the secret number, and chased the star. The three turtle programs were run against a **mock `ColabTurtlePlus.Turtle` module**. The mock is built from the real source on GitHub: it allows only names in the real `_tg_turtle_functions` / `_tg_screen_functions` lists and only colours in the real `VALID_COLORS` list. It correctly rejected `t.onkey()`, `onclick` and `color('Red')`. The drawings themselves were **not** viewed in Colab.
- ColabTurtlePlus details checked in the source (`Turtle.py`, GitHub main), relevant to these projects:
  - `write(obj, align=..., font=(name, size, type))` exists.
  - `jumpto()`/`teleport()` move instantly, like Scratch "go to x: y:".
  - Shapes are `turtle, ring, classic, arrow, square, triangle, circle, turtle2, blank`.
  - `speed()` is 0 to 13, and **speed 0 needs `done()`** at the end or nothing is shown.
  - **Colour names must be lowercase HTML names**: `"Red"` raises an error.
  - `hideturtle`, `dot`, `stamp`, `begin_fill`/`end_fill` and `bgcolor` all exist.

## Tutorial list (official Scratch 3.0 starter projects)

Sources: the in-editor Tutorials library (`scratch.mit.edu/projects/editor/?tutorial=all`) and the Scratch Coding Cards (scratch-cards-all.pdf, now redirected to the Scratch Foundation Learning Library). The Scratch site pages render with JavaScript and could not be fetched as text. The card set titles were confirmed by a web search of the cards PDF. The block lists below come from the published card contents and are marked as such.

| Tutorial / card set | Key Scratch blocks | Fit for Colab Python |
|---|---|---|
| Getting Started | when flag clicked, move, play sound | Covered by modules |
| **Animate a Name** (tutorial + cards) | when this sprite clicked, change color effect, turn, glide, play sound | **Good** (turtle `write`, loops) |
| Animate a Character | switch costume, next costume, wait, glide, forever | Partial (no costumes; `shape`/`stamp`) |
| Make Music | play drum, play note, set tempo, repeat | Poor (sound needs IPython.display.Audio; skip) |
| Create a Story | say for secs, switch backdrop, broadcast, when I receive | **Good** (print, functions as "scenes") |
| Create Animations That Talk / Code a Cartoon | say, change size, glide, when backdrop switches | Text/turtle partial |
| Imagine a World | switch backdrop, glide, say, when key pressed | Partial |
| **Make It Fly** (tutorial + digital cards) | when key pressed, change y, glide, forever, go to random | Turn-based only |
| **Chase Game** (tutorial "Make a Chase Game" + cards) | when key pressed, change x/y, if touching, change score, go to random position | **Good as turn-based grid** |
| **Pong Game** (tutorial + cards) | forever, move, if on edge bounce, if touching paddle, point in direction, set x to mouse x | Automatic-bounce animation only (no mouse) |
| **Catch Game** (cards) | go to x: random y: 180, change y by -5, repeat until, if touching, change score | **Good** (input picks bowl lane, apple animates) |
| **Virtual Pet** (cards) | variables (hunger/happiness), when sprite clicked, change by, broadcast, say | **Good** (text menu loop) |
| Hide and Seek / Clicker game | show, hide, go to random position, when sprite clicked | Text guessing variant |
| Let's Dance / Video Sensing | video motion, switch costume, play sound | Not possible (camera) |
| Jumping Game / Race to the Finish | when key pressed, change y, gravity loop, if touching | Turn-based or auto-race simulation |
| Pen extension ideas (Pen card / Ideas page) | pen down, set pen color, repeat, turn, move | **Excellent** (turtle is the Pen extension) |

## The 8 projects (difficulty order)

Every program follows the setup convention `from ColabTurtlePlus.Turtle import *`, `clearscreen()`, `setup(480, 360)`, `t = Turtle()` (480 x 360 is the Scratch stage size, with the origin in the centre, so Scratch x/y coordinates carry over). The text projects need no import beyond `random`.

### Project 1: Animate a Name (turtle)

- **Scratch version:** each letter is a sprite. `when this sprite clicked` then `change color effect by 25`, `turn 15 degrees` (repeat), `play sound`, `glide`.
- **Python concepts:** `input()`, strings as sequences (`for letter in name`), lists + `random.choice`, a variable that changes (`x = x + gap`), nested loops, `t.write(..., font=...)`.

```python
# Project 1: Animate a Name
from ColabTurtlePlus.Turtle import *
import random

clearscreen()
setup(480, 360)            # same size as the Scratch stage
bgcolor("black")
t = Turtle()
t.speed(8)
t.hideturtle()             # like "hide" in Looks
t.penup()                  # move without drawing lines

name = input("What is your name? ")
colours = ["red", "orange", "gold", "limegreen", "skyblue", "violet"]
gap = min(45, 400 // len(name))    # squash long names so they fit

x = -200                           # like "go to x: -200"
for letter in name:                # one letter at a time
    t.goto(x, 40)
    t.color(random.choice(colours))    # like "change color effect"
    t.write(letter, align="center", font=("Arial", 40, "bold"))
    x = x + gap                    # like "change x by 45"

# Make the letters bounce, getting smaller each time
size = 30
for jump in range(3):              # repeat 3
    x = -200
    for letter in name:
        t.goto(x, -40 - jump * 45)
        t.color(random.choice(colours))
        t.write(letter, align="center", font=("Arial", size, "normal"))
        x = x + gap
    size = size - 8

t.goto(0, -170)
t.color("white")
t.write("Hello, " + name + "!", align="center", font=("Arial", 16, "italic"))
```

- **Testing:** run against the API mock with "Zainab" and with a 20-character name (the `gap` line keeps it on stage). Calls used: `bgcolor, clearscreen, color, goto, hideturtle, penup, setup, speed, write`, all of them real ColabTurtlePlus names. `write` takes only `align`/`font`. The visual layout was not checked in Colab.

### Project 2: Times Tables Quiz (text)

- **Scratch version:** `ask (join a " x " b) and wait`, `if answer = a * b then change score by 1 / say Correct else say ...`, `pick random 2 to 12`, `repeat 5`.
- **Python concepts:** `for ... in range`, `random.randint`, f-strings (the Python `join`), `if/else`, `if/elif/else` for the final message, comparing text with `str(a*b)` so non-numbers cannot crash it.

```python
# Project 2: Times Tables Quiz
import random

score = 0                  # like "make a variable: score"
rounds = 5
print("Welcome to the Times Tables Quiz!")

for question in range(1, rounds + 1):     # repeat 5
    a = random.randint(2, 12)             # pick random 2 to 12
    b = random.randint(2, 12)
    answer = input(f"Question {question}: What is {a} x {b}? ")   # ask and wait
    if answer.strip() == str(a * b):      # compare as text, so "cat" can't crash it
        score = score + 1                 # change score by 1
        print("Correct!")
    else:
        print("Not quite. It was", a * b)

print(f"You scored {score} out of {rounds}.")
if score == rounds:
    print("Perfect! Maths champion!")
elif score >= 3:
    print("Great work!")
else:
    print("Keep practising, you'll get there!")
```

- **Testing:** `printf 'cat\n1\n2\n\n99\n' | python3` gave 0/5 with no crash on "cat" or a blank answer. A bot that computed the right answers gave 5/5, "Perfect!".

### Project 3: Guess the Number (text)

- **Scratch version:** `set secret to pick random 1 to 100`, `repeat until answer = secret`, `ask`, `if answer < secret say Too low`, `change tries by 1`.
- **Python concepts:** `while` loop (Scratch "repeat until" with the condition flipped), `int()`, `.isdigit()` input checking, `continue`, counting with a variable.

```python
# Project 3: Guess the Number
import random

secret = random.randint(1, 100)   # the computer picks a secret number
tries = 0
guess = 0
print("I'm thinking of a number from 1 to 100.")

while guess != secret:            # like "repeat until guess = secret"
    text = input("Your guess: ")
    if not text.strip().isdigit():    # stop "banana" from crashing the game
        print("Please type a whole number.")
        continue                  # go back to the top of the loop
    guess = int(text)
    tries = tries + 1
    if guess < secret:
        print("Too low!")
    elif guess > secret:
        print("Too high!")

print(f"You got it in {tries} tries!")
if tries <= 7:
    print("Super smart guessing!")
```

- **Testing:** a binary-search bot (seed 3) won in 4 tries ("Super smart guessing!"). Piping `banana` printed "Please type a whole number." and the loop continued. Good follow-up lesson: why 7 guesses is always enough (halving).

### Project 4: Virtual Pet (text)

- **Scratch version (cards):** variables `hunger`, `happiness`; `when this sprite clicked` → `change hunger by -1`, `say Yum`; a `forever` loop that slowly changes stats; `if hunger > 9 then ...`.
- **Python concepts:** several variables as "state", `while True` + `break` (Scratch "forever" + "stop all"), menu with `if/elif/else`, `min()`/`max()` to keep values between 0 and 10, `.strip().lower()`.

```python
# Project 4: Virtual Pet (text version)
import random

name = input("Name your pet: ")
hunger = 3        # 0 = full, 10 = starving
happy = 7         # 0 = sad, 10 = very happy
energy = 7        # 0 = worn out, 10 = full of beans
day = 0

while True:                                    # like "forever"
    day = day + 1
    print(f"\nDay {day}: {name}  hunger {hunger}  happy {happy}  energy {energy}")
    choice = input("feed, play, sleep or quit? ").strip().lower()
    if choice == "feed":
        hunger = max(0, hunger - 4)            # never below 0
        print(f"{name} munches happily. Yum!")
    elif choice == "play":
        if energy < 2:
            print(f"{name} is too tired to play.")
        else:
            happy = min(10, happy + 3)         # never above 10
            energy = energy - 2
            print(f"{name} chases the ball!")
    elif choice == "sleep":
        energy = 10
        print("Zzz... zzz...")
    elif choice == "quit":
        print(f"Bye! {name} will miss you.")
        break                                  # like "stop all"
    else:
        print("Try feed, play, sleep or quit.")
    hunger = min(10, hunger + 1)               # pets get hungry every day
    happy = max(0, happy - random.choice([0, 1]))
    if hunger == 10 or happy == 0:
        print(f"Oh no! {name} ran away. Look after your pet better next time!")
        break
```

- **Testing:** `printf 'Biscuit\nfeed\nplay\nPLAY\nsleep\ndance\nplay\nquit\n'` covered every branch: uppercase "PLAY" accepted, "dance" gave the help text, "quit" ended. An input of only "sleep" (`yes sleep`) let hunger reach 10 on day 7 and the pet ran away. Extension: add the turtle drawing a face whose `color` depends on `happy`.

### Project 5: Pen Art Flower (turtle)

- **Scratch version (Pen extension):** `erase all`, `pen down`, `set pen color to`, `repeat (petals)`, `repeat 2 [ arc ]`, `turn (360 / petals) degrees`.
- **Python concepts:** nested `for` loops, `%` to cycle through a colour list, maths in arguments (`360 / petals`), `circle(radius, extent)` for arcs, `dot()`.

```python
# Project 5: Pen Art Flower
from ColabTurtlePlus.Turtle import *

clearscreen()
setup(480, 360)
bgcolor("black")
t = Turtle()
t.speed(13)                    # fastest
t.pensize(2)                   # like "set pen size to 2"
colours = ["red", "orange", "gold", "limegreen", "skyblue", "violet"]

petals = int(input("How many petals (3 to 20)? "))

for p in range(petals):                     # repeat (petals)
    t.color(colours[p % len(colours)])      # next colour each petal
    for side in range(2):                   # a petal is two curves
        t.circle(100, 60)                   # part of a circle
        t.left(120)
    t.left(360 / petals)                    # turn so petals go all the way round

# A yellow middle
t.penup()
t.goto(0, 0)
t.dot(30, "gold")
t.hideturtle()
```

- **Testing:** run against the mock with 8 petals. Calls `circle, color, dot, left, pensize, penup, goto, hideturtle, bgcolor, setup, clearscreen, speed` are all real. `dot(30, "gold")` matches the real signature `dot(size=None, *color)`. Typing "eight" would crash `int()`. That is a good discussion point, or reuse the `isdigit` check from Project 3.

### Project 6: Choose-Your-Own Story (text)

- **Scratch version (Create a Story):** `say ... for 2 seconds`, `switch backdrop to`, `broadcast cave`, `when I receive cave`, `ask ... and wait`, `if answer = left`.
- **Python concepts:** **defining functions** (a function = a "when I receive" script; calling it = "broadcast"), parameters and `return`, a validation `while` loop, `"/".join(list)`.

```python
# Project 6: Choose-Your-Own Story
def ask(question, options):
    """Keep asking until the reader types one of the options."""
    answer = ""
    while answer not in options:
        answer = input(question + " (" + "/".join(options) + ") ").strip().lower()
    return answer

def cave():                       # a "scene", like a new backdrop
    print("The cave is dark. Something glitters... and something growls.")
    if ask("Grab the treasure or tiptoe out?", ["grab", "tiptoe"]) == "grab":
        print("A friendly dragon wakes up and shares its gold. THE END")
    else:
        print("You sneak out and live to explore another day. THE END")

def river():
    print("A wide river blocks the path. There is a wobbly boat.")
    if ask("Row the boat or swim?", ["row", "swim"]) == "row":
        print("You row to an island full of talking parrots. THE END")
    else:
        print("Brrr! Too cold. You swim back for hot chocolate. THE END")

hero = input("What is your hero's name? ")
print(f"{hero} stands at the edge of the Whispering Forest.")
if ask("Go left to the cave or right to the river?", ["left", "right"]) == "left":
    cave()                        # like "broadcast cave"
else:
    river()
```

- **Testing:** all four endings reached by piped choices (`left grab`, `left tiptoe`, `right row`, `right swim`). An invalid answer and uppercase `LEFT` were both handled (the question was asked again, or the answer accepted).

### Project 7: Chase Game, one move per turn (text)

- **Scratch version (Chase Game):** `when right arrow key pressed` → `change x by 10`; star: `if touching player` → `change score by 1`, `go to random position`; enemy `forever` `point towards player`, `move`.
- **Python concepts:** x/y coordinates as variables, a 2D grid printed with nested loops, tuple comparison `(x, y) == (px, py)` as "touching", boundary checks with `and`, `random.random() < 0.6` as a probability, `break` on game over.

```python
# Project 7: Chase Game (one move per turn)
import random
SIZE = 7
px, py = 0, 0                    # you (P) start top-left
gx, gy = SIZE - 1, SIZE - 1      # the ghost (G) starts bottom-right
sx, sy = random.randint(1, SIZE - 1), random.randint(1, SIZE - 1)   # the star (*)
score = 0
for turn in range(1, 21):        # 20 turns
    for y in range(SIZE):        # draw the board, one row at a time
        row = ""
        for x in range(SIZE):
            if (x, y) == (px, py): row = row + "P "
            elif (x, y) == (gx, gy): row = row + "G "
            elif (x, y) == (sx, sy): row = row + "* "
            else: row = row + ". "
        print(row)
    move = input(f"Turn {turn}, score {score}. Move w/a/s/d: ").strip().lower()
    if move == "w" and py > 0: py = py - 1          # up    (change y by 10)
    if move == "s" and py < SIZE - 1: py = py + 1   # down
    if move == "a" and px > 0: px = px - 1          # left  (change x by -10)
    if move == "d" and px < SIZE - 1: px = px + 1   # right
    if (px, py) == (sx, sy):                        # "if touching star"
        score = score + 1
        print("You got the star!")
        sx, sy = random.randint(0, SIZE - 1), random.randint(0, SIZE - 1)  # go to random position
    if random.random() < 0.6:            # ghost chases you 6 turns in 10
        if gx < px: gx = gx + 1
        elif gx > px: gx = gx - 1
        elif gy < py: gy = gy + 1
        elif gy > py: gy = gy - 1
    if (gx, gy) == (px, py):
        print("The ghost caught you! GAME OVER")
        break
print("Final score:", score)
```

- **Testing:** piped moves (`d/s` diagonal run) ended in "The ghost caught you! GAME OVER" on turn 12. Invalid keys (`yes x`) left the player still. A star-seeking bot over 6 seeds scored 0 to 3 stars. The ghost chase chance was lowered from 0.7 to 0.6 after this test. Tuning `0.6` is a good "make it easier/harder" exercise. Playing with no key presses works because `input()` acts like a frozen game clock.

### Project 8: Catch the Apple (turtle + input)

- **Scratch version (Catch Game cards):** apple `go to x: (pick random) y: 180`, `repeat until y < -170` `change y by -5`, `if touching bowl` `change score by 1` `else go to top`; bowl `when key pressed` `change x by`.
- **Python concepts:** two Turtle objects (two sprites), a list of lane positions, `range` with a negative step (falling), `jumpto` vs `goto` (instant vs gliding), a random "wind" event, list indexing with `lane - 1`.

```python
# Project 8: Catch the Apple
from ColabTurtlePlus.Turtle import *
import random
clearscreen()
setup(480, 360)
bgcolor("skyblue")
lanes = [-150, 0, 150]               # x positions of lanes 1, 2 and 3
bowl = Turtle()
bowl.shape("square")
bowl.color("brown")
bowl.penup()
apple = Turtle()
apple.shape("circle")
apple.color("red")
apple.penup()
score = 0
for rnd in range(1, 6):                       # 5 apples
    lane = random.randint(0, 2)               # pick random lane
    apple.jumpto(lanes[lane], 160)            # appear at the top, instantly
    print(f"Apple {rnd} is above lane {lane + 1}. It's windy!")
    pick = input("Move the bowl to lane 1, 2 or 3: ").strip()
    bowl_lane = 1                             # middle, if you type something odd
    if pick in ["1", "2", "3"]:
        bowl_lane = int(pick) - 1
    bowl.goto(lanes[bowl_lane], -140)
    for y in range(160, 10, -30):             # fall halfway: "change y by -30"
        apple.goto(lanes[lane], y)
    if random.random() < 0.3:                 # a gust of wind!
        lane = max(0, min(2, lane + random.choice([-1, 1])))
    for y in range(10, -150, -30):            # fall the rest of the way
        apple.goto(lanes[lane], y)
    if lane == bowl_lane:                     # "if touching bowl"
        score = score + 1
        print("Caught it!")
    else:
        print("Splat! It landed in lane", lane + 1)
print("You caught", score, "out of 5 apples.")
```

- **Testing:** `printf '2\n1\nbanana\n3\n3\n'` with the mock: "banana" fell back to the middle lane and was caught; the wind moved apple 2 from lane 1 to lane 2 (splat), score 1/5. Calls `shape("square")`, `shape("circle")`, `jumpto`, `goto` and colours `brown`, `red`, `skyblue` are all valid. Not viewed in Colab: at speed 5 the fall animation may be slow. Raise it with `apple.speed(10)` if needed.

## Capstone path (after the 8 modules)

The path is ordered so that each project adds one big idea and reuses the previous ones.

| Step | Project | New big idea | Uses from earlier |
|---|---|---|---|
| 1 | Animate a Name | loop over a string, turtle `write` | modules on motion/looks |
| 2 | Pen Art Flower | nested loops, maths in turns, `%` | step 1 turtle setup |
| 3 | Times Tables Quiz | `input`, `if/else`, score variable | loops |
| 4 | Guess the Number | `while` (repeat until), input checking | step 3 |
| 5 | Choose-Your-Own Story | **own functions** (= broadcast / when I receive) | steps 3-4 |
| 6 | Virtual Pet | several state variables, `while True`/`break`, `min`/`max` | steps 4-5 |
| 7 | Chase Game (turns) | x/y grid, "touching" as equal coordinates, probability | steps 3-6 |
| 8 | Catch the Apple | two turtles + game loop + score together (the "real game") | everything |

The suggested final challenge (stretch, not written here) is an automatic **Pong** animation: a ball turtle bouncing off walls with `if abs(x) > 230: dx = -dx`, and the paddle moved by `input()` every 10 frames. It is the Scratch "if on edge, bounce" idea, done by hand.

Things that do not translate, so tell the child up front:
- live key/mouse control (the turn-based `input()` replaces it)
- sound (Make Music)
- camera (Video Sensing, Let's Dance)
- costumes (use `shape`, colours and `stamp` instead)

## Sources

- Scratch Coding Cards (all), now redirected to the Learning Library: https://resources.scratch.mit.edu/www/cards/en/scratch-cards-all.pdf, https://www.scratchfoundation.org/learn/learning-library
- Scratch Ideas page: https://scratch.mit.edu/ideas
- In-editor tutorials library: https://scratch.mit.edu/projects/editor/?tutorial=all
- Scratch Getting Started guide: https://resources.scratch.mit.edu/www/guides/en/scratch-getting-started-guide.pdf
- ColabTurtlePlus repository and README: https://github.com/mathriddle/ColabTurtlePlus
- ColabTurtlePlus source used for the API mock: https://raw.githubusercontent.com/mathriddle/ColabTurtlePlus/main/ColabTurtlePlus/Turtle.py
