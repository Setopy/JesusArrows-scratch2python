# 04. Events blocks (Scratch 3.0 to Python)

## Summary

Scratch's Events category is yellow (scratch-blocks event colours: primary `#FFBF00`, secondary `#E6AC00`, tertiary `#CC9900`). It has 9 blocks: 7 **hat blocks** that start a script, and 2 **stack blocks** (`broadcast`, `broadcast and wait`).

**The big idea:** Scratch is always **event-driven**. Every script sits waiting under its hat block, and the Scratch engine (scratch-vm) runs an invisible loop about 30 times a second. That loop checks for clicks, key presses, messages and thresholds and starts the matching scripts. A plain Python file or Colab cell is different: it runs **top to bottom, once, and then stops**. Python only reacts to events if you set up an **event loop** yourself:

- **Desktop `turtle` (IDLE/Thonny):** register handler functions (`screen.onkey`, `turtle.onclick`, `screen.onclick`, `screen.ontimer`), call `screen.listen()`, and finish with `turtle.mainloop()` / `turtle.done()`. `mainloop()` is the Python version of Scratch's invisible engine loop.
- **Colab + ColabTurtlePlus:** there are no key or click events. The kid builds the event loop by hand: `while True:` + `input()` + `if/elif` (or a dict of handler functions). The cell's Run button stands in for the green flag.

Every Scratch "script under a hat" becomes **a Python function**. "Broadcast" becomes **calling functions**: directly, or through a small dictionary of message names mapped to lists of functions (tested below).

## Block-by-block mapping table

| Scratch block (exact text) | What it does in Scratch (scratch-vm detail) | Desktop `turtle` equivalent | Colab / ColabTurtlePlus workaround |
|---|---|---|---|
| `when green flag clicked` (hat) | Starts every script under this hat in every sprite. If a script is already running, it **restarts** it (`restartExistingThreads: true`). | Run the file (F5 in IDLE/Thonny). Top-level code is the green-flag script. Optionally `def green_flag(): ...` and call it at the bottom. | Run the cell (Shift+Enter). For a "new game" you re-run the cell, or wrap everything in `def green_flag():` and call it. |
| `when [space v] key pressed` (hat) | Options: a to z, 0 to 9, arrow keys, space, `any`. Does **not** restart a running copy of its script (`restartExistingThreads: false`); a second press while it runs is ignored. Held keys repeat only at the operating system's key-repeat rate. | `screen.onkeypress(func, "space")` (fires on press, repeats while held) or `screen.onkey(func, "Up")` (fires on **release**). Key names: `"a"`, `"space"`, `"Up"`, `"Down"`, `"Left"`, `"Right"`, `"Return"`. `screen.onkeypress(func)` with no key means any key. **Must** call `screen.listen()` and end with `turtle.mainloop()`. | No key events. Use `key = input("Key (w/a/s/d, q to quit): ")` inside `while True:` and `if key == "a": ...` or a dict `{"a": go_left, "d": go_right}`. The kid must press Enter after each key. |
| `when this sprite clicked` (hat) | Runs when you click this sprite's visible pixels. Restarts if already running. Only appears in the palette when a sprite is selected. | `t.onclick(func)`. `func(x, y)` **must take two parameters** (the click position). Also `t.ondrag(t.goto)` and `t.onrelease(func)`. Needs `mainloop()`. | No clicks. Use a menu: `choice = input("Click who? cat/dog: ")` and call `cat_clicked()`. |
| `when stage clicked` (hat) | Runs when you click the stage where no sprite is. Only appears when the Stage is selected. Restarts if running. | `screen.onclick(func)` (also `turtle.onscreenclick`). `func(x, y)` gets the click position. Classic trick: `screen.onclick(t.goto)` sends the turtle to where you click. | Ask for coordinates: `x = int(input("x? "))`, `y = int(input("y? "))`, then call `stage_clicked(x, y)`. |
| `when backdrop switches to [backdrop1 v]` (hat) | Runs when the backdrop changes to the named one (by `switch backdrop to`, `next backdrop`, etc.). Restarts if running. | No built-in. Write your own `switch_backdrop_to(name)` that sets `screen.bgcolor()` or `screen.bgpic()` **and** calls the handlers for that name (dict pattern below). | Same home-made function; ColabTurtlePlus can change `bgcolor()`. |
| `when [loudness v] > (10)` (hat) | Options: `loudness` and `timer` (plus `video motion` once the Video Sensing extension is added). **Edge-triggered** (`edgeActivated: true`): fires once when the value goes from "not greater" to "greater", not again until it drops back below and crosses again. Strict `>` comparison. | **Timer:** `screen.ontimer(func, 3000)` runs `func` once after 3000 milliseconds (milliseconds, not seconds!). Or keep `start = time.time()` and check `time.time() - start > 3` in a loop with a `fired` flag. **Loudness:** no simple equivalent (needs a microphone library; skip for a 9-year-old). | Timer: `import time`, `start = time.time()`, check in your loop with a `fired = False` flag so it fires once (tested). Or simply `time.sleep(3)` then do the thing. Loudness: not available. |
| `when I receive [message1 v]` (hat) | Runs when that message is broadcast. **Restarts** the script if it is already running (`restartExistingThreads: true`). Any sprite or the Stage can receive. | `def message1(): ...` A receiver is just a function. For many receivers of one message, use the `receivers` dict (below). | Identical (pure Python, no turtle events needed). |
| `broadcast (message1 v)` (stack) | Sends the message to every sprite and the Stage, then **carries on immediately** without waiting. | Call the function(s): `message1()` or `broadcast("message1")`. **Difference:** a Python function call finishes before the next line runs, so a plain call actually behaves like `broadcast and wait`. True "fire and carry on" needs `screen.ontimer(message1, 0)` (desktop) and is rarely needed. | Plain function call. |
| `broadcast (message1 v) and wait` (stack) | Starts all receiving scripts, then pauses until **all** of them have finished (it checks every frame). If nobody receives the message, it continues straight away. | A plain function call: `broadcast("message1")`. Python waits for the function to return. | Plain function call. |

