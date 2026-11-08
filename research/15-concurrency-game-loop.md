# 15. How Scratch runs many scripts at once, and the Python game loop

## Summary

**For the parent.** Scratch looks like it runs every script at the same time, but it doesn't. scratch-vm has one *sequencer*. On each frame it walks a list of *threads* (one per running script), and it runs each thread until that thread *yields*. A thread yields at the end of each loop pass (`forever`, `repeat`, `repeat until`), at `wait`, at `glide`, at `say ... for ... secs`, at `broadcast and wait`, and at sounds it waits for. Then the sequencer moves on to the next thread. Facts from the source:

- The runtime has two step intervals: `THREAD_STEP_INTERVAL = 1000/60` and `THREAD_STEP_INTERVAL_COMPATIBILITY = 1000/30`. The Scratch editor runs in compatibility mode, so you get about **30 frames per second**.
- `sequencer.stepThreads` spends at most `WORK_TIME = 0.75 * currentStepTime` per frame. Within that time it can go round the thread list more than once. It stops early when a sprite has changed how the screen looks (`redrawRequested`), unless **Turbo Mode** is on. A loop that only changes variables can therefore run many times in one frame. A loop that moves a sprite runs about once per frame.
- **Turbo Mode** removes the "stop when a redraw is needed" check. Loops then run many iterations per frame, as in "Run without screen refresh" (warp mode, which caps at `WARP_TIME = 500 ms`).
- **Order**: threads are stepped from index 0 upward, and each new frame starts again from index 0. `startHats` walks `executableTargets` from the end to the start, and that list "shares its order with drawables" (the layer order). So the sprite on the **top layer starts its hat scripts first**, and the **Stage goes last**. When one hat block triggers several scripts in the same sprite, they start in script order. Most projects should not depend on any of this.
- **Restart rule**: green-flag and broadcast hats restart a thread that is already running. The thread keeps its place in the list and begins again from the top. A second `broadcast` while the first handler is still inside a `wait` cancels that handler halfway. This is the classic broadcast race.

**For the 9-year-old.** Scratch is like **one juggler with lots of balls**. The juggler gives each ball a little push (one trip round each `forever` loop), then moves to the next ball, and keeps cycling so fast it looks like everything moves together. Python is a juggler who only ever holds **one ball**, until you write the juggling yourself. That's the **game loop**. Each time round the loop is one *frame*, and in that frame you give every sprite its little push.

**Recommendation.** In Colab (ColabTurtlePlus, which has no `ontimer` and no `mainloop`), teach **one game loop**: `for frame in range(N):` that calls `update_cat()`, then `update_ghost()`, then waits a short time once. Write it as `for` with an end, not `while True`. On desktop turtle, the same `update_*` functions can go into `screen.ontimer(tick, 33)`, which is the closest thing to Scratch's scheduler. Generators, `asyncio` and `threading` are "much later" topics.

## Mapping table

