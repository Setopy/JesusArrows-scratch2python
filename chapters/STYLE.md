# Style guide for the expanded workbook "From Scratch to Python"

You are one of 12 agents. Each agent writes **one chapter file** (plus an answers file) for a LaTeX workbook that teaches a **9-year-old** who already knows **Scratch 3.0** to write Python in **Google Colab**. The coordinator will `\input` your file into the main book. Read this whole guide before writing.

Project folder: the repository's top folder (called ROOT below).

## 1. Files

- Write ONLY your own files: `ROOT/chapters/NN-name.tex`, `ROOT/chapters/NN-name-answers.tex` (if your brief says so), and your test files `ROOT/chapters/_test-NN.tex` and `ROOT/chapters/_build-NN/`. Never edit `preamble.tex`, other chapters, or the main `.tex`.
- Your chapter file has **no** `\documentclass`, no `\begin{document}`. It starts with your opener (see section 4).
- The answers file holds only `\subsection*{...}` blocks and their content. The coordinator puts all answers at the back of the book.

## 2. The Colab setup (TESTED LIVE in Colab on 7 Nov 2026: Python 3.13, ColabTurtlePlus 2.2.0)

The book uses the **ColabTurtlePlus** library in the `initializeTurtle()` style with plain commands (no `t.`):

```python
from ColabTurtlePlus.Turtle import *
clearscreen()
initializeTurtle((480, 360))
```

- These are **the three starting lines**. Every drawing program starts with exactly these three lines, character for character (the coordinator may replace them all with a script later, so do not vary them).
- After them, use plain commands: `forward(100)`, `right(90)`, `goto(0, 0)`, `pencolor("red")`, `speed(13)`. The plain commands move "the turtle", which plays the part of the selected sprite in Scratch.
- Extra sprites, only when a program needs two or more: `cat = Turtle()`, then `cat.forward(10)`. This was tested: plain commands and `Turtle()` objects work together in one cell. Explain it as "making a new sprite and giving it a name".
- The “In the beginning” cell, once per session: `!pip install ColabTurtlePlus` (NOT `ColabTurtle`: that is a different library with no `Turtle`, a black 800x500 window and (0, 0) at the top-left; never use it).
- Stage: `initializeTurtle((480, 360))` gives exactly the Scratch stage: centre (0, 0), x from -240 to 240, y from -180 to 180, y goes up.
- Directions: standard mode, 0 = right, 90 = up, anticlockwise. Scratch 0 = up, 90 = right, clockwise. Rule taught to the child: **Python direction = 90 - Scratch direction**, i.e. `setheading(90 - d)`. Turning (`right`, `left`) is the same as Scratch.
- **Never** use `mode("logo")` or `initializeTurtle((480, 360), "logo")`: tested live, `setheading(90)` then points DOWN (library bug).
- Speed: 1 (slow) to 13 (fastest animated). Do not use `speed(0)` (nothing shows until `done()`).
- Colour names must be lowercase HTML names: `"red"`, `"gold"`, `"skyblue"`.
- ColabTurtlePlus has NO `onkey`, `onkeypress`, `onclick`, `ontimer`, `listen`, `mainloop`, `textinput`, `numinput`, `bgpic`, `tracer`, sound, or image costumes. Interaction in Colab = `input()`. Key-press games belong in the Thonny section only (desktop `turtle`, `screen.onkeypress(f, "space")`, never `onkey`).
- Available turtle functions (check every name you use against this list or the source `ROOT/research/ref/ColabTurtlePlus-Turtle-2.2.x.py`; do NOT execute that file, only read it): animationOff, animationOn, back, backward, begin_fill, circle, clear, clearstamp, clearstamps, color, distance, done, dot, end_fill, face, fd, fillcolor, forward, getheading, goto, heading, hideturtle, home, isdown, isvisible, jumpto, left, pencolor, pensize, pendown, penup, pos, position, regularPolygon, reset, right, setheading, seth, setpos, setx, sety, shape, shapesize, showturtle, speed, stamp, teleport, tilt, towards, width, write, xcor, ycor. Screen functions: bgcolor, clearscreen, colormode, initializeTurtle, setup, showborder, hideborder, turtles, window_width, window_height. Shapes: "classic", "arrow", "triangle", "square", "circle", "turtle", "turtle2", "ring", "blank".
- `distance()` and `towards()` accept only numbers or an (x, y) pair, never a turtle (source lines 1891-1952). Write `cat.distance(dog.pos())` and `cat.towards(dog.pos())`, never `cat.distance(dog)`. (Desktop turtle in Thonny does accept a turtle.)
- `input()` always returns text. `int(...)` is needed for numbers.
- `clear()` on a turtle wipes its drawing; `clearscreen()` wipes everything.