### Tested broadcast system (dictionary of handlers)

Ran with `python3` on 7 Nov 2026; output: `Cat: Oh no!`, `Stage: GAME OVER`.

```python
receivers = {}                       # message name -> list of scripts

def when_i_receive(message):         # the hat block (a "decorator")
    def add(func):
        receivers.setdefault(message, []).append(func)
        return func
    return add

def broadcast(message):              # the broadcast block
    for func in receivers.get(message, []):
        func()

@when_i_receive("game over")
def cat_says():
    print("Cat: Oh no!")

@when_i_receive("game over")
def stage_says():
    print("Stage: GAME OVER")

broadcast("game over")
broadcast("nobody listens")          # like Scratch: no error, nothing happens
```

A decorator-free version for a first lesson (also tested):

```python
def dog_barks():
    print("Dog: Woof!")

messages = {"bark": [dog_barks]}
for script in messages["bark"]:
    script()
```

### Desktop `turtle` event template (green flag + keys + clicks + timer)

```python
import turtle
screen = turtle.Screen()
cat = turtle.Turtle(shape="turtle")

def go_right():          # when [right arrow] key pressed
    cat.setheading(0); cat.forward(10)

def cat_clicked(x, y):   # when this sprite clicked (needs x, y!)
    cat.write("Meow!")

def stage_clicked(x, y): # when stage clicked
    cat.goto(x, y)

def three_seconds():     # when [timer] > (3)
    cat.color("red")

screen.onkeypress(go_right, "Right")
cat.onclick(cat_clicked)
screen.onclick(stage_clicked)
screen.ontimer(three_seconds, 3000)
screen.listen()          # let the window hear the keyboard
turtle.mainloop()        # the "Scratch engine": keep waiting for events (last line)
```

Not run here (needs a window), but uses only the documented API in the Python `turtle` docs.

### Colab event loop template (ColabTurtlePlus)

```python
handlers = {"a": go_left, "d": go_right, "w": go_up, "s": go_down}
while True:                                  # our own "forever" event loop
    key = input("Press w/a/s/d then Enter (q to quit): ")
    if key == "q":
        break
    if key in handlers:
        handlers[key]()                      # "when [key] key pressed"
    else:
        print("No script for", key)
```

(The dict logic was tested in Bash with stand-in functions.)

## Gaps and gotchas

