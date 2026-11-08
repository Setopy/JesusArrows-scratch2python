# 19. Environments: where the child should write Python

Research date: 7 November 2026. Facts marked (verified) were checked on the tool's own page or docs during this research. Facts marked (unverified) come from general knowledge or secondary sources and should be tested before going into the workbook.

## Summary

1. **Colab + ColabTurtlePlus cannot do Scratch "Events" or "Sensing".** Its own documentation leaves out every event, keyboard, mouse, timer and input-dialog function (`onkey`, `onclick`, `ontimer`, `listen`, `mainloop`, `textinput`, `numinput`). It also has no `bgpic`, no `undo`, no `tracer` and no sound (verified). It is very good for Motion, Pen, Looks (shapes, stamp, colour, `write`), Operators, Variables, My Blocks and multiple turtles. So it covers drawing programs, not games.
2. **Two well-known "second tools" are gone or frozen.** Trinket.io shut down on 31 August 2026, and all hosted trinkets were lost (verified). A community copy runs at trinket.strivemath.org, but nobody guarantees it will last. Mu editor's GitHub repository was archived on 31 August 2025 and is no longer maintained, although it still runs (verified). Do not build a 2026 to 2027 workbook on either one.
3. **Best second tool for key-press games: Thonny with Pygame Zero.** Thonny is free and maintained (5.0.0, April 2026, bundles Python 3.14). It has a built-in *Run → Pygame Zero mode* and installs `pgzero` through *Tools → Manage packages* (verified). Pygame Zero's hooks map almost one-to-one onto Scratch hat blocks: `on_key_down`, `on_mouse_down`, `update()` as `forever`, `Actor` as sprite, `sounds.x.play()`, `clock.schedule`. Standard-library `turtle` also works in Thonny with real `onkey`, `onclick` and `ontimer`, which makes a gentle bridge before Pygame Zero. The cost is that it needs a Mac, Windows or Linux computer, and it does not run on an iPad.
4. **No-install fallback for iPad or Chromebook:** the Raspberry Pi Code Editor (editor.raspberrypi.org) and the micro:bit Python editor (python.microbit.org, which has a simulator, buttons, sound and no account). Neither replaces Thonny + Pygame Zero for Scratch-style games.

## ColabTurtlePlus capabilities and gaps

Version 2.2.x (2.2.0 released 2 October 2026; GitHub mentions 2.2.1 in October 2026). Install with `!pip install ColabTurtlePlus`, then `from ColabTurtlePlus.Turtle import *`. It draws as SVG in the cell output.

### Present (verified from the documentation page)

| Area | Functions |
|---|---|
| Motion | `forward/fd`, `backward/bk/back`, `right/rt`, `left/lt`, `goto/setpos/setposition`, `setx`, `sety`, `setheading/face`, `home`, `jumpto/teleport`, `circle`, `regularPolygon` (*) |
| Motion queries | `position/pos`, `xcor/getx`, `ycor/gety`, `heading/getheading`, `towards`, `distance` |
| Pen | `pendown/pd`, `penup/pu/up`, `pensize/width`, `pen`, `isdown`, `dot`, `stamp(layer)`, `clearstamp`, `clearstamps` |
| Colour and fill | `color`, `pencolor`, `fillcolor`, `begin_fill`, `end_fill`, `filling`, `fillrule` (*), `fillopacity` (*), `colormode`, `getcolor(n)` (*) |
| Drawing control | `reset`, `clear`, `delete` (*), `write(obj, align, font)` |
| Visibility and appearance | `showturtle/st`, `hideturtle/ht`, `isvisible`, `shape`, `shapesize/turtlesize`, `shearfactor`, `tilt`, `tiltangle` |
| Built-in shapes | classic, arrow, triangle, square, circle, blank, turtle, turtle2, ring |
| Custom shapes | `register_shape/addshape`, `Shape("compound")`, `addcomponent`, `addellipsecomponent`, `addpathcomponent` |
| Screen | `setup`, `mode`, `bgcolor`, `window_width`, `window_height`, `setworldcoordinates`, `showborder`, `hideborder`, `initializeTurtle`, `clearscreen`, `resetscreen`, `turtles`, `drawline/line` (*) |
| Animation | `speed` (1 to 13, or 0 for no animation; with 0 you must call `done()`), `delay(seconds)`, `animationOn`, `animationOff`, `done/update` |
| Output | `showSVG`, `saveSVG`, `savePNG` |
| Many sprites | `Turtle()` objects and `clone()` (object-oriented interface only) |

