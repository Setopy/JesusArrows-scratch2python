# 09 Variables, data types and scope

## Summary

Scratch's orange Variables blocks map almost one-to-one onto Python assignment: `set [score] to (0)` is `score = 0`, and `change [score] by (1)` is `score += 1`. The hard parts are the things Scratch hides from the child:

1. **Typing.** Scratch is loosely typed. A value is "a number or a string" and Scratch converts silently: `"10" + 5` gives 15, `"abc" + 1` gives 1 (the text counts as 0), and `"A" = "a"` is true. Python is strict. `"score: " + 5` is a `TypeError`, `"10" + "5"` is `"105"`, and `"A" == "a"` is `False`. `input()` always returns a `str`, so `int()` is needed before doing maths. This is the most common beginner trap.
2. **Scope.** "For all sprites" is a module-level (global) variable. "For this sprite only" fits best as an object attribute (`cat.health`). The catch is that a function can *read* a global but cannot *change* it without `global name`, or Python raises `UnboundLocalError`. Scratch has no equivalent of this rule.
3. **Monitors.** Python has no on-stage monitor. `print(f"score: {score}")` is the "show variable" equivalent. In Colab, putting a bare variable name on the last line of a cell also displays its value.
4. **Names.** Scratch allows spaces, leading digits and any case pattern (`my score`, `2nd place`). Python names cannot contain spaces, cannot start with a digit, cannot be keywords (`for`, `if`, `class`...), and are case-sensitive. `Score` and `score` are two different variables.
5. **Cloud variables** (numbers only, at most 256 digits, at most 10 per project, not for New Scratchers) have no direct Python match. The closest beginner idea is saving to a JSON file. In Colab that file disappears when the runtime resets unless it is saved to Drive.

All snippets below were tested with `python3` (3.13.5; Colab runs 3.12, which gives the same messages, including the "Did you mean" hints).

## Block-by-block mapping table

| Scratch block / feature | Python | Notes (tested) |
|---|---|---|
| Make a Variable → `score` | `score = 0` (created by first assignment) | Scratch creates a variable with a button and gives it a starting value of 0. Python has no "make" step: the first `=` creates it. Using a name before assigning it gives `NameError`. |
| `set [score] to (0)` | `score = 0` | `=` means "put into the box", not "equals". |
| `set [name] to (Ada)` | `name = "Ada"` | Text needs quotes. Without them Python looks for a variable called `Ada`. |
| `change [score] by (1)` | `score += 1` (same as `score = score + 1`) | `score -= 2` for negative changes. Scratch's `change by` on a text value treats the text as 0. Python raises `TypeError` instead. |
| `change [score] by (-1)` | `score -= 1` | |
| `(score)` reporter | `score` | Use the name anywhere a value goes. |
| `show variable [score]` / monitor | `print("score:", score)` or `print(f"score: {score}")` | A print shows a snapshot, not a live monitor. Large readout ≈ `print(score)`. Colab: a bare `score` on the last line of a cell shows the value. |
| `hide variable [score]` | (stop printing it) | There is nothing to hide. Output only appears when you print it. |
| Slider monitor (default range 0 to 100) | `score = int(input("score? "))` or Colab form `score = 50  # @param {type:"slider", min:0, max:100}` | The Colab `@param` slider is the closest match to a Scratch slider. |
| "For all sprites" (global) | Variable at the top level of the notebook/file | Readable inside any function. To *change* it inside a function you need `global score`. |
| "For this sprite only" (local) | Object attribute: `cat.health`, `dog.health` | Each object has its own copy, like each sprite (and each clone) in Scratch. A function's own local variables are a *different* idea: they are temporary and vanish when the function ends. |
| `[health] of [Cat]` (sensing) | `cat.health` | Dot notation reads another object's attribute. |
| Cloud variable ☁ | `json.dump` / `json.load` to a file | Scratch cloud variables hold numbers only, at most 256 digits, at most 10 per project, update at most 10 times a second, and are public. A file is private and local. |
| Number vs text (implicit) | `int`, `float`, `str`, `bool`; check with `type(x)` | `type(5)` gives `<class 'int'>`, `type(2.5)` gives `float`, `type("5")` gives `str`, `type(True)` gives `bool`. |
| `join (score: ) (score)` | `"score: " + str(score)` or `f"score: {score}"` | f-strings are the friendliest option for kids. |
| `(answer)` after `ask` | `answer = input("...")` → `int(answer)` | `input()` is always text. |
| `"A" = "a"` (true in Scratch) | `"A".lower() == "a".lower()` | In Python `"A" == "a"` is `False`. |

