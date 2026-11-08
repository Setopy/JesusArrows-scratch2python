# 16. Errors and debugging: from "Scratch never complains" to "Python leaves clue notes"

## Summary

- **Scratch hides errors on purpose.** Maloney, Resnick et al. (2010) say Scratch has no error messages: blocks only fit together in ways that make sense (like LEGO), so syntax errors cannot happen, and runtime blocks "fail soft" by returning something harmless and carrying on. A child who learned in Scratch has therefore never seen an error message. Some examples: `item 99 of` a 3-item list gives an empty string, `"hello" * 2` gives `0`, `10 / 0` gives `Infinity`, and a typo in a variable name is impossible because you pick names from a palette.
- **Python stops and explains.** A Python error is the computer saying "I stopped here, on this line, because of this." The child needs to learn that **the last line of the red box is the clue**, and that the line number and the `^^^^` arrows point to the scene of the crime.
- **Modern Python is much kinder than it used to be.** Python 3.10+ adds "Did you mean...?" hints and `expected ':'`. Python 3.11+ underlines the exact part of a line with `~~~^~~~` (PEP 657). All the messages below were captured with **Python 3.13.5** (macOS). Colab runs 3.12, which gives the same wording for these cases; check with `import sys; print(sys.version)`.
- **Two families of bugs** (worth teaching by name):
  1. **Grammar bugs** (`SyntaxError`, `IndentationError`). Python refuses to run *any* of the cell. No traceback header, just `File ..., line N`.
  2. **Running bugs** (all the rest). Python runs the lines one by one and stops at the bad one. Starts with `Traceback (most recent call last):`. Lines *before* the bad one have already run (their `print`s show up).
  3. Plus the **silent bug** (infinite loop, wrong logic): there is no message at all, just like Scratch. That is where "say debugging" (`print`) comes back.
- **Research note.** "Enhanced" error messages help novices less reliably than you would hope (Becker et al. 2019 review; mixed results with middle-schoolers learning Python, Zhou et al. 2021). What helps more is *teaching how to read* the message. That is the purpose of the Bug Zoo below.

## Bug Zoo

All outputs are real, from `python3` 3.13.5. File paths are shortened to `File "bug.py"`; in Colab you see `<ipython-input-N-...>` or `/tmp/ipython-input-...` instead, plus a few lines of Colab framing.