(*) = not in classic `turtle.py`, or has extra parameters.

### Missing (absent from the docs; the README says most omissions are "for user events, special turtle methods, and screen methods")

- **Events:** `onkey`, `onkeypress`, `onkeyrelease`, `listen`, `onclick`, `onscreenclick`, `onrelease`, `ondrag`, `ontimer`, `mainloop`/`exitonclick`. There is no way to react to keys or mouse during a run.
- **Input dialogs:** `textinput`, `numinput`. Plain `input()` works in a Colab cell as the workaround for Scratch's "ask and wait" (unverified that it works mid-drawing; the drawing appears as the cell runs).
- **Screen:** `bgpic` (no background images), `tracer` (use `speed(0)` + `done()` or `animationOff()` instead), `undo`, `shapes()` listing.
- **Images:** `register_shape` does not accept image files, so there are no costume pictures.
- **Sound:** none. In Colab, `IPython.display.Audio(...)` can play a file or a generated tone, but only as a separate player widget, not tied to the turtle (unverified for the workbook).

### Behaviour differences and known issues (verified unless marked)

- Fill follows SVG rules, so self-crossing shapes can fill differently from classic turtle. The default fill rule is described inconsistently in the docs (`evenodd` globally versus `nonzero` per fill).
- `circle(r, steps=n)` honours `steps` only up to 20. Above that it draws a smooth arc.
- `stamp()` defaults to `layer=0`, so a later fill can cover a stamp. Use `stamp(layer=1)` to keep it on top.
- Variables persist between cells until the runtime restarts. Start every drawing cell with `clearscreen()` (or `initializeTurtle()`) so a re-run starts clean.
- Version 2.1.2 fixed a bug where several turtles sharing one shape failed. Keep the version pinned (`!pip install ColabTurtlePlus==2.2.0`) so the workbook behaves the same every time.
- Each new Colab runtime forgets the install, so the `!pip install` cell must be run first each session.
- A drawing is finished output, not a live stage. There is no game loop, and a `while True:` loop just freezes the cell. A "forever" can be shown only as a loop with a fixed count (`for i in range(200):`).

### Other Colab turtle ports (for comparison)

| Port | Status | Events? | Notes |
|---|---|---|---|
| ColabTurtle (original, tolgaatam) | Old, the base that ColabTurtlePlus extends | No | Fewer functions, no fill (unverified detail). ColabTurtlePlus supersedes it. |
| ipyturtle / ipyturtle3 | ipyturtle3 is on PyPI, built on ipycanvas | Limited (unverified) | Needs a widget extension, which is awkward in Colab. Aimed at JupyterLab and VS Code. |
| jupyturtle (Allen Downey) | SVG, few dependencies | No | Made for *Think Python* 3rd ed. Fine for drawing, no events. |
| mobilechelonian | Old Jupyter widget | No | Unmaintained (unverified). Not recommended. |

None of these fixes the events gap in a notebook. The notebook model (run a cell, see the result) does not fit "when key pressed".

## Tool matrix

Key: Yes / Partial / No / ? (unverified).

