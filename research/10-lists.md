# 10. Lists: Scratch 3.0 to Python

## Summary

Scratch lists and Python lists hold the same idea: one name, many items in order. Almost every Scratch list block has a one-line Python equivalent. The two big differences:

1. **Counting starts at 1 in Scratch and at 0 in Python.** `item 1 of [backpack]` is `backpack[0]`. Every block that takes a position needs `- 1` (or `+ 1` for `item # of`).
2. **Scratch never crashes; Python complains.** Scratch quietly returns an empty string for a bad position, `0` for a missing item, and ignores impossible deletes. Python raises `IndexError` or `ValueError`. That is a feature to teach: the error message tells you what went wrong.

There is one nasty half-exception: in Python a **negative** position does not crash, it counts from the end. So the beginner bug `backpack[n - 1]` with `n = 0` gives `backpack[-1]`, the *last* item, with no error.

All Python below was run with `python3` (3.x) on 7 Nov 2026; outputs shown are the real outputs.

## Block-by-block mapping table

Example list used throughout: `backpack = ["apple", "torch", "map"]`.

| Scratch block | Python | Tested result / notes |
|---|---|---|
| make a list `backpack` | `backpack = []` | Empty list. Scratch lists are global or "this sprite only"; Python lists live in the notebook. |
| `add (apple) to [backpack]` | `backpack.append("apple")` | Adds to the end. Scratch stops adding at 200,000 items; Python has no such limit. |
| `delete (2) of [backpack]` | `del backpack[2 - 1]` or `backpack.pop(1)` | `['apple', 'map']`. `pop` also hands back the removed item. |
| `delete (last) of [backpack]` | `backpack.pop()` | Removes and returns the last item. |
| `delete (all) of [backpack]` (typed "all") | `backpack.clear()` | Scratch's delete block accepts the word `all`. |
| `delete all of [backpack]` | `backpack.clear()` | `[]`. (`backpack = []` also works but makes a new list.) |
| `insert (rope) at (2) of [backpack]` | `backpack.insert(2 - 1, "rope")` | `['apple', 'rope', 'torch', 'map']`. Scratch allows position up to length + 1 (= add to end). Python's `insert(99, x)` silently adds to the end, no error. |
| `replace item (3) of [backpack] with (lamp)` | `backpack[3 - 1] = "lamp"` | Python raises `IndexError` if position is past the end; Scratch does nothing. |
| `item (1) of [backpack]` | `backpack[1 - 1]` i.e. `backpack[0]` | `'apple'`. Out of range: Scratch gives `""`, Python gives `IndexError: list index out of range`. |
| `item (last) of [backpack]` | `backpack[-1]` | Python's negative index, a bonus over Scratch. |
| `item (random) of [backpack]` | `random.choice(backpack)` | Needs `import random`. Scratch also accepts `any`. On an empty list Scratch gives `""`, Python raises `IndexError`. |
| `item # of (map) in [backpack]` | `backpack.index("map") + 1` | Missing item: Scratch gives `0`, Python raises `ValueError: 'cake' is not in list`. Guard with `if "cake" in backpack:` first. |
| `length of [backpack]` | `len(backpack)` | `4` |
| `<[backpack] contains (rope)?>` | `"rope" in backpack` | `True`. **Scratch ignores capitals, Python does not:** `"ROPE" in backpack` is `False`. |
| `show list [backpack]` | `print(backpack)` | Prints `['apple', 'rope', 'lamp', 'map']`. No live on-stage monitor in Colab; you print again whenever you want to look. |
| `hide list [backpack]` | (just stop printing) | No equivalent needed. |
| `(backpack)` reporter (round list block) | `" ".join(backpack)` | `'apple rope lamp map'`. Scratch special rule: if **every** item is a single character, it joins with **no** spaces (`c`,`a`,`t` gives `cat`); Python equivalent `"".join(...)`. `join` needs strings: `" ".join([1,2,3])` raises `TypeError`; use `" ".join(str(n) for n in nums)`. |
| Right-click list > **import** (.txt/.csv, one item per line) | `items = [line.strip() for line in open("words.txt")]` | In Colab, upload the file first (Files panel, or `from google.colab import files; files.upload()`). |
| Right-click list > **export** | `open("backpack.txt", "w").write("\n".join(backpack))` | Then download from the Colab Files panel. |

### Scratch-faithful helpers (tested)

If a lesson wants Scratch behaviour exactly, these match it:

```python
def item_of(lst, n):          # item (n) of [lst]
    if 1 <= n <= len(lst):
        return lst[n - 1]
    return ""                 # Scratch gives empty for bad positions

def item_num(lst, thing):     # item # of (thing) in [lst]
    low = str(thing).lower()  # Scratch ignores capitals
    for i, it in enumerate(lst, start=1):
        if str(it).lower() == low:
            return i
    return 0                  # Scratch gives 0 if not found
```

Tested: `item_of(backpack, 10)` gives `''`, `item_of(backpack, 0)` gives `''`, `item_num(backpack, "ROPE")` gives `2`, `item_num(backpack, "cake")` gives `0`.

### What Python adds (no single Scratch block)