| # | Bug (Zoo animal name idea) | Scratch habit that causes it | Broken snippet | Real error message (Python 3.13.5) | Kid-friendly explanation and fix |
|---|---|---|---|---|---|
| 1 | **Missing colon** (`SyntaxError`), "the Colon Cobra" | The C-shaped `if` / `forever` block *is* the opening. There is nothing to type. | `if 5 > 3`<br>`    print("yes")` | `File "bug.py", line 1`<br>`    if 5 > 3`<br>`            ^`<br>`SyntaxError: expected ':'` | Every `if`, `for`, `while`, `def` line is the "mouth" of a C-block, and the colon `:` is the mouth opening. Python even tells you exactly what it expected. Add `:` at the end. |
| 2 | **Indentation** (`IndentationError`), "the Wobbly Stack" | In Scratch, blocks *snap inside* the C-block; you never think about spaces. | `for i in range(3):`<br>`print(i)` | `File "bug.py", line 2`<br>`    print(i)`<br>`    ^^^^^`<br>`IndentationError: expected an indented block after 'for' statement on line 1` | The spaces at the start of a line show which C-block it is inside. No spaces = "outside the loop". Press Tab before `print`. Its twin: too many spaces where none are needed gives `IndentationError: unexpected indent`. |
| 3 | **Typo in a name** (`NameError`), "the Misspelled Monkey" | Scratch variables come from a dropdown/palette, so you can never misspell one. | `score = 10`<br>`print(scroe)` | `Traceback (most recent call last):`<br>`  File "bug.py", line 2, in <module>`<br>`    print(scroe)`<br>`          ^^^^^`<br>`NameError: name 'scroe' is not defined. Did you mean: 'score'?` | Python has never heard of `scroe`. It even guesses what you meant! Read the "Did you mean" part and fix the spelling. |
| 4 | **Upper/lower case** (`NameError`), "the Capital Copycat" | Scratch block text is fixed; `Say` vs `say` never matters. | `Print("hi")`<br><br>`name = "Sam"`<br>`print(Name)` | `NameError: name 'Print' is not defined. Did you mean: 'print'?`<br><br>`NameError: name 'Name' is not defined. Did you mean: 'name'?` | To Python, `Name` and `name` are two different boxes, like "Sam" and "sam" being two different kids. Python words (`print`, `if`, `True`) have to be spelled exactly. |
| 5 | **Text + number** (`TypeError`), "the Glue Goblin" | Scratch's `join` happily glues `Score: ` and `10`, and `+` turns text into numbers. Scratch converts types silently. | `score = 10`<br>`print("Score: " + score)` | `TypeError: can only concatenate str (not "int") to str` (with `~~~~~~~~~~^~~~~~~` under the `+`) | "concatenate" = glue together. "str" = text, "int" = whole number. Python will not glue a word to a number. Use `str(score)`, or `print("Score:", score)`, or `f"Score: {score}"`. |
| 5b | **The `ask` trap** (same `TypeError`) | Scratch `answer` acts like a number if you typed a number. | `age = input("Age? ")`<br>`print(age + 1)` | `TypeError: can only concatenate str (not "int") to str` | `input()` *always* gives text, even if you type 9. Wrap it: `age = int(input("Age? "))`. |
| 6 | **Missing quotes** (`NameError` or `SyntaxError`), "the Quote Thief" | In Scratch you type into a white bubble; you never need quote marks. | `print(hello)`<br><br>`print("hello)` | `NameError: name 'hello' is not defined. Did you mean: 'help'?`<br><br>`SyntaxError: unterminated string literal (detected at line 1)` | Without quotes, Python thinks `hello` is the name of a variable. Quotes say "this is just text". A missing *closing* quote = "you started some text and never finished it". The first case is sneaky: the message says NameError, but the real fix is to add quotes. |
| 7 | **Missing brackets on print** (`SyntaxError`), "the Bracketless Bat" | `say [Hello!]` has no brackets; old Python 2 tutorials online also use `print "x"`. | `print "hello"` | `SyntaxError: Missing parentheses in call to 'print'. Did you mean print(...)?` | `print` is a block that needs its "input hole", and in Python the hole is `( )`. Its cousin, a bracket opened but not closed: `print("hi"` gives `SyntaxError: '(' was never closed`. |
| 8 | **`=` vs `==`** (`SyntaxError`), "the Equals Eel" | Scratch has one `=`, which means "is equal?" inside the green block and `set` is a separate block. | `x = 5`<br>`if x = 5:`<br>`    print("five")` | `SyntaxError: invalid syntax. Maybe you meant '==' or ':=' instead of '='?` | One `=` is the `set` block ("put 5 in x"). Two `==` is the green `( ) = ( )` question block ("is x 5?"). Ignore `:=`; that is an advanced tool. |
| 9 | **Word that is not a number** (`ValueError`), "the Number Faker" | Scratch treats non-numbers as `0` with no complaint. | `age = int("five")` | `ValueError: invalid literal for int() with base 10: 'five'` | `int()` can turn `"5"` into `5`, but it cannot read words. Ignore "literal" and "base 10" for now; the clue is `'five'`. Type digits, or (later) use `try`/`except`. |
| 10 | **Item that does not exist** (`IndexError`), "the Off-by-One Owl" | Scratch lists start at **item 1** and `item 99` of a short list just gives empty. | `fruits = ["apple", "banana", "cherry"]`<br>`print(fruits[99])` | `IndexError: list index out of range` (with `~~~~~~^^^^` under `[99]`) | "index" = item number, "out of range" = no such item. **Python counts from 0**, so the 3 fruits are `[0]`, `[1]`, `[2]`; `fruits[3]` also fails. Use `len(fruits)` to check. |
| 11 | **Divide by zero** (`ZeroDivisionError`), "the Zero Zombie" | Scratch gives `Infinity` (or `-Infinity`/`NaN`) and keeps going. | `print(10 / 0)` | `ZeroDivisionError: division by zero` | Sharing 10 sweets among 0 friends makes no sense, so Python stops. Check `if friends != 0:` first. |
| 12 | **Infinite loop** (no message!), "the Forever Phantom" | `forever` is normal in Scratch, and the green flag / stop sign controls it. A `repeat until` whose condition never changes just spins quietly. | `count = 0`<br>`while count < 3:`<br>`    print("hi")` | *No error at all.* In 0.05 s it printed "hi" 81,930 times. In Colab the cell's spinning circle never stops. | You forgot to change `count`, so `count < 3` is true forever. Press the **stop button (square) on the cell** (or Runtime > Interrupt execution, Ctrl+M I); you will then see `KeyboardInterrupt`, which just means "you stopped me". Fix: add `count = count + 1` inside the loop (Scratch's `change count by 1`). |