| Tool | Cost | Install? | iPad / Chromebook | Turtle graphics | Keys / mouse events | Sound | Animation / game loop | Accounts and child safety | Saving work | Status 2026 |
|---|---|---|---|---|---|---|---|---|---|---|
| **Colab + ColabTurtlePlus** | Free | No (pip in a cell) | Chromebook yes; iPad works in a browser but editing is fiddly | Yes, rich (SVG) | **No** | No (only an IPython Audio widget) | Animated drawing only; no live loop | Needs a Google account; a child under 13 needs a Family Link or school account, or uses a parent's | Google Drive, automatic | Maintained |
| Colab + other ports | Free | No | As above | Partial | No | No | No | As above | Drive | Mixed or old |
| **Thonny** | Free, open source | Yes (Mac, Windows, Linux) | No iPad; Chromebook only through Linux (Crostini) | Yes, full standard `turtle` | **Yes** (`turtle.onkey`, `onclick`, `ontimer`; Pygame Zero hooks) | Yes through Pygame Zero (`sounds`, `music`) | Yes (`ontimer` loops; Pygame Zero `update()` at about 60 fps) | No account, offline; nothing leaves the computer | Local `.py` files | Maintained (5.0.0, April 2026) |
| IDLE | Free, ships with Python | Python install | No | Yes, full `turtle` (+ `turtledemo`) | Yes (turtle events) | No | `ontimer` | None | Local files | Maintained, but plain for a child; no debugger view like Thonny |
| Mu editor (Pygame Zero mode) | Free | Yes | No | Yes | Yes | Yes | Yes | None | Local | **Archived 31 Aug 2025**; still runs, no fixes |
| Trinket.io | Was freemium | No | Was yes | Was yes (Skulpt, with events) | Was yes | Partial | Was partial | Accounts | Cloud | **Shut down 31 Aug 2026**; community copy at trinket.strivemath.org with no guarantee |
| Replit | Free tier + paid | No | Yes (browser and app) | Yes (real Python, graphical output) | Yes (unverified on free tier) | Partial | Yes | Terms say not directed at under-13s; reported 13+ with parental consent. Public projects and AI agent features make it unsuitable for a 9-year-old alone | Cloud | Pivoted to AI app-building |
| Code.org | Free | No | Yes | No Python turtle (its Python lab is newer and limited, unverified) | ? | ? | ? | Child-safe, teacher sections | Cloud | Maintained |
| EduBlocks | Free | No | Yes, partial mobile support | Python blocks; turtle mode ? (not found in 2025 to 2026 sources) | Partial ? | ? | ? | Optional account, classrooms | Cloud | Maintained (Anaconda); runs Python in the browser through PyScript |
| BlockPy | Free | No | Yes | Partial (Skulpt turtle, unverified) | No | No | No | Course or LTI oriented | Cloud | Academic tool, mainly for data and assignments |
| Python Tutor | Free | No | Yes | **No** graphics | No | No | No | No account | Share link | Maintained; for *seeing* variables and loops step by step |
| JupyterLite | Free | No | Yes (heavy on iPad) | Partial (jupyturtle-style SVG ports) | No | No | No | No account | Browser storage only (easy to lose) | Maintained |
| Raspberry Pi Code Editor | Free (charity) | No | **Yes** | Partial ? (p5/py5 drawing confirmed by press; turtle not confirmed) | Partial (p5-style key and mouse functions, unverified) | ? | Partial (p5 `draw()` loop) | Raspberry Pi Foundation account for saving; designed for young people, 13+ rules for some features (unverified) | Cloud (account) or download | Maintained |
| Pyodide / Skulpt pages | Free | No | Yes | Depends on the page | Depends | Rare | Depends | Depends | Usually none | Building blocks, not a learner tool |
| micro:bit Python editor | Free | No | **Yes**; simulator, no board needed | No turtle (5x5 LED grid) | Buttons A/B, shake, tilt (in the simulator) | **Yes** (`music`, `speech`; the simulator plays sound) | Yes (`while True` with `sleep`) | No account | Downloads `.hex` / `.py`, browser storage | Maintained (Micro:bit Educational Foundation) |

## Scratch-category support matrix (top 4 tools)

Top 4 for this child: **Colab + ColabTurtlePlus** (current), **Thonny + turtle**, **Thonny + Pygame Zero**, **micro:bit Python editor** (no-install, browser-based fallback). Trinket and Mu are left out because one has shut down and the other is unmaintained.