### Tested core snippet

```python
score = 0
score = score + 10      # set score to (score + 10)
score += 1              # change score by 1
score -= 2              # change score by -2
print(score)            # 9
print(f"score: {score}")  # score: 9   (the "monitor")

print(type(5), type(2.5), type("5"), type(True))
print(int("42") + 1, str(7) + "!", float("3.5"))   # 43 7! 3.5
print("10" + "5", 10 + 5, "ha" * 3)                # 105 15 hahaha
```

### For all sprites vs for this sprite only

```python
lives = 3                 # "for all sprites"

def lose_life():
    global lives          # "I mean the shared one!"
    lives -= 1

def show_lives():
    print("lives is", lives)   # reading needs no 'global'

lose_life()
show_lives()              # lives is 2

class Sprite:
    def __init__(self, name):
        self.name = name
        self.health = 100     # "for this sprite only"

cat = Sprite("Cat")
dog = Sprite("Dog")
cat.health -= 30
print(cat.health, dog.health)   # 70 100
```

(Classes may come later in the workbook. Until then, a dictionary per sprite works: `cat = {"health": 100}` and `cat["health"] -= 30`.)

### Cloud variable → file

```python
import json
with open("save.json", "w") as f:
    json.dump({"high_score": score}, f)
with open("save.json") as f:
    print(json.load(f)["high_score"])   # 9
```

## Gaps and gotchas (all tested; error text from Python 3.13)

