# 08 - Operators blocks (green) to Python

## Summary

Scratch's green Operators blocks map almost one-to-one onto Python's arithmetic operators, comparison operators, `and`/`or`/`not`, string tools (`+`, `len`, `in`, indexing) and the `random` and `math` modules. Shapes carry over too: round reporters become **expressions that give a value** (numbers or text), and hexagonal booleans become **expressions that give `True` or `False`**.

Scratch is forgiving and Python is strict, and that difference causes most of the surprises:

- Scratch quietly turns text into numbers ("abc" becomes 0). Python raises `TypeError`.
- Scratch's `=`, `<`, `>` and `contains` ignore upper and lower case. Python's do not.
- Scratch letters are counted from 1. Python indexes from 0.
- Scratch `round` rounds .5 upward. Python's `round` uses banker's rounding.
- Scratch trig works in degrees. Python's `math` works in radians.
- Scratch divide by zero gives Infinity. Python raises `ZeroDivisionError`.
- Scratch `mod` and Python `%` both use floored division, so they agree, even for negative numbers.

Behaviour details below come from `scratch3_operators.js` and `util/cast.js` in scratch-vm.

## Block-by-block mapping table

| Scratch block | Shape | Scratch behaviour (from scratch-vm) | Python equivalent | Watch out |
|---|---|---|---|---|
| `( ) + ( )` | round | Casts both to number (bad text becomes 0) | `a + b` | `"5" + 3` gives TypeError; `"5" + "3"` gives `"53"` |
| `( ) - ( )` | round | Numeric subtraction | `a - b` | none |
| `( ) * ( )` | round | Numeric multiplication | `a * b` | `"5" * 3` gives `"555"` |
| `( ) / ( )` | round | JS division; `/0` gives Infinity | `a / b` | Always a float (`6 / 3` = `2.0`); `/0` gives ZeroDivisionError; `//` is whole-number division |
| `pick random ( ) to ( )` | round | Inclusive at both ends; swaps the ends if the first is bigger; if either end has a decimal point it returns a decimal | `random.randint(a, b)` (whole numbers) or `random.uniform(a, b)` (decimals) | Needs `import random`; `randint(10, 1)` gives ValueError (no auto-swap) |
| `< ( ) > ( ) >` | hexagon | Compares as numbers if both look numeric, otherwise as lower-case text | `a > b` | `"10" < "9"` is True for text, so convert with `int()` |
| `< ( ) < ( ) >` | hexagon | same | `a < b` | same |
| `< ( ) = ( ) >` | hexagon | Case-insensitive; `"5" = "5.0"` is true | `a == b` | Two `=` signs (`a = b` is assignment, a SyntaxError inside `if`); case-sensitive; `"5" == "5.0"` is False |
| `< < > and < > >` | hexagon | Logical AND | `a and b` | Lower-case keyword |
| `< < > or < > >` | hexagon | Logical OR | `a or b` | same |
| `< not < > >` | hexagon | Logical NOT | `not a` | same |
| `join ( ) ( )` | round | Joins as text | `a + b` (text only), `str(n)`, or f-string `f"{a}{b}"` | Numbers need `str()` or an f-string |
| `letter ( ) of ( )` | round | 1-based; out of range gives `""` | `s[i - 1]` | Index starts at 0; `s[10]` gives IndexError; `s[-1]` is the last letter, not empty |
| `length of ( )` | round | Length of the text | `len(s)` | Also works on lists |
| `< ( ) contains ( ) ? >` | hexagon | Case-insensitive substring test | `b in a` | Order flips (`"ell" in "hello"`); case-sensitive |
| `( ) mod ( )` | round | Floored modulo (result has the divisor's sign) | `a % b` | Same as Scratch for negatives (`-7 % 3` = 2); `% 0` gives ZeroDivisionError |
| `round ( )` | round | JS `Math.round` (.5 goes up: 2.5 to 3, -2.5 to -2) | `math.floor(x + 0.5)` for Scratch-identical results | `round(2.5)` = 2 (banker's rounding) |
| `[abs] of ( )` | round | Absolute value | `abs(x)` | Built in, no import |
| `[floor] of ( )` | round | Round down | `math.floor(x)` | `import math` |
| `[ceiling] of ( )` | round | Round up | `math.ceil(x)` | Name is `ceil` |
| `[sqrt] of ( )` | round | Square root; negative gives NaN | `math.sqrt(x)` | `sqrt(-1)` gives ValueError |
| `[sin] of ( )` / `[cos]` | round | Takes degrees; result rounded to 10 decimal places | `math.sin(math.radians(d))` | Radians! `cos(90 deg)` gives `6.1e-17`, not 0 |
| `[tan] of ( )` | round | Degrees; gives Infinity at 90 and -Infinity at 270 | `math.tan(math.radians(d))` | Gives `1.6e16` at 90 |
| `[asin]/[acos]/[atan] of ( )` | round | Returns degrees | `math.degrees(math.asin(x))` | Returns radians unless converted |
| `[ln] of ( )` | round | Natural log | `math.log(x)` | `log` in Python is ln |
| `[log] of ( )` | round | Base-10 log | `math.log10(x)` | Not `math.log` |
| `[e ^] of ( )` | round | e to the x | `math.exp(x)` | none |
| `[10 ^] of ( )` | round | 10 to the x | `10 ** x` | `^` in Python is XOR, not power! |

## Gaps and gotchas (with test output)

All results come from `python3` runs on 7 Nov 2026.

**1. Letters start at 1 in Scratch and 0 in Python**
```
"hello"[1]          -> 'e'      # Scratch letter 1 of hello = h
"hello"[1 - 1]      -> 'h'
"hello"[10]         -> IndexError: string index out of range   # Scratch gives ""
"hello"[-1]         -> 'o'      # Scratch letter 0 gives ""
```

**2. `=` is case-insensitive in Scratch and Python needs two signs**
```
"A" == "a"                       -> False   # Scratch: true
"A".lower() == "a".lower()       -> True
"5" == "5.0"                     -> False   # Scratch: true (numeric compare)
5 = 5                            -> SyntaxError: invalid syntax
```

**3. Text and number mixing (Scratch's `+` never errors)**
```
"5" + 3        -> TypeError: can only concatenate str (not "int") to str
"5" + "3"      -> '53'      # this is Scratch "join", not "+"
int("5") + 3   -> 8
"5" * 3        -> '555'
"10" < "9"     -> True      # text comparison; Scratch compares as numbers
```
This matters most after `input()`, which always returns text (the Scratch `answer` is cast automatically).

**4. Division**
```
7 / 2   -> 3.5      6 / 3 -> 2.0 (always a float)      7 // 2 -> 3
10 / 0  -> ZeroDivisionError   (Scratch shows Infinity)
10 % 0  -> ZeroDivisionError   (Scratch shows NaN)
0.1 + 0.2 -> 0.30000000000000004   (Scratch shows the same, so this is not a new surprise)
```

**5. Round: banker's rounding**
```
round(2.5) -> 2    round(3.5) -> 4    round(0.5) -> 0    round(-2.5) -> -2
math.floor(2.5 + 0.5) -> 3     # matches Scratch
```
Scratch uses JS `Math.round`: 2.5 becomes 3 and 0.5 becomes 1.

**6. Pick random**
```
random.randint(1, 10)  -> 10 (inclusive at both ends, like Scratch)
random.uniform(1, 10)  -> 1.728912671299149   # Scratch "pick random 1.0 to 10"
random.randint(10, 1)  -> ValueError: empty range   # Scratch swaps the ends silently
```
In Scratch, `pick random 1 to 10.0` gives decimals because one end has a decimal point. Python decides by which function you call.

**7. Mod with negatives agrees**
```
-7 % 3 -> 2    7 % -3 -> -2    math.fmod(-7, 3) -> -1.0
```
The scratch-vm source comment notes that Scratch mod uses floored division, the same as Python's `%`. Do not use `math.fmod`.

**8. Trig in degrees and radians**
```
math.sin(90)                          -> 0.8939966636005579   (radians!)
math.sin(math.radians(90))            -> 1.0
math.cos(math.radians(90))            -> 6.123233995736766e-17
round(math.cos(math.radians(90)), 10) -> 0.0   # what Scratch does internally
math.tan(math.radians(90))            -> 1.633123935319537e+16  (Scratch: Infinity)
math.degrees(math.asin(1))            -> 90.0
```

**9. Other math**
```
math.sqrt(-1) -> ValueError: math domain error  (Scratch: NaN)
math.log(100) -> 4.605...   (this is ln)     math.log10(100) -> 2.0  (this is Scratch "log")
math.floor(-2.5) -> -3    math.ceil(2.1) -> 3    abs(-4) -> 4    10 ** 2 -> 100
```

**10. Contains: the order flips and case matters**
```
"ell" in "hello"                  -> True
"ELL" in "hello"                  -> False   # Scratch: true
"ELL".lower() in "hello".lower()  -> True
```

**Gap:** no single Python operator covers the whole `[ ] of ( )` dropdown. Kids need `import math` plus several different names (`abs` is built in, `ceil` not `ceiling`, `log10` not `log`).

## Teaching ideas for a 9-year-old

**Analogy: Scratch is a friendly waiter, Python is a strict robot chef.** If you ask the waiter for "5" plus 3, they guess what you meant. The robot chef says "ERROR: I can't add a word to a number" until you tell it exactly what to do (`int("5") + 3`). The robot also counts its shelves starting at shelf 0, and it notices CAPITAL letters.

**Mini-challenge 1: Dice duel (pick random, >, if).** Roll two dice with `random.randint(1, 6)`. Print who wins, or "Tie!" using `==`. Bonus: roll 100 times and count how often you get a 6.

**Mini-challenge 2: Secret letter spy (letter of, length of, contains).** Ask for a name with `input()`. Print the first letter (`name[0]`), the last letter (`name[len(name) - 1]`, then the shortcut `name[-1]`), and whether it contains "a" in any case (`"a" in name.lower()`). Talk about why `name[1]` is not the first letter.

**Mini-challenge 3: Bug hunt.** Give five broken lines to fix, one per gotcha:
`if answer = "yes":`, `print("Score: " + 10)`, `print(round(2.5))` (expected 3), `print(math.sin(90))` (expected 1), `print("Hello"[1])` (expected H).

A quick test for the case-insensitivity idea: `if answer.lower() == "yes":` gives the same "any-case" feel as Scratch.

## Sources

- scratch-vm operators source: https://github.com/scratchfoundation/scratch-vm/blob/develop/src/blocks/scratch3_operators.js
- scratch-vm cast utilities (compare, toNumber, isInt): https://github.com/scratchfoundation/scratch-vm/blob/develop/src/util/cast.js
- Scratch Wiki, Operators Blocks: https://en.scratch-wiki.info/wiki/Operators_Blocks
- Scratch Wiki, Pick Random () to (): https://en.scratch-wiki.info/wiki/Pick_Random_()_to_()_(block)
- Scratch Wiki, Letter () of (): https://en.scratch-wiki.info/wiki/Letter_()_of_()_(block)
- Scratch Wiki, () = (): https://en.scratch-wiki.info/wiki/()_%3D_()_(block)
- Scratch Wiki, () of () math block: https://en.scratch-wiki.info/wiki/()_of_()_(Operators_block)
- Python docs, built-in round: https://docs.python.org/3/library/functions.html#round
- Python docs, math module: https://docs.python.org/3/library/math.html
- Python docs, random module: https://docs.python.org/3/library/random.html