Key: **Full** = every everyday block in the category has a direct Python match; **Partial** = some blocks or a workaround; **No** = not possible.

| Scratch category | Colab + ColabTurtlePlus | Thonny + `turtle` | Thonny + Pygame Zero | micro:bit editor |
|---|---|---|---|---|
| Motion (move, turn, go to x:y, glide, point towards, bounce) | **Full** except "bounce" and "glide", which you write yourself | **Full** (same; glide = loop + `ontimer`) | **Full** (`Actor.x/y`, `angle`, `animate()` for glide) | No (LED pixels only) |
| Looks (costume, say/think, size, colour effect, show/hide, layers) | Partial: `shape`, `shapesize`, `color`, `write` for "say", `hideturtle`; no image costumes, no layers except `stamp(layer)` | Partial: GIF costumes through `register_shape("x.gif")`; `write` for "say" | **Full** (`Actor('image')`, swap `.image` for costumes, `screen.draw.text` for "say", draw order = layers) | Partial (`display.show`, `display.scroll`, images) |
| Sound (play, drum, note, volume) | **No** | No (standard library only; a beep through `print('\a')` at most) | **Full**-ish (`sounds.pop.play()`, `music.play()`, `tone.play()`, volume) | **Full** for notes and melodies (`music.play`, `music.pitch`, `speech`, `audio`) |
| Events (green flag, key pressed, sprite clicked, broadcast, timer) | Partial: green flag = run cell; **no keys, no clicks, no timer** | **Full** (`onkey`, `onclick`, `onscreenclick`, `ontimer`, `listen`, `mainloop`); broadcast = calling a function | **Full** (`on_key_down`, `on_mouse_down` + `actor.collidepoint`, `clock.schedule`) | Partial (buttons, gestures; `button_a.was_pressed()` in a loop) |
| Control (wait, repeat, forever, if, wait until, stop, clones) | Partial: `repeat`, `if`, `for` fine; `forever` only as a long fixed loop; `wait` = `time.sleep` | **Full** (forever = `ontimer` loop) | **Full** (`update()` is forever; `clock.schedule` = wait) | **Full** (`while True`, `sleep`) |
| Sensing (touching, key pressed?, mouse x/y, ask and wait, timer, distance) | Partial: `distance`, `towards`, `xcor`; `input()` for "ask"; no mouse, no key state | Partial: `distance`; touching = distance check; mouse position only through clicks; `textinput` for "ask" | **Full** (`colliderect`, `keyboard.left`, `on_mouse_move(pos)`, `time` for timer) | Partial (accelerometer, light, temperature, buttons) |
| Operators | **Full** | **Full** | **Full** | **Full** |
| Variables and lists | **Full** | **Full** | **Full** | **Full** |
| My Blocks | **Full** (`def`) | **Full** | **Full** | **Full** |
| Pen | **Full** (best of all: fill, stamp, opacity, SVG export) | **Full** | Partial (draw on screen each frame; no lasting pen trail without extra code) | No |
| Clones | Partial (`clone()` or many `Turtle()` objects; no "when I start as a clone") | Partial (`clone()`, lists of turtles) | **Full** (a list of `Actor`s, add and remove inside `update()`) | No |

## Recommendation