## 3. Voice and level

- Write for a 9-year-old reading with a parent. Short sentences. Friendly, celebratory, never babyish. Use "you".
- British or neutral spelling is fine; be consistent with the existing book: "colour" in prose, but code uses `pencolor`/`color` because that is Python's spelling. Point this out once if relevant.
- Use analogies (from the research files): indentation = the C-block's mouth; a variable = a labelled box; a list = a backpack or train carriages; a function = a recipe card / your own super-block; a class = a cookie cutter; an error message = a detective's clue note.
- Explain every new piece of syntax as a bridge from Scratch: why the colon, quotes, brackets, `==`, `int()`.
- Never claim something is impossible without saying what to do instead.

## 4. Structure of a Part chapter (Parts 1 to 7)

1. Opener: `\partopener{<colour>}{PART n}{<Title>}{<one-line promise>}` where colour is a Scratch colour name defined in the preamble: motion, looks, sound, events, control, sensing, operators, variables, lists, myblocks, pen.
2. A short intro: which Scratch blocks this part covers, with a few `\chip[colour]{block text}` examples.
3. **Concept pages.** For every block or idea in your brief, a "side-by-side" unit:
   - `\subsection*{...}` with a kid-friendly title.
   - The Scratch block(s) drawn with the scratch3 package and the Python next to it, in a `tcbraster` with two columns (copy the pattern from section 6).
   - **How it works**: 2 to 5 sentences that bridge the syntax.
   - Optional `think`, `watchout` box.
4. **Missions** (2 to 4 per part), each started with `\mission{Title}{you will learn ...}` (auto-numbered; do not number missions yourself). Every mission has these steps, using `\step{...}`:
   - Step 1: Build it in Scratch (a scratch3 picture)
   - Step 2: Type it in Colab (`typethis` box)
   - Step 3: Read it line by line (longtable: Line | Scratch block | What it means). **Line numbers must match the listing's numbering, which counts blank lines too.**
   - Step 4: Run it (`outputbox` with what they should see, or a description of the drawing)
   - Step 5: Make it yours (`challenge` box with 3 or 4 `\tick` items)
5. **Translate it yourself**: one unseen Scratch script, with ruled lines to write the Python (pattern in section 6). Answer goes in your answers file.
6. **Two-line puzzle**: a `puzzle` box with a tiny puzzle whose answer is 2 lines of Python. Answer in your answers file.
7. **Part checklist**: "I can..." list with `\tick` boxes (4 to 6 items).

Length: aim for 9 to 13 printed pages per Part. Use `\needspace{N\baselineskip}` before blocks that must not split. Every `\mission` starts a new page automatically.

## 5. Code rules

- Every Python program in the book must run. Test every program that does not draw with `python3 -I` (pipe input with `printf 'Ada\n7\n' | python3 -I prog.py`). For drawing programs, check every function name against section 2, and run the logic with a stand-in: create a file in your build folder that defines the used functions as plain Python recording calls (forward/right/goto/xcor... updating x, y, heading with standard turtle maths), import it instead of ColabTurtlePlus, and run the program. Report in your final message what you tested and how.
- Keep each code line under about 55 characters so it fits a `typethis` box without wrapping.
- Four spaces for indentation. No tabs.
- Comments in code sparingly (`# like this`); explanations go in the line-by-line tables.
- Put all drawing programs that you write into `ROOT/chapters/NN-colab-tests.py`, separated by lines `# %% <mission or page name>`, each piece complete with its three starting lines, so the coordinator can paste them into Colab and run them. Use `input()` programs too, but mark them `# needs typing: <what to type>`.

## 6. LaTeX patterns (copy these; the macros live in ROOT/preamble.tex)

Look at `ROOT/scratch-to-python-workbook-v2-backup.tex` for many working examples of every pattern below, including scratch3 block syntax. Note: that old file uses `t.forward` etc.; the new book uses plain `forward`.