1. **Forgetting `mainloop()` / `listen()`.** Without `screen.listen()` key presses are ignored. Without `turtle.mainloop()` (or `done()`) a script run from the command line closes immediately. `mainloop()` must be the **last** line; code after it does not run until the window closes.
2. **Click handlers need `(x, y)`.** `turtle.onclick` and `screen.onclick` call your function with two numbers. `def clicked():` with no parameters crashes with a `TypeError`. Key handlers are the opposite: **no** parameters.
3. **Pass the function, don't call it.** `screen.onkey(jump, "space")`, not `screen.onkey(jump(), "space")`. The brackets would run `jump` once immediately and register `None`. Kids hit this one constantly.
4. **`onkey` fires on release.** In Python 3 `onkey` is the same as `onkeyrelease`. Use `onkeypress` to match Scratch's "pressed" feeling and get repeats while the key is held.
5. **Key names are case-sensitive Tk names:** `"Up"`, `"space"`, `"Return"`, not `"up arrow"` or `"Space"`.
6. **`ontimer` is in milliseconds and fires once.** To repeat, the function re-schedules itself (`screen.ontimer(f, 250)` at its end). That is the Python version of a `forever` loop that keeps the event loop free. A `while True:` loop with `time.sleep` inside a turtle program **freezes** key and click handling, because `mainloop()` never gets a turn.
7. **Python does one thing at a time.** Scratch runs many scripts "at once" (it switches between them every frame). Python handlers run one after another. A slow handler blocks all others. So `broadcast` (don't wait) and `broadcast and wait` both become a plain call in Python, which behaves like **and wait**.
8. **Restart rules differ.** In Scratch, green flag, sprite click, stage click, backdrop switch and `when I receive` **restart** a running script, but a key-press hat and `when [timer] >` do **not**. Python never restarts anything; each call is a fresh run. A script that broadcasts its own message at the end makes a loop in Scratch; the Python equivalent (a function calling itself) is recursion and crashes after about 1000 levels (`RecursionError`). Use a `while` loop instead.
9. **Edge-triggered `when >`.** It fires once per crossing, so the Python check needs a `fired` flag (or `ontimer`). Otherwise it runs every time round the loop.
10. **Loudness and video motion** have no beginner-friendly Python equivalent. Say so honestly and skip them.
11. **Colab has no live keyboard or mouse for turtle.** ColabTurtlePlus draws in the notebook output and does not provide `onkey`/`onclick`/`ontimer`/`mainloop`. `input()` needs the Enter key and blocks the cell while it waits. Games become turn-based ("press a, Enter"). Also, Scratch's `ask` box pauses key-press hats, just as `input()` pauses everything.
12. **Up/down arrow hats also fire on mouse scroll** in Scratch. Kids sometimes rely on this by accident; Python will not do it.
13. **`when stage clicked` and `when this sprite clicked`** only appear in the palette for the Stage or a sprite respectively. In Python both are available on any screen or turtle.

## Teaching ideas for a 9-year-old

**Analogy: the doorbell and the butler.** In Scratch, every sprite has a butler (the Scratch engine) standing by the door all day, waiting for the doorbell (an event) and then doing the job written on the card (the script). A Python program is like a to-do list you read once from top to bottom, and then you go home. `turtle.mainloop()` is hiring the butler: "Stand here and wait. When someone rings the **space** bell, do the `jump` card." In Colab there is no butler, so **you** stand at the door: `while True:` keeps asking "Who's there?" with `input()`. A **broadcast** is shouting a message through the house. Everyone who has a card for that message (`when I receive`) does their job.

**Mini-challenges**

1. **Green flag = Run button (Colab).** Rebuild a Scratch "when green flag clicked → say Hello → move 100" script as a cell. Then wrap it in `def green_flag():` and call it twice. Question: "What is the Python green flag?" (Running the cell, or calling the function.)
2. **Remote-control turtle (Colab, then desktop).** In Colab, make a `while True:` + `input()` loop where `w/a/s/d` move the turtle and `q` quits, using a dict of handler functions. Bonus at home in IDLE/Thonny: swap the loop for `screen.onkeypress(...)`, `screen.listen()`, `turtle.mainloop()` and feel the difference (no Enter key needed).
3. **Message party (pure Python, works anywhere).** Use the `receivers` / `broadcast` system. Make three "sprites" (functions) that each react to `"party"` with a different `print` or turtle drawing, then `broadcast("party")`. Stretch: a `"game over"` message, plus a `switch_backdrop_to("night")` function that changes `bgcolor` and broadcasts `"night time"`.

**Quick-check questions:** Why does `def clicked(x, y):` need `x, y` but `def jump():` does not? What happens if you forget `screen.listen()`? What goes wrong if you write `screen.onkey(jump(), "space")`?

## Sources

- Scratch Wiki, Events Blocks: https://en.scratch-wiki.info/wiki/Events_Blocks
- Scratch Wiki, Broadcast () (block): https://en.scratch-wiki.info/wiki/Broadcast_(block)
- Scratch Wiki, When () Key Pressed (Events block): https://en.scratch-wiki.info/wiki/When_()_Key_Pressed_(Events_block)
- scratch-vm source, event blocks (`getHats` restart/edge flags, `broadcastAndWait`, `hatGreaterThanPredicate`, key handling): https://github.com/scratchfoundation/scratch-vm/blob/develop/src/blocks/scratch3_event.js
- scratch-blocks colours (event `#FFBF00` / `#E6AC00` / `#CC9900`; the raw-file fetch failed, so these values are from memory of `core/colours.js`): https://github.com/scratchfoundation/scratch-blocks/blob/develop/core/colours.js
- Python docs, `turtle` (onkey, onkeypress, onkeyrelease, onclick, onscreenclick, onrelease, ondrag, ontimer, listen, mainloop, done, exitonclick): https://docs.python.org/3/library/turtle.html