1. **Keep Colab + ColabTurtlePlus for the first half of the workbook:** Motion, Pen, Looks-as-drawing, Operators, Variables, Lists, Control (repeat and if), My Blocks, and many turtles with `clone()`. It needs no install, saves to Drive automatically and works on a Chromebook. Its SVG output and `fill`, `stamp` and `write` make good-looking results. Pin the version, start every cell with `clearscreen()`, and use `input()` for "ask and wait". Tell the child plainly that Colab cannot do "when key pressed", so they will not think they made a mistake.
2. **Second tool for key-press games: Thonny**, in two steps:
   - **Step A (same turtle they know):** run the same `turtle` code in Thonny, then add `screen.listen()`, `screen.onkey(up, "Up")` and `screen.ontimer(loop, 20)`. The commands are the same and only the place changes. This teaches Scratch's Events directly.
   - **Step B (real games): Pygame Zero** through *Run → Pygame Zero mode*. `Actor` = sprite, `update()` = forever, `on_key_down` = "when key pressed", `sounds.x.play()` = Sound, and a list of Actors = clones. This is the closest Scratch-shaped game model in Python.
   - Why Thonny over the others: it is free, offline, needs no account (best for child safety) and is still maintained. It has a beginner variable view and a step debugger that work like Python Tutor's visuals. Mu is archived, Trinket has shut down, and Replit is not aimed at under-13s.
   - Caveat: a reported Thonny issue (#3158) gives an AST error in Pygame Zero mode on newer Python versions. Test the exact Thonny 5.x + pgzero pairing on the family computer before writing the chapter. Fallback: run `pgzrun game.py` from Thonny's system shell, or use plain `pygame` in Thonny.
3. **If only an iPad or Chromebook is available:** use the micro:bit Python editor's simulator for Events, Sound and forever loops, and keep Colab for drawing. Try the Raspberry Pi Code Editor for p5-style animation once its key-event support is confirmed by hand.
4. **Python Tutor as a side tool:** paste short non-graphics snippets in to *see* variables and loops change. This helps with the Variables and Control chapters. It cannot run turtle.

## Sources

- ColabTurtlePlus on PyPI: https://pypi.org/project/ColabTurtlePlus/
- ColabTurtlePlus on GitHub: https://github.com/mathriddle/ColabTurtlePlus
- ColabTurtlePlus documentation (full function list): https://larryriddle.agnesscott.org/ColabTurtlePlus/documentation2.html
- ColabTurtlePlus issues: https://github.com/mathriddle/ColabTurtlePlus/issues
- Trinket shutdown notice: https://shutdown.trinket.io/
- Trinket announcement: https://trinket.io/announcement
- Trinket closure coverage: https://craigndave.org/trinket-is-shutting-down-in-june-2026/ ; https://teachcomputing.org/blog/trinket-to-ide
- Mu editor (archived): https://github.com/mu-editor/mu/ ; https://codewith.mu/
- Thonny: https://thonny.org/ ; releases https://github.com/thonny/thonny/releases ; Pygame Zero mode issue https://www.github.com/thonny/thonny/issues/3158
- Pygame Zero setup in Thonny (third-party guide): https://www.phidgets.com/education/learn/projects/pygame-zero-projects/install-setup/
- Pygame Zero event hooks: https://pygame-zero.readthedocs.io/en/stable/hooks.html
- Python turtle (standard library): https://docs.python.org/3/library/turtle.html
- Raspberry Pi Code Editor: https://editor.raspberrypi.org/ ; source https://github.com/RaspberryPiFoundation/editor-ui ; launch review https://www.reviewgeek.com/150725/raspberry-pi-debuts-a-code-editor-for-young-people
- micro:bit Python editor: https://python.microbit.org/v/3
- EduBlocks: https://app.edublocks.org/ ; https://www.anaconda.com/blog/anaconda-empowers-education-with-new-edublocks-release-featuring-classrooms-mobile-support-and-more ; https://programme.europython.eu/europython-2025/talk/3BQFTP/
- BlockPy: https://blockpy.cis.udel.edu/ ; https://github.com/technologiclee/blockpy
- Python Tutor: https://pythontutor.com/
- Replit terms (secondary trackers): https://conductatlas.com/platform/replit/replit-terms-of-service/ ; https://conductatlas.com/platform/replit/replit-privacy-policy/services-not-directed-to-children-under-13/
- ipyturtle3: https://pypi.org/project/ipyturtle3/ ; jupyturtle: https://github.com/AllenDowney/jupyturtle
- JupyterLite: https://jupyterlite.readthedocs.io/
- Code.org: https://code.org/
