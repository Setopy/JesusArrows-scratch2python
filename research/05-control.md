# 05 Control blocks (excluding clones)

Dimension: Scratch 3.0 Control category (`wait`, `repeat`, `forever`, `if then`, `if then else`, `wait until`, `repeat until`, `stop`). Clone blocks (`when I start as a clone`, `create clone of`, `delete this clone`) are covered by another agent.

## Summary

- **Colour.** Control blocks are amber/orange. scratch-gui's default theme sets `control` to primary `#FFAB19`, secondary `#EC9C13` and tertiary `#CF8B17`. The Scratch Wiki calls them "amber".
- **Shapes.** Five of the eight blocks are **C blocks**: `repeat`, `forever`, `if then`, `if then else` and `repeat until`. Two are **stack blocks**: `wait`, `wait until`. `stop` is a **cap block** for "all" and "this script". It turns into a stack block for "other scripts in sprite", and it is the only Scratch block that changes shape. `forever` is a C block with a cap bottom, so nothing can snap under it.
- **The big idea for the child: the mouth of the C is Python's indentation.** In Python, a line ending in `:` opens the mouth. Every line indented by 4 spaces under it is inside the C. The first line that goes back to the left margin is the block snapped *under* the C.
- **The biggest behaviour difference: Scratch loops share the stage, Python loops do not.** In scratch-vm, each pass of a loop waits for the next screen frame (about 1/30 s) when other scripts need a turn, so many scripts appear to run at once. A Python `while True:` runs only itself. Everything else waits, and in Colab the cell keeps spinning until you press the **Interrupt / Stop** button.
- **Mapping in one line each:**
  - `wait` → `time.sleep()`
  - `repeat` → `for i in range(n):`
  - `forever` → `while True:`
  - `if then` / `if then else` → `if` / `else`. Python adds `elif`, which Scratch does not have.
  - `wait until` → `while not cond: time.sleep(0.01)`
  - `repeat until` → `while not cond:`
  - `stop` → `break`, `return`, or `sys.exit()` / `raise SystemExit`, depending on which option is chosen.

## Block-by-block mapping table

All Python snippets were run with `python3` 3.13.5 on macOS (output checked; see "Tests run" below).

| Scratch block (exact text, shape) | What it does in Scratch | Python equivalent | Gaps and notes |
|---|---|---|---|
| `wait (1) seconds` (stack) | Pauses this script only. Other scripts keep running. Negative values become 0 (`Math.max(0, 1000*DURATION)` in scratch-vm). It always yields at least one frame, even `wait (0)`. | `import time` then `time.sleep(1)` | `time.sleep(-1)` raises `ValueError: sleep length must be non-negative`. `sleep` pauses the **whole program**, not one script. In ColabTurtlePlus, the turtle's own `speed()` animation already adds delays. |
| `repeat (10)` (C) | Runs the mouth 10 times. The input is rounded with JS `Math.round` (2.5 → 3, 2.4 → 2). Zero, negative or non-numeric input runs 0 times. Infinity runs forever. Each pass waits for the next frame if other scripts need to yield. | `for i in range(10):` + indented body | `range(2.5)` raises `TypeError: 'float' object cannot be interpreted as an integer`. Python's `round(2.5)` is **2** (round half to even), while Scratch gives **3**; `math.floor(x + 0.5)` matches Scratch for positive numbers. `range(-1)` safely runs 0 times. Python's `i` counts 0..9, and Scratch has no visible counter (kids make a variable). |
| `forever` (C with cap bottom) | Repeats the mouth until the green flag or stop sign, or a `stop` block. Nothing can attach below. Yields a frame each pass. | `while True:` + indented body | Python never yields to anything else. With no `sleep`, the cell freezes or spins at 100% CPU. In Colab you must press the **Interrupt** button (or Runtime → Interrupt execution), which raises `KeyboardInterrupt`. Code after the loop *can* be written in Python (it is not a cap), but it only runs if the loop `break`s. For animation, put `time.sleep(0.03)` inside to imitate Scratch's 30 FPS. |
| `if <> then` (C) | Runs the mouth once if the condition is true. Not a loop: it checks only once, at the moment the script reaches it. | `if cond:` + indented body | The classic Scratch bug of an `if` outside a `forever` that checks only once happens in Python too. Comparison operators are covered by the Operators agent. |
| `if <> then / else` (E-shaped, two mouths) | Runs the first mouth if true, otherwise the second. | `if cond:` … `else:` … | `else:` must line up with `if` (same indent), and both need a colon. **Python has `elif`; Scratch does not.** In Scratch, "else if" is an `if/else` nested inside the `else` mouth, which piles up indentation. `elif` flattens it. |
| `wait until <>` (stack) | Pauses this script, checking the condition once every frame until it is true. | `while not cond:` with `time.sleep(0.01)` as the indented body | `while not cond: pass` works but burns CPU. The deeper gap is that in Python nothing else is running to *make* the condition true (no other scripts), so it can wait forever. It is useful with time (`time.time()`), threads or `input()`. Colab has no live keyboard or mouse sensing for ColabTurtlePlus, so "wait until key pressed" becomes `input("Press Enter")`. |
| `repeat until <>` (C) | Checks the condition *before* each pass, then runs the mouth while it is false and stops once it is true. Yields each pass. | `while not cond:` + indented body | The logic is flipped: Scratch says "until", Python's `while` says "as long as". Teach `while not (...)` first, then simplify (`until x > 4` = `while x <= 4`). Scratch 3 also has a hidden `while` block (`control_repeat_while`) in the VM, but it is not in the palette. |
| `stop [all]` (cap) | Same as clicking the red stop sign. Stops every script in every sprite. | `sys.exit()` or `raise SystemExit` | In a plain `python3` script it ends the program (tested). In Colab it raises `SystemExit` and prints a warning, but the notebook kernel stays alive, so later cells still run. With desktop turtle, `turtle.bye()` closes the window. |
| `stop [this script]` (cap) | Ends only this script. Inside a custom block, it ends the custom block and the caller carries on. | Inside a loop: `break` (leaves only the innermost loop). Inside a function: `return`. | `break` is the closest kid-level match for "stop this loop". `return` matches "stop this script" when the script is written as a function (this pairs with the My Blocks agent: a custom block = `def`). At the top level of a cell there is no "this script", so you use `break` or restructure. |
| `stop [other scripts in sprite]` (stack) | Stops this sprite's other scripts and keeps going. On the Stage it reads "other scripts in stage". | No direct equivalent. Python runs one script at a time. | It only means something if you have built "several scripts" with threads (`threading.Event` as a stop flag; tested) or with turtle `ontimer` callbacks (stop by not rescheduling). It is too advanced for a 9-year-old: just say "Python has only one script running, so there is nothing else to stop." |