| Scratch pattern | Python pattern (Colab, ColabTurtlePlus) | Desktop turtle |
|---|---|---|
| Two sprites, each with `when green flag clicked` → `forever` | One `for frame in range(300):` loop that calls `update_cat()` and then `update_ghost()` | `def tick(): update_cat(); update_ghost(); screen.update(); screen.ontimer(tick, 33)`, then `tick(); screen.mainloop()` |
| One loop pass is one frame (about 30 fps) | One pass of the game loop; `time.sleep(0.03)` **once**, at the end of the loop | `ontimer(tick, 33)`; use `screen.tracer(0)` + `screen.update()` so all sprites draw together |
| `wait 1 seconds` inside one sprite's `forever` (other sprites keep moving) | **Don't sleep.** Keep a timer: `if time.time() >= next_beep: beep(); next_beep = time.time() + 1` (or count frames: `if frame % 30 == 0`) | Same, or a separate `screen.ontimer(beep, 1000)` chain |
| `wait 1 seconds` in a script nothing else is running alongside | `time.sleep(1)` is fine | `time.sleep(1)` is fine (the window freezes while it sleeps) |
| `repeat 10` / `glide 1 secs to x:` (animates over several frames) | A loop `for i in range(10): move(); sleep(0.03)`. This blocks all other sprites, so to animate everyone at once, put the step inside the game loop with a counter | Same idea, a counter inside `tick` |
| `when this sprite clicked` / `when key pressed` hats | Not available in ColabTurtlePlus (no events). Use `input()` between rounds, or skip | `screen.onkey(fn, "space")`, `turtle.onclick(fn)`, `screen.listen()` |
| `broadcast [game over]` | Call the function directly: `game_over()`; or set a flag `state = "game over"` that the loop checks | Same, or `ontimer(game_over, 0)` to run it "next frame" |
| `broadcast and wait` | A plain function call: Python already waits until the function returns | Same |
| `stop all` | `break` out of the game loop (or a `running = False` flag) | `running = False`, and stop scheduling `ontimer` |
| `stop this script` | `return` from that sprite's update, or a flag such as `cat_alive = False` | Same |
| Turbo Mode / "Run without screen refresh" | Remove the `sleep` / skip drawing for some frames; on desktop `tracer(0)` | `screen.tracer(0)` and call `update()` less often |
| Layer order decides who runs first | **You decide**: the order of the lines inside the loop | Same |
| Clones each running their own script | A list of dictionaries (or objects) plus `for c in clones: update_clone(c)` | Same |
| Many threads at once | Later, much later: generators (`yield` in Python is Scratch's yield), `asyncio`, `threading` (and turtle is not thread-safe) | Same |

### Tested example (text-only; run with `python3`)

Two Scratch scripts:
- Cat: `forever { move 10 steps; if on edge, bounce }`
- Ghost: `forever { next costume }`

```python
import time
cat = {"x": 0, "dx": 10}
ghost = {"x": 0, "costume": 1}

def update_cat():                 # one pass of the cat's forever loop
    cat["x"] += cat["dx"]
    if cat["x"] > 30 or cat["x"] < -30:
        cat["dx"] = -cat["dx"]    # "if on edge, bounce"

def update_ghost():               # one pass of the ghost's forever loop
    ghost["costume"] = 2 if ghost["costume"] == 1 else 1

for frame in range(8):            # "forever", but it ends, so Colab never freezes
    update_cat()
    update_ghost()
    print("frame", frame, "cat x =", cat["x"], "ghost costume =", ghost["costume"])
    time.sleep(0.03)              # ONE wait per frame, like Scratch's screen refresh
```

Output (verified): the cat goes 10, 20, 30, 40, then bounces back 30, 20, 10, 0, while the ghost switches costume 2, 1, 2, 1. It overshoots to 40 because it moves first and checks the edge afterwards, just like the Scratch script.

A non-blocking "wait" (tested): with `if now >= next_beep: ...; next_beep = now + 0.3` inside a 0.03 s loop, it beeps at 0.00, 0.33, 0.66, 0.99 and 1.30 s (frames 0, 10, 20, 30, 39) while the loop keeps running. In a Colab turtle version, `update_cat` would call `cat_turtle.forward(...)` and so on. Set ColabTurtlePlus to its fastest speed so each frame doesn't animate slowly; agent topics on ColabTurtlePlus cover the exact API.

Desktop version of the same loop:

```python
import turtle
screen = turtle.Screen(); screen.tracer(0)
cat_t = turtle.Turtle("turtle"); ghost_t = turtle.Turtle("circle")
running = True
def tick():
    update_cat(); update_ghost()
    cat_t.setx(cat["x"] * 5)
    ghost_t.color("white" if ghost["costume"] == 1 else "grey")
    screen.update()
    if running:
        screen.ontimer(tick, 33)      # about 30 fps, like Scratch
tick()
screen.mainloop()
```

## Gaps and gotchas (bugs kids will hit)

1. **`while True:` freezes Colab.** Scratch's `forever` is safe because it yields every frame and has a red stop sign. In Python, `while True` never gives control back. The cell keeps spinning, output may never show, and you have to press Stop (Interrupt). Teach `for frame in range(300):` first, and show the Stop button before anyone needs it.
2. **`time.sleep()` inside the loop slows *everything*.** In Scratch, `wait 1` in the cat's script pauses only the cat. In Python, `sleep(1)` pauses every sprite, because there is only one juggler. Use exactly one short sleep per frame and timers or frame-counters for waits. This is the biggest change in thinking.
3. **`repeat` or `glide` inside an update function blocks everyone else.** A `for i in range(10)` animation inside `update_cat()` finishes completely before the ghost moves even once. Each update should do **one small step**.
4. **Order of updates matters, and it's visible.** If `update_cat()` runs before `check_collision()`, a hit can be seen one frame early or late. If the player moves before the enemy, they may "slip past" each other. In Scratch this is hidden behind the layer order. In Python the line order is the run order, which is actually easier to reason about. Usual order: read input → move everything → check hits → draw.
5. **Drawing one sprite at a time looks flickery.** Scratch redraws the whole stage once per frame. Desktop turtle redraws after every move unless you use `tracer(0)` + `update()`. ColabTurtlePlus redraws the SVG as turtles move, so many turtles × many frames can be slow; keep the number of turtles and frames small.
6. **Broadcast races don't happen the same way.** In Scratch, broadcasting again restarts a handler that hasn't finished. In Python, `game_over()` runs straight through to the end and returns. Kids who used `broadcast` as "run this alongside" have to learn that a function call means "do this *now*, then come back".
7. **Turbo-mode habits.** Scratch loops that don't change the screen silently run many times per frame. In Python every loop runs as fast as the computer can, so a counting loop without a sleep finishes almost instantly. A loop of turtle moves without the right speed can either take ages or finish instantly.
8. **Variables shared between "scripts".** Inside a function, changing a global number needs `global score`; a dict or list (`cat["x"]`) avoids this. The `UnboundLocalError` is a common first wall.
9. **No events in ColabTurtlePlus.** Things like `when space key pressed` or `when this sprite clicked` have no direct Colab equivalent. Save them for desktop turtle, or use turn-based `input()` games.

## Teaching ideas for a 9-year-old

**Analogy: the juggler (or the plate spinner).** "Scratch has one juggler who gives each ball a tiny push and then moves on, super fast. In Python *you* are the juggler. Your loop is your hands going round: push the cat, push the ghost, look at the screen, again. If you stop to tie your shoe (`sleep(1)`), *every* ball falls." You can act it out: the child walks between two "sprites" (toys) and moves each one a step per "frame" while the parent counts frames.

**Mini-challenges**

1. **Two sprites, one loop.** Take the tested example. Add a third sprite, `update_bat()`, that moves up and down. Then swap the order of the update lines and see whether anything changes (it shouldn't, yet). Finally add `if cat["x"] == bat["y"]: print("Bonk!")` and try putting it *before* vs *after* the moves.
2. **The wait that doesn't stop the world.** Make the ghost change costume only every 10 frames (`if frame % 10 == 0`), while the cat still moves every frame. Bonus: try `time.sleep(1)` inside `update_ghost()` instead and describe what happens to the cat. This bug is the lesson.
3. **Broadcast = function call.** Rebuild a Scratch "game over" broadcast. When `frame == 50`, call `game_over()`, which prints a message, and then `break`. Then try a "scene" variable (`scene = "title"` → `"play"` → `"end"`) that the loop checks with `if/elif`. That's how one loop replaces many broadcasts.

**Sequence:** first a `for` loop that moves one turtle, then two sprites in one loop (text first, then turtles), then timers with `frame %`, then a scene variable. Desktop `ontimer` + `onkey` comes last, as "the version where the keyboard works".

## Sources

- scratch-vm sequencer (`stepThreads`, `WORK_TIME = 0.75 * currentStepTime`, redraw/turbo check, thread order): https://github.com/scratchfoundation/scratch-vm/blob/develop/src/engine/sequencer.js
- scratch-vm runtime (`THREAD_STEP_INTERVAL` 1000/60, `THREAD_STEP_INTERVAL_COMPATIBILITY` 1000/30, `startHats` reverse `executableTargets` order sharing drawable order, `restartExistingThreads` / `_restartThread`): https://github.com/scratchfoundation/scratch-vm/blob/develop/src/engine/runtime.js
- Scratch Wiki, Turbo Mode (loops run several iterations per frame, like "Run without screen refresh"): https://en.scratch-wiki.info/wiki/Turbo_Mode
- Scratch Wiki, Frame Rate (30 fps): https://en.scratch-wiki.info/wiki/Frame_Rate
- Scratch Wiki, Broadcast (restart behaviour, broadcast and wait): https://en.scratch-wiki.info/wiki/Broadcast
- Python `turtle` docs (`ontimer`, `tracer`, `update`, `onkey`, `mainloop`): https://docs.python.org/3/library/turtle.html
- ColabTurtlePlus (no event loop or timers in Colab): https://github.com/mathriddle/ColabTurtlePlus

Note: the Scratch Wiki "Thread" page turned out to be about forum threads, and "Execution Order" returned 404. The execution-order facts above come straight from the scratch-vm source. The Frame Rate and Broadcast wiki pages are given as reading links; I did not fetch them in this session.
