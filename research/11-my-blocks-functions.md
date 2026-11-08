# 11. My Blocks to functions

## Summary

The pink **My Blocks** category is Scratch's version of functions. A `define` hat block holds the instructions, and the matching pink stack block calls them. Python's `def` works the same way: you name some steps once, then call them by name as often as you like. Most of what the child knows carries straight over:

- the `define` block becomes `def name(...):`
- the inputs (number or text inputs, boolean inputs) become **parameters**
- the label text becomes the function name, or good parameter names
- calling the block becomes `name(...)`, written with parentheses

Python adds three things Scratch lacks:

1. **`return`.** A function can hand back a value, like a home-made reporter block. Scratch has no custom reporters or booleans, so Scratchers fake a return by setting a global variable or adding to a list (Scratch Wiki: My Blocks; Recursion).
2. **Sharing.** Scratch custom blocks are **sprite-local**: they show up only in the sprite that made them, and you move them between sprites or projects by dragging them or using the Backpack. A Python function in a notebook can be used anywhere in that notebook. Saving functions in a `.py` file and using `import` is Python's Backpack.
3. **Real recursion that returns values**, plus default values, docstrings and keyword arguments.

Scratch's "Run without screen refresh" checkbox in the Make a Block dialog draws everything at once. In ColabTurtlePlus the closest match is **`speed(0)` followed by `done()`** at the end, which shows only the final picture. Two milder options are `speed(13)` (fastest animation) and `animationOff()` / `animationOn()` (moves jump but you still see them).

All logic snippets below were tested with Python 3.13.5 (output shown). The turtle snippets need Colab plus ColabTurtlePlus and were not run here.

## Block-by-block mapping table

| Scratch (pink My Blocks) | Python | Notes / tested output |
|---|---|---|
| **Make a Block** button, then `define [jump]` | `def jump():` then indented body | The colon and the indent matter: the indent is the "inside the hat". |
| Calling `jump` (the pink stack block) | `jump()` | You **must** write `()`. Writing `jump` on its own silently does nothing. |
| `define jump (height)` with a number/text input | `def jump(height):` | Scratch 3 merged its number and text inputs into one. Python parameters have no type either, so `"3"` and `3` are different values (see gotchas). |
| Several inputs: `define greet (name) (times)` | `def greet(name, times):` / `greet("Ada", 2)` | Prints `Hi Ada` twice. Arguments match up **by position**. |
| Boolean input (hexagon): `define say (name) loud? <shout>` | `def say_hello(name, shout):` with `if shout:` | `say_hello("ada", True)` gives `ADA!!!`. In Python `True`/`False` start with a capital letter. |
| Label text between inputs (`move (n) steps then say (msg)`) | Put the words in the name: `move_then_say(n, msg)`, or call with keywords: `jump(height=5)` | Keyword arguments read almost like Scratch labels. |
| Default input value (Scratch has none; the slot is just blank) | `def jump(height=10):` so `jump()` uses 10 | Tested: `jump()` prints `jump 10` and `jump(50)` prints `jump 50`. Defaults must come **after** the inputs that have none. |
| Input reporter dragged out of the define hat | Use the parameter name inside the body | Outside the definition, Scratch reports `0`. In Python the parameter name does not exist outside the function. |
| Faking a reporter: `set [answer] to (n * 2)` inside the block, then read `answer` | `def double(n): return n * 2` and `print(double(double(3)))` | Prints `12`. The `global answer` style also works (prints `8`) but `return` is the clean way. |
| Custom boolean (not possible in Scratch) | `def is_even(n): return n % 2 == 0` | `is_even(4), is_even(7)` gives `True False`. You can then write `if is_even(x):`. |
| `stop [this script]` inside a custom block | `return` (with no value) | Ends the function early. The caller keeps going. |
| Run without screen refresh (checkbox) | ColabTurtlePlus `speed(0)` ... `done()`; or `speed(13)`; or `animationOff()` / `animationOn()` | `speed(0)` "draws only the final image" and needs `done()` at the end (ColabTurtlePlus docs). The standard turtle library's `tracer(0)` / `update()` is **not** listed in the ColabTurtlePlus docs, so don't teach it for Colab. |
| Turbo Mode (project-wide) | `speed(13)` at the top of the program | |
| Recursion: a block that calls itself | `def countdown(n): if n == 0: ...; return` then `countdown(n - 1)` | Prints `3 2 1 Blast off!`. |
| Recursive factorial (Scratch uses a list as a stack) | `def factorial(n): return 1 if n <= 1 else n * factorial(n - 1)` | `factorial(5)` is `120`. No list stack needed, because `return` carries the value back. |
| Recursive tree with pen (needs run without screen refresh) | See turtle tree below | |
| Right-click > Edit | Edit the `def` cell and **re-run it** | In Colab, a change to a function only takes effect after you run its cell again. |
| Comment on the define block | Docstring: `"""Make the sprite jump."""` as the first line | `help(jump)` prints the docstring. |
| Backpack / drag a script to another sprite | Save the functions in `myblocks.py`, then `import myblocks` and call `myblocks.star(5)`, or write `from myblocks import star` | Tested: both forms work. In Colab, upload the file or write it with `%%writefile myblocks.py`. |
| Sprite-local blocks | Functions are shared by the whole notebook | Closer to "every sprite can see it". |

### Turtle tree (Colab, ColabTurtlePlus; not run here)