| Mistake | Error | Fix / how to explain it |
|---|---|---|
| Typo: `scor = 0` then `print(score)` | `NameError: name 'score' is not defined. Did you mean: 'scor'?` | Python only knows names you have put in a box. Read the "Did you mean" hint. |
| Case: `Score = 1` then `print(score)` | `NameError: ... Did you mean: 'Score'?` | Capital letters count. Scratch also treats `Score` and `score` as different variables, but kids rarely notice. |
| `"score: " + 5` | `TypeError: can only concatenate str (not "int") to str` | Use `f"score: {score}"`, `str(score)`, or `print("score:", score)`. Scratch's `join` converts silently. |
| `age = input()` then `age + 1` | the same `TypeError` | `input()` gives text. Use `int(input())`. |
| `int("abc")` | `ValueError: invalid literal for int() with base 10: 'abc'` | Scratch would quietly use 0. Python refuses. |
| Changing a global in a function without `global` | `UnboundLocalError: cannot access local variable 'lives' where it is not associated with a value` | Inside a function, `lives -= 1` makes a brand-new local `lives` that is empty. Add `global lives`, or (better later) `return` the new value. |
| `my score = 5` | `SyntaxError: invalid syntax` | No spaces: use `my_score`. |
| `2score = 1` | `SyntaxError: invalid decimal literal` | Names can't start with a digit: `score2`. |
| `for = 3` | `SyntaxError: invalid syntax` | Keywords are reserved. `import keyword; keyword.kwlist` lists them. |
| `"A" == "a"` | `False` (no error) | Scratch's `=` ignores case. Python's `==` does not. |
| `"10" + "5"` | `"105"` (no error) | Text plus text sticks the pieces together. Scratch would give 15. |
| `round(2.5)` | `2` | Python rounds halves to the nearest even number. Scratch's `round` gives 3. `int(3.9)` gives 3 (it chops off the decimal part). |
| `=` vs `==` | `if score = 5:` is a `SyntaxError` | `=` puts a value in a box. `==` asks whether two values are equal (Scratch's green `=`). |
| Colab-specific | (none) | Variables live on across cells. Running cells out of order can leave old values. Runtime → Restart clears all the boxes, which is like pressing the green flag with no `set` blocks. Files written by `json.dump` are lost when the runtime resets unless saved to Drive. |

Optional helper if a lesson wants to imitate Scratch's forgiving maths (tested: `to_num("abc") + 1` gives `1`):

```python
def to_num(v):
    try:
        return float(v)
    except (ValueError, TypeError):
        return 0
```

## Teaching ideas for a 9-year-old

**Analogy: the labelled box.** A variable is a box with a name label on it. `score = 0` means "put 0 in the box labelled score". Each box holds one thing at a time, and putting a new thing in throws the old one out. `score += 1` means "take out what's there, add 1, put it back". Python is picky about the label: it must be one word (use `_` for spaces), it can't start with a number, and `Score` is a different box from `score`. The **type** is what kind of thing is in the box: a number box (`int`), a decimal box (`float`), a words box (`str`), or a yes/no box (`bool`). Python won't glue a number onto words until you turn the number into words with `str()`. "For all sprites" is a box on the classroom shelf that everyone shares. "For this sprite only" is a box in each sprite's own backpack (`cat.health`). To change the shelf box from inside a function, you must say `global` ("I mean the shelf one!").

**Mini-challenge 1: Coin collector (set and change).**
Start `coins = 0`. Add 5, add 3, lose 2, and print `f"You have {coins} coins"` after each step. Bonus: predict each number before running the cell.

**Mini-challenge 2: Fix the robot's bugs (errors as puzzles).**
Give a cell with three planted bugs: `my score = 0`, `print("Score: " + score)`, and `Score += 1`. The child reads each red error message, says which Scratch rule Python is stricter about, and fixes it. Make it a game: each fixed bug earns a "bug badge".

**Mini-challenge 3: Two sprites, one shared timer (scope).**
Make `timer = 10` (shared) and two dictionaries or objects, `cat = {"health": 100}` and `dog = {"health": 100}`. Write `def tick():` that lowers the timer (needs `global timer`) and `def hurt(sprite):` that takes 10 health from one sprite. Run `tick()` twice and `hurt(cat)` once, then print everything. Ask: why did the dog not lose health? Extra: remove `global` and look at the `UnboundLocalError`.

(Optional fourth: "High-score saver". Write the best score to `save.json`, restart the runtime, and load it back. This is the cloud-variable idea.)

## Sources

- Scratch Wiki, Variable: https://en.scratch-wiki.info/wiki/Variable
- Scratch Wiki, Set () to () (block): https://en.scratch-wiki.info/wiki/Set_()_to_()_(block)
- Scratch Wiki, Change () by () (block): https://en.scratch-wiki.info/wiki/Change_()_by_()_(block) ("the string is casted to 0")
- Scratch Wiki, Local Variable: https://en.scratch-wiki.info/wiki/Local_Variable (clones inherit and keep their own copies)
- Scratch Wiki, Global Variable: https://en.scratch-wiki.info/wiki/Global_Variable
- Scratch Wiki, Cloud Data: https://en.scratch-wiki.info/wiki/Cloud_Data (numbers only, 256 digits, 10 per project, 10 updates a second, no New Scratchers)
- Scratch Wiki, Variable Monitor: https://en.scratch-wiki.info/wiki/Variable_Monitor (normal, large and slider modes)
- Python docs, Names and identifiers / keywords: https://docs.python.org/3/reference/lexical_analysis.html#identifiers
- Python docs, the `global` statement: https://docs.python.org/3/reference/simple_stmts.html#the-global-statement
- Python FAQ, why UnboundLocalError: https://docs.python.org/3/faq/programming.html#why-am-i-getting-an-unboundlocalerror-when-the-variable-has-a-value
- Google Colab forms (`@param` slider): https://colab.research.google.com/notebooks/forms.ipynb