### Indentation = the C-shape mouth (tested)

```python
for i in range(2):      # top of the C: line ends with a colon
    print("inside")     # 4 spaces = inside the mouth
print("after")          # back at the margin = snapped UNDER the C
```
Output: `inside`, `inside`, `after`.

Nested C blocks = more indentation:
```python
for side in range(4):          # repeat 4
    forward(100)               #     move
    for blink in range(2):     #     repeat 2   (C inside a C)
        print("blink")         #         8 spaces = inside both
    right(90)                  #     back to the outer mouth
```

### The common errors (exact messages from Python 3.13)

```python
for i in range(3):
print("hi")
```
`IndentationError: expected an indented block after 'for' statement on line 1`. You can read it as "the C has an empty mouth": nothing is inside.

```python
if True:
    print("a")
      print("b")
```
`IndentationError: unexpected indent`. This block is pushed in further than the others, as if it were floating loose.

```python
for i in range(3)
    print("hi")
```
`SyntaxError: expected ':'`. The colon is what opens the mouth.

Other gotchas to warn about: mixing tabs and spaces (Colab's editor inserts spaces by default, which is good). Putting a line at the wrong indent level gives **no error**, the program just does something different. This is the Python version of dropping a block below the C instead of inside it.

## Gaps and gotchas

1. **Concurrency (most important).** In Scratch, each green-flag script is its own thread. The VM switches between them every frame, and loops yield each pass (scratch-vm `startBranch(1, true)`). Python runs top to bottom, one thing at a time. Two Scratch `forever` scripts (for example "move" and "change colour") must become **one** Python loop that does both steps. Teach "merge your forevers".
2. **Frozen notebook.** `while True:` with no `break` never finishes. In Colab the cell spinner keeps going and later cells queue up. Use the Interrupt button. With ColabTurtlePlus, the drawing may only appear in pieces or not at all until the cell ends. Prefer `for i in range(200):` over `while True:` for drawings.
3. **Desktop turtle.** A `while True:` loop works (`turtle.update()` / normal drawing keeps the window repainting), but clicks and keys are ignored unless you use `screen.ontimer(func, 33)` with event handlers. That is the closest true analogue of `forever` sharing time with "when key pressed". Closing the window mid-loop raises `turtle.Terminator`.
4. **Rounding differs.** Scratch `repeat (2.5)` runs 3 times. Python `range(2.5)` is an error and `round(2.5)` is 2. Use `int(...)` or `math.floor(x + 0.5)`.
5. **No `elif` block in Scratch.** Kids nest `if/else` in Scratch. Show them `elif` as a shortcut. Also, Python checks `if`/`elif` branches in order and runs only the first true one.
6. **"Until" vs "while" flip.** `repeat until x > 4` → `while not (x > 4):` or `while x <= 4:`. An off-by-one here is the classic bug.
7. **`wait until` busy-waiting.** Always put `time.sleep(0.01)` in the body. Without it, the loop runs flat out at 100% CPU.
8. **`stop` has three Python meanings.** `break` (stop this loop), `return` (stop this function/script) and `sys.exit()` (stop everything). `break` inside nested loops only leaves the innermost loop.
9. **`forever` is a cap block in Scratch, not in Python.** Python lets you write code after `while True:`. It silently never runs unless there is a `break`.
10. **`if` checks once.** This is the same in both languages, but kids rediscover it. A collision check needs to sit inside the loop.

## Teaching ideas for a 9-year-old

**Analogy: the C block is a sandwich and indentation is the filling.** The `for ...:` line is the top slice of bread and the colon is the bite mark that says "filling goes here". Every indented line is filling. The first line back at the left edge is the plate under the sandwich, not part of it. Alternative: the C-mouth "eats" indented lines. If you forget to indent, the mouth is empty and Python complains: "expected an indented block!"

**Mini-challenges (all work in Colab with ColabTurtlePlus):**

1. **Square to star (repeat).** Convert the Scratch script `repeat 4: move 100, turn 90` to `for i in range(4):`. Then change only two numbers to draw a 5-point star (`range(5)`, `right(144)`). Bonus: nest it inside `for j in range(6):` with `right(60)` to make a flower. Indentation shows which C is which.
2. **Countdown rocket (repeat until + wait).** `n = 10`, then `while not (n == 0): print(n); time.sleep(1); n = n - 1`, then `print("Blast off!")` *after* the loop (outdented). Predict first: what happens if `print("Blast off!")` is indented? And what if you forget `n = n - 1`? (That makes a forever loop, so practise pressing the Interrupt button.)
3. **Hot or cold (if / elif / else + stop).** `secret = 7`, then `while True:`, read a guess with `guess = int(input("Guess: "))`, and use `if guess == secret: print("You got it!"); break`, `elif guess < secret: print("Too low")` and `else: print("Too high")`. Ask: "In Scratch, how many `if/else` blocks would this need?" (Nested ones.) `break` is Python's `stop this script`.

## Tests run

All of the above was run with `python3` 3.13.5: `time.sleep`, `range` counts, `round(2.5)` = 2 vs `math.floor(2.5 + 0.5)` = 3, `while True` + `break`, `if/elif/else`, timed `wait until`, `repeat until` (`x` ends at 5 for `until x > 4`), `return` ending a function early, `sys.exit()` and `raise SystemExit` (later lines not run), a `threading.Event` stop flag, `range(2.5)` TypeError, `time.sleep(-1)` ValueError, and the three indentation/colon error messages quoted above. Colab-specific behaviour (Interrupt button, `SystemExit` warning without the kernel dying) comes from standard IPython behaviour and was not run in Colab itself.

## Sources

- Scratch Wiki, Control Blocks: https://en.scratch-wiki.info/wiki/Control_Blocks
- Scratch Wiki, Forever (block): https://en.scratch-wiki.info/wiki/Forever_(block)
- Scratch Wiki, Repeat () (block): https://en.scratch-wiki.info/wiki/Repeat_()_(block)
- Scratch Wiki, Stop () (block): https://en.scratch-wiki.info/wiki/Stop_()_(block)
- Scratch Wiki, C Block: https://en.scratch-wiki.info/wiki/C_Block
- Scratch Wiki, Cap Block: https://en.scratch-wiki.info/wiki/Cap_Block
- scratch-vm Control implementation (`Math.round` in repeat, `startBranch(1, true)` loop yielding, wait clamping, stop options): https://github.com/scratchfoundation/scratch-vm/blob/develop/src/blocks/scratch3_control.js
- scratch-gui default theme colours (`control` #FFAB19 / #EC9C13 / #CF8B17): https://github.com/scratchfoundation/scratch-gui/blob/develop/src/lib/themes/default/index.js
- Python docs, compound statements (`if`/`while`/`for`, indentation): https://docs.python.org/3/reference/compound_stmts.html
- Python docs, `time.sleep`: https://docs.python.org/3/library/time.html#time.sleep
- Python docs, `sys.exit`: https://docs.python.org/3/library/sys.html#sys.exit
- Python docs, `turtle` (`ontimer`, `bye`): https://docs.python.org/3/library/turtle.html