```python
from ColabTurtlePlus.Turtle import *
clearscreen()
speed(0)            # "run without screen refresh": draw only the final picture
left(90)            # point up, like Scratch "point in direction 0"

def tree(length, levels):
    """Draw a tree. Each branch grows two smaller trees."""
    if levels == 0:          # base case: stop growing
        return
    forward(length)
    left(30)
    tree(length * 0.7, levels - 1)
    right(60)
    tree(length * 0.7, levels - 1)
    left(30)
    back(length)             # go back so the turtle ends where it started

tree(80, 6)
done()              # required with speed(0)
```

The `back(length)` line at the end is the key idea: every branch must leave the turtle exactly where it found it. Scratch fractal projects need the same trick.

## Gaps and gotchas

Every error message below was produced by running the code.

1. **Calling before defining.** `dance()` placed above `def dance():` gives `NameError: name 'dance' is not defined`. Scratch lets the define hat sit anywhere in the code area, but Python reads from top to bottom. In Colab, the `def` cell must be **run** before the cell that calls it.
2. **Forgetting the parentheses.** A line with just `jump` runs with no error and does nothing. `print(jump)` shows `<function jump at 0x...>`. This is the sneakiest mistake.
3. **Missing or extra argument.** `greet()` gives `TypeError: greet() missing 1 required positional argument: 'name'`, and `greet("a","b")` gives `TypeError: greet() takes 1 positional argument but 2 were given`. Scratch never complains, because an empty slot just counts as blank or 0.
4. **Forgetting the colon or the indent.** You get `SyntaxError: expected ':'` or `IndentationError: expected an indented block after function definition`.
5. **Text versus number.** Scratch 3 merged number and text inputs and converts between them automatically. Python does not:
   - `add("2","3")` gives `23`, while `add(2,3)` gives `5`
   - `"x" * "3"` gives `TypeError: can't multiply sequence by non-int`
   - `input()` always returns text, so wrap it in `int(...)`
6. **`print` is not `return`.** A function with no `return` hands back `None`. Tested: `print(no_return(3))` prints `None`. Children often print inside the function and then wonder why `x = double(3)` is empty.
7. **Parameters are local copies.** Changing `x` inside `f(x)` does not change the `x` outside (tested: it stays `1`). This is like Scratch block inputs, which you can't `set` either. To change an outside variable you need `global`, but `return` is the better habit to teach.
8. **Runaway recursion.** A function that calls itself with no base case stops with `RecursionError: maximum recursion depth exceeded`, at Python's default limit of 1000 calls. In Scratch the same mistake freezes or crashes the project. Python's error is friendlier, but teach "always write the stop case first".
9. **Run without screen refresh has no exact match.** Scratch's checkbox applies to one block, and Scratch can freeze when that block has a `wait` or a forever loop (it caps the time at about 500 ms). In ColabTurtlePlus, `speed(0)` applies to the **whole drawing** and needs `done()` at the end, or the picture never appears.
10. **Defaults must come last.** `def f(a=1, b):` gives `SyntaxError: parameter without a default follows parameter with a default`.
11. **Scratch scoping trivia.** An early Scratch 3.0 bug let a called block see its caller's inputs. It has been fixed. Python never worked that way, because each call gets its own parameters.

## Teaching ideas for a 9-year-old

**Analogy: a recipe card, or a super-block.** "A `def` is a recipe card you write once and pin to the fridge. The name at the top is the recipe's name, and the parameters are the blanks: *how many* eggs, *which* topping. Calling `pancakes(3, "honey")` is asking someone to follow the card with those blanks filled in. In Scratch, the card could only make the food. In Python, the card can also *hand you back* the result, and that is `return`. Python functions are Scratch's pink blocks with a superpower: they can be reporters too."

You can make this concrete: put the Scratch `define` hat and the Python `def` side by side and colour the Python keyword pink.

**Mini-challenges**

1. **Shape machine (parameters and defaults).** Write `def polygon(sides, size=50):` that draws any regular shape with `forward(size)` and `right(360 / sides)`. Then call `polygon(3)`, `polygon(6, 30)` and `polygon(sides=8)`. Bonus: add a boolean `filled` parameter that uses `begin_fill()` and `end_fill()`.
2. **Reporter you couldn't build in Scratch (`return`).** Write `def double(n):` and `def is_even(n):`. Use them together: `if is_even(double(7)): print("even!")`. Then rebuild the same thing in Scratch with a global variable, and compare how many blocks each version needs.
3. **Grow a tree (recursion and screen refresh).** Run the tree code. First try it with `speed(13)` and watch it grow, then with `speed(0)` and `done()`. Change `levels` from 3 to 7 and change the angle. Ask the child: "What happens if you delete the `if levels == 0` line?" (Python stops with a RecursionError.)

**Debugging game.** Show the three broken calls (`dance()` placed above its `def`, a bare `jump`, and `greet()` with no name). Have the child predict and read each error message, which makes red error text something to read rather than fear.

## Sources

- Scratch Wiki, My Blocks: https://en.scratch-wiki.info/wiki/My_Blocks
- Scratch Wiki, Run Without Screen Refresh: https://en.scratch-wiki.info/wiki/Run_Without_Screen_Refresh
- Scratch Wiki, Recursion: https://en.scratch-wiki.info/wiki/Recursion
- Scratch Wiki, Custom Blocks / Define (): https://en.scratch-wiki.info/wiki/Custom_Blocks , https://en.scratch-wiki.info/wiki/Define_()_(block) (related pages; key facts taken from the My Blocks page)
- ColabTurtlePlus on PyPI (speed 0 to 13, `animationOff`/`animationOn`, `done()`): https://pypi.org/project/ColabTurtlePlus/
- Python tutorial, Defining Functions: https://docs.python.org/3/tutorial/controlflow.html#defining-functions
- Python tutorial, Modules: https://docs.python.org/3/tutorial/modules.html