Side by side:
```latex
\begin{tcbraster}[raster columns=2, raster equal height=rows, raster column skip=12pt, raster valign=center]
\begin{tcolorbox}[colback=white, colframe=white, boxrule=0pt, valign=center]
\begin{scratch}
\blockinit{when \greenflag clicked}
\blockrepeat{repeat \ovalnum{4}}{
  \blockmove{move \ovalnum{100} steps}
  \blockmove{turn \turnright{} \ovalnum{90} degrees}
}
\end{scratch}
\end{tcolorbox}
\begin{code}
for i in range(4):
    forward(100)
    right(90)
\end{code}
\end{tcbraster}
```

scratch3 macros used in the book: \blockinit (hat), \blockmove, \blocklook, \blocksound, \blockevent, \blockcontrol, \blocksensing, \blockvariable, \blocklist, \blockpen, \blockmoreblocks, \initmoreblocks{define \namemoreblocks{name \ovalmoreblocks{arg}}}, \blockrepeat{repeat \ovalnum{n}}{...}, \blockinfloop{forever}{...}, \blockif{if \booloperator{...} then}{...}, \blockifelse{if ...}{...}{...}, \blockstop{stop \selectmenu{all}}, \ovalnum{}, \ovalvariable{}, \ovaloperator{}, \ovalsensing{}, \ovalmove{}, \ovallist{}, \ovalmoreblocks{}, \booloperator{}, \boolsensing{}, \boollist{}, \selectmenu{}, \greenflag, \turnright{}, \turnleft{}, \blockspace. If you need another macro (e.g. \ovallook, \boolempty, \blockrepeat with "repeat until", \ovalcontrol), test-compile it first.

Other boxes: `typethis` (numbered, titled "Type this into a code cell"), `code` (numbered), `codenonum`, `spaces` (shows visible spaces), `outputbox` (monospace output), `watchout`, `think`, `challenge`, `puzzle`, `errorbox`. Inline code: `\py|forward(100)|`. Inline block: `\chip[motion]{move 10 steps}`. Buttons: `\playbtn`, `\stopbtn`. Tick box: `\tick`.

Translate it yourself (ruled answer lines):
```latex
\begin{tcolorbox}[colback=white, colframe=codeframe, arc=5pt, title=\textbf{My Python}, coltitle=ink, colbacktitle=codebg]
\vspace{4pt}
\foreach \n in {1,...,7}{\rule{\linewidth}{0.4pt}\par\vspace{9pt}}
\end{tcolorbox}
```

Line-by-line table:
```latex
\begin{longtable}{>{\centering\arraybackslash}p{1.1cm} P{5.3cm} P{9.1cm}}
\toprule
\textbf{Line} & \textbf{Scratch block} & \textbf{What it means} \\
\midrule
1--3 & \chip[events]{when green flag clicked} & The three starting lines. \\
\bottomrule
\end{longtable}
```

Gotchas: `\py|...|` cannot be used inside the argument of `\chip`, `\subsection`, or a tcolorbox `title=`; use `\texttt{}` there. Escape `#`, `%`, `_`, `&`, `$` outside code (`\#`, `\%`, `\_`, `\&`). `listings` environments cannot be inside another macro's argument.

## 7. Test-compile and look

1. Copy `ROOT/chapters/_harness.tex` to `ROOT/chapters/_test-NN.tex`, change `XX-name` to your file names (drop the answers lines if you have no answers file).
2. From ROOT run: `mkdir -p chapters/_build-NN && tectonic -o chapters/_build-NN chapters/_test-NN.tex` (paths inside the harness are relative to `chapters/`) (tectonic is the only TeX on this Mac; first run downloads packages, allow 2 to 5 minutes; use a long timeout).
3. Render pages: `pdftoppm -r 40 -png chapters/_build-NN/_test-NN.pdf chapters/_build-NN/pg` and LOOK at them with the Read tool (they are images). Fix overflowing code, orphaned headings, half-empty pages, broken tables.
4. Fix until it compiles with no errors.

## 8. Research to use

`ROOT/research/00-curriculum-map.md` (overview) and the 20 reports `ROOT/research/01-motion.md` ... `20-projects.md`. Your brief names the ones you must read. Take facts from them, but re-check anything about Colab against section 2 of this guide (section 2 wins: it was tested live).

## 9. Final reply

At most 150 words: your file names, page count of your test PDF, what you tested and how, and anything the coordinator must know (e.g. a macro you needed, a claim you could not verify).