| Python | What it does | Tested |
|---|---|---|
| `for snack in snacks:` | Visit every item, no counter variable needed (Scratch needs `repeat (length)` + a counter + `item (i)`). | prints `I eat crisps`, `I eat banana` |
| `scores.sort()` / `sorted(scores, reverse=True)` | Sorting, which Scratch lacks entirely. | `[2, 5, 9]` / `[9, 5, 2]` |
| `max(scores)`, `min`, `sum(scores)` | Instant high score / total. | `9`, `16` |
| `backpack.remove("b")` | Delete by *value*, not by position. | `['a', 'c']` (raises `ValueError` if absent) |
| `backpack[-1]`, `backpack[-2]` | Count from the end. | last, second-to-last |
| `backpack[0:2]` | Slices: a piece of the list. | first two items |
| `grid = [["X","O"],["O","X"]]`, `grid[1][0]` | Lists of lists (a game board). Scratch cannot nest lists. | `'O'` |
| `pet = {"name": "Rex", "legs": 4}`, `pet["name"]` | Dictionary: a "labelled backpack", find things by label not position. | `'Rex'` |

## Gaps and gotchas

1. **Off-by-one.** Every position block needs `- 1`; `item #` needs `+ 1`. The most common mistake by far.
2. **Negative index silently wraps.** `lst[0 - 1]` is the last item, not an error. A Scratch user expects "item 0" to be nothing.
3. **Errors instead of blanks.** `IndexError` (bad position) and `ValueError` (`index()`/`remove()` of a missing value). Teach reading the last line of the red error box.
4. **Capitals.** Scratch `contains`, `item #` and `=` ignore upper/lower case (scratch-vm `Cast.compare` lowercases strings). Python is exact: `"Rope" != "rope"`.
5. **Numbers vs text.** Scratch treats `5` and `"5"` as the same item; Python does not: `5 in ["5"]` is `False`. Numbers from `input()` are text until `int()`.
6. **The join reporter.** Scratch silently joins lists into text when you drop the list block in `say`. Python `print(backpack)` shows brackets and quotes; use `" ".join(...)` for the Scratch look, and convert numbers with `str` first.
7. **Fractional positions.** Scratch floors them (`item 2.7` is item 2). Python rejects floats: `lst[2.7]` is a `TypeError`. Use `int()`.
8. **Shared lists.** `b = a` does not copy; `b.append(3)` also changes `a` (tested: `a` became `[1, 2, 3]`). Use `b = a.copy()`. Scratch has no such surprise.
9. **No live monitor.** Scratch shows the list updating on the stage; in Colab you must `print` it. Printing inside the loop helps the child "see" the list change.
10. **Limits.** Scratch caps add/insert at 200,000 items (import is uncapped). Python has none worth mentioning for a child.

## Teaching ideas for a 9-year-old

**Analogy: a train.** Each carriage carries one item. In Scratch the carriages are numbered from 1 like seats. In Python the numbers are *how many carriages from the engine*: the first carriage is 0 steps away. `append` hooks a carriage on the back, `insert` squeezes one in, `del` uncouples one and the train closes the gap, `len` counts the carriages. Negative numbers count back from the guard's van at the end. (A dictionary is then a backpack with labelled pockets: you reach for the "snacks" pocket, not "pocket 3".)

**Mini-challenge 1: Packing for camp.** Start with `backpack = []`. Ask the child three times with `input()` and `append` each answer. Print `"I packed " + " ".join(backpack)`. Bonus: if they type something already packed (`if thing in backpack:`), say "Already got it!".

**Mini-challenge 2: Fix the robot's counting.** Give buggy code `print("First is", train[1])` and `print("Item 0 is", train[0 - 1])`. The child predicts the output, runs it, then fixes it. Makes the 0-based rule and the negative-index trap memorable.

**Mini-challenge 3: Random joke / fortune machine.** A list of 5 jokes; `import random`; `print(random.choice(jokes))` in a loop that runs until the child types `stop`. Then rewrite the Scratch-style version with `jokes[random.randint(1, len(jokes)) - 1]` and compare, to see why `random.choice` is nicer. Extension: keep a high-score list, `sort()` it and print the top 3 with a `for` loop.

## Sources

- Scratch Wiki, List: https://en.scratch-wiki.info/wiki/List
- Scratch Wiki, list block pages (linked from the List page), e.g. https://en.scratch-wiki.info/wiki/Item_()_of_()_(block) and https://en.scratch-wiki.info/wiki/Item_Number_of_()_in_()_(block)
- scratch-vm source, list blocks: https://github.com/scratchfoundation/scratch-vm/blob/develop/src/blocks/scratch3_data.js (LIST_ITEM_LIMIT = 200000; join rule for single-character items; `item #` returns 0; insert allows length + 1)
- scratch-vm source, casting rules: https://github.com/scratchfoundation/scratch-vm/blob/develop/src/util/cast.js (`toListIndex`: "all", "last", "random"/"any", flooring, out of range is invalid; `compare`: case-insensitive)
- Python tutorial, lists: https://docs.python.org/3/tutorial/datastructures.html
- Python `random.choice`: https://docs.python.org/3/library/random.html#random.choice