Bonus specimens (good for later):
- `"hello" * 2` gives `hellohello` (no error; Scratch would say `0`!). `"hello" * "2"` gives `TypeError: can't multiply sequence by non-int of type 'str'`.
- `len(5)` gives `TypeError: object of type 'int' has no len()`.
- `fruits[-1]` gives `cherry` (no error; negative numbers count from the end). Scratch has the `last` option for this.

## How Colab shows errors

- The error appears **under the cell** in the output area, with the error name in red/bold (for example **NameError**) and a traceback. Colab traceback lines point to the cell with an arrow `---->` next to the offending line number, and the `^^^^` / `~~~^~~~` marks underline the exact spot.
- For a **running bug**, anything printed *before* the bad line is still shown above the error. That is a clue in itself: "it got this far".
- For a **grammar bug**, *nothing* in the cell runs, not even line 1.
- Variables from earlier cells stay alive. A common confusing case: you fix a typo, but run cells out of order, and get `NameError` because the cell that creates the variable was never run. Runtime > Restart and run all is the "click the green flag again from scratch" button.
- Colab may show an **"Explain error"** button (AI assistant). For a learner, I suggest reading the last line *yourself first*, guessing, and only then pressing it, otherwise the detective work is skipped. (Availability depends on the account and region; verify on the child's account.)
- Colab line numbers: switch on **Tools > Settings > Editor > Show line numbers**, so "line 3" in the error can be matched to the cell.

## Debugging tricks (Scratch to Python)

| Scratch trick | Python version |
|---|---|
| `say (score) for 2 seconds` to see a value | `print("score is", score)`, i.e. "say debugging". Put one before and after the suspicious line. |
| Tick the checkbox to show a variable monitor on the stage | `print(score)` inside the loop, or Colab's **Variables** panel ({x} icon in the left sidebar) |
| Add `wait 1 seconds` to slow things down | `import time` then `time.sleep(1)` inside the loop |
| Click a block to run just that one | Run a single small cell; split a big cell into smaller ones |
| Ask a friend to read the script | **Rubber duck**: explain your code line by line out loud to a toy; you often hear the bug yourself |
| Debug list (`add (x) to [log]`) | `log.append(x)` then `print(log)` |

**Reading an error, in 3 steps (the Detective's Routine):**
1. **Read the LAST line first.** The word before the colon is the *kind* of bug (which Zoo animal). The words after it are the clue.
2. **Find the line number** (`line 2`) and look where the `^^^^` arrows point.
3. **Check the line *above* too.** For grammar bugs (missing `)` or `"`), the real mistake is often on the line before the one Python names.

## Gaps and gotchas

- **Some Scratch silent bugs become Python silent bugs.** `"hello" * 2` gives `hellohello` with no error, and `fruits[-1]` works. The child may expect an error and not get one.
- **The error name can mislead.** A missing quote often shows as `NameError` (case 6, even with a funny `Did you mean: 'help'?`), not a "quote error". Teach "the message tells you *what Python saw*, not always *what you did*".
- **Jargon words** a 9-year-old will meet: *syntax* (grammar), *str* (text), *int* (whole number), *concatenate* (glue), *index* (item number), *literal* (a value typed directly), *module* (`<module>` = "your main program"), *traceback* (the trail of footprints). A small glossary card helps.
- **0-based lists** are the biggest Scratch-to-Python gotcha for `IndexError`: Scratch `item 1` = Python `[0]`.
- **Version differences.** Wording like `Did you mean:` (3.10+), `expected ':'` (3.10+) and the `~~~^~~~` underlines (3.11+) do not appear in older Pythons or in old tutorials and videos. Older guides show the scarier `SyntaxError: invalid syntax`. Materials should be checked on the actual Colab version.
- **Tabs vs spaces**: Colab inserts 2 spaces by default (setting: Tools > Settings > Editor > indentation width); copying code from elsewhere with 4 spaces is fine as long as each block is consistent; mixing can cause `IndentationError` / `TabError`.
- **Infinite loops with `print`** can make the Colab tab slow because of huge output; teach the stop button before teaching `while`.
- `input()` in Colab shows a text box under the cell. If you re-run another cell while it is waiting, the program gets confused; finish typing first.
- Research shows that clearer messages alone do not reliably help novices (Becker et al. 2019; Zhou et al. 2021). Explicitly teaching how to *read* them is the part that matters.

## Teaching ideas for a 9-year-old

**Analogy: the Detective's Clue Note.** When Scratch hits a problem, it quietly sweeps it under the rug. Python is a detective's assistant: it freezes the scene and leaves you a clue note. The note always says *where* it happened (the line number, like a room in the house), *which kind* of trouble it was (the error name, like the suspect's name), and a hint (the words after the colon). Red does not mean "you failed"; it means "a clue has arrived". Real programmers get these notes all day long. Optional: a "Bug Zoo" sticker chart, one sticker for each new species caught and fixed.

**Debug It challenges** (in the spirit of the Harvard Creative Computing "Debug It" activities: programs that do not work as intended, fixed by the learner). Each has a mix of loud bugs and one silent bug.

1. **"The Cat Who Can't Count"** (3 bugs: colon, indentation, missing increment)
   ```python
   count = 1
   while count <= 5
   print("Meow number", count)
   ```
   Goal: print Meow 1 to 5. Clues come in order: `expected ':'`, then `IndentationError`, then a silent forever loop (stop the cell!), which is fixed by `count = count + 1` (Scratch: `change count by 1`).

2. **"Scoreboard Mix-up"** (3 bugs: typo, case, text + number)
   ```python
   score = 0
   score = score + 10
   Print("Your score is " + scroe)
   ```
   Clues: `Print` (Did you mean 'print'?), then `scroe` (Did you mean 'score'?), then TypeError. Fix with `print("Your score is", score)`. Bonus: ask why the error shows only one bug at a time (Python stops at the first problem it finds).

3. **"The Missing Fruit"** (0-based list + silent bug)
   ```python
   fruits = ["apple", "banana", "cherry"]
   print("First fruit:", fruits[1])
   print("Last fruit:", fruits[3])
   ```
   The first line runs but prints `banana` (a silent bug, no error!). The second gives IndexError. Discuss: Scratch `item 1` = Python `[0]`; the last item is `[2]` or `[-1]`. Use "say debugging": `print(len(fruits))`.

**Other quick ideas**
- **Bug-making game:** the child *deliberately* breaks a working program in one way and predicts which Zoo animal will appear before running it. Predicting errors is the fastest way to stop fearing them.
- **Swap roles:** the adult writes a broken cell; the child is the detective and must say the error name and line number out loud before touching the keyboard.
- **Rubber duck station:** a toy next to the laptop; rule: "explain it to the duck before asking a grown-up".

## Sources

- Maloney, J., Resnick, M., Rusk, N., Silverman, B., Eastmond, E. (2010). *The Scratch Programming Language and Environment*. ACM TOCE 10(4), article 16. https://doi.org/10.1145/1868358.1868363 ; MIT Media Lab page: https://www.media.mit.edu/publications/the-scratch-programming-language-and-environment/
- Resnick, M. et al. (2009). *Scratch: Programming for All*. Communications of the ACM 52(11). https://doi.org/10.1145/1592761.1592779 (not fetched here; cited for the design philosophy)
- Scratch Wiki, "Debugging". https://en.scratch-wiki.info/wiki/Debugging
- Harvard Creative Computing / ScratchEd, "Debug It" activities. https://scratched.gse.harvard.edu/resources/debug-it ; https://scratched.gse.harvard.edu/resources/debug-it-2.html ; curriculum: https://creativecomputing.gse.harvard.edu/
- PEP 657, "Include Fine Grained Error Locations in Tracebacks" (Python 3.11). https://peps.python.org/pep-0657/
- Python 3.11 What's New (error locations). https://docs.python.org/3/whatsnew/3.11.html ; 3.10 better error messages: https://docs.python.org/3/whatsnew/3.10.html#better-error-messages
- LWN, Python 3.12 error message improvements. https://lwn.net/Articles/928437
- Zhou, Z., Wang, S., Qian, Y. (2021). Learning from errors: exploring the effectiveness of enhanced error messages in learning to program. *Frontiers in Psychology* 12:768962. https://www.frontiersin.org/articles/10.3389/fpsyg.2021.768962
- Becker, B. A. (2016). Effective compiler error message enhancement for novice programming students. *Computer Science Education* 26(2-3). Becker, B. A. et al. (2019). Compiler error messages considered unhelpful (ITiCSE Working Group report). https://doi.org/10.1145/3344429.3372508
- Error outputs: run locally with `python3` 3.13.5 (macOS), 7 Nov 2026.
