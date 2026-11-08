# 13. Scratch extensions (other than Pen) mapped to Python

Research dimension: the Scratch 3.0 Extensions Library (the blue "Add Extension" button, bottom left of the editor), excluding Pen. Each extension is treated as an idea for a Python library. Audience: a 9-year-old who knows Scratch and is learning Python in Google Colab.

Researched 7 Nov 2026 from the Scratch Wiki and the Scratch source code (scratch-vm). Sound and speech code was tested on macOS with Python 3 and numpy 2.3.1.

---

## Summary

- Scratch 3.0 has **12 official extensions**: Music, Pen, Video Sensing, Face Sensing, Text to Speech, Translate, Makey Makey, micro:bit, LEGO MINDSTORMS EV3, LEGO BOOST, LEGO Education WeDo 2.0 and Go Direct Force & Acceleration. **Face Sensing is now on the main site.** It was in Scratch Lab from Feb 2021 and was added to Scratch on 7 Oct 2025.
- **Music works best in Colab.** The Music extension is a small set of rules: a note number, a beat count and a tempo. Seconds = 60 / tempo x beats, and note 60 is middle C. It maps almost one-to-one to about 15 lines of numpy plus `IPython.display.Audio`. I tested this: a 3.5-beat tune at tempo 120 made a WAV of exactly 1.75 s, and note 60 gave 261.63 Hz. This is the best "extension as a Python library" project for the child. Rating **5/5**.
- **Text to Speech and Translate both use online services, in Scratch too.** Scratch sends text to `synthesis-service.scratch.mit.edu` (128-character limit, 5 voices) and to `translate-service.scratch.mit.edu`. In Colab, gTTS (Text to Speech) works well. Translation needs a third-party package and can break without warning.
- **Colab is a computer far away (a cloud server).** It cannot reach the child's webcam live, their keyboard in real time, Bluetooth, or USB. So **all six hardware extensions** (micro:bit, EV3, BOOST, WeDo 2.0, Go Direct, Makey Makey) and the live camera extensions (**Video Sensing, Face Sensing**) **need a different tool from Colab**. The friendliest is the micro:bit Python Editor (python.microbit.org), which runs in the browser and has a simulator, so no hardware is needed. For LEGO, the path is Pybricks (BOOST Move Hub) or LEGO's EV3 MicroPython.
- The **Makey Makey only pretends to be a keyboard** (space, arrows, w a s d f g). Any Python program that listens for those keys works with it unchanged, but only in a local window (turtle, pygame, Pygame Zero), not in Colab.

---

## Extension-by-extension mapping table

Rating = how suitable for a 9-year-old **in Colab** (5 = great, 1 = not workable there). Where Colab fails, the "Best non-Colab path" column gives the friendliest option.

| Extension | Scratch blocks (what they do) | Friendliest Python path | Colab rating | Best non-Colab path / notes |
|---|---|---|---|---|
| **Music** | `play drum () for () beats`, `rest for () beats`, `play note () for () beats`, `set instrument to ()`, `set tempo to ()`, `change tempo by ()`, `(tempo)`. 21 instruments, 18 drums. Notes 0 to 130 (60 = middle C). Tempo 20 to 500, default 60. Beats 0 to 100. | numpy sine waves (frequency = 440 x 2^((note-69)/12)) joined with `np.concatenate`, played by `IPython.display.Audio(song, rate=22050)`. Drums = a short burst of random noise that fades out. "Instruments" = different waveforms (square, sawtooth) or volume envelopes. Optional later: `music21` or MIDI files. | **5** | Works anywhere. Sound plays after the cell finishes, not note by note. See gotchas. |
| **Text to Speech** | `speak ()` (waits until finished), `set voice to ()` (alto, tenor, squeak, giant, kitten), `set language to ()` (about 23 languages). Text is cut off after 128 characters. | `!pip install gTTS`, then `gTTS("Hello", lang="en").save("hi.mp3")` and `Audio("hi.mp3", autoplay=True)`. Languages: `lang="fr"`, `"es"` and many more (list them with `gtts-cli --all`). No voice choice, but `tld="co.uk"` or `"com.au"` changes the accent. | **4** | Mac: `os.system('say -v Albert "hello"')` (tested; `say -v '?'` lists the voices, and some are silly ones like the kitten/giant voices). Offline on Windows/Linux: `pyttsx3`. |
| **Translate** | `translate () to ()` (reporter), `(language)` (the viewer's language). Uses Google Translate through a Scratch server. Numbers are returned unchanged. Returns empty text on error. | `!pip install deep-translator`, then `GoogleTranslator(source="auto", target="fr").translate("hello")`. Honest note: it is an unofficial wrapper around a web service. It needs internet, can be rate-limited and may break. For a child, a hand-made **dictionary** (`{"hello": "bonjour"}`) is a better first lesson. | **3** | Same everywhere. Good moment to teach "your words are sent to someone else's computer". |
| **Video Sensing** | `when video motion > ()` (hat), `video (motion/direction) on (sprite/stage)`, `turn video (on/off/on flipped)`, `set video transparency to ()`. Motion = how many pixels changed between frames. | OpenCV (`cv2`) with frame differencing: `cv2.absdiff(frame1, frame2)` then count changed pixels. In Colab you can only take **single snapshots** with a JavaScript helper (the "Camera Capture" code snippet), not a live stream. | **1** | Honestly too advanced at 9 if done from scratch. Locally, an adult can set up a 20-line OpenCV script that prints "motion!". Simpler in Colab: compare two still photos and count the different pixels with numpy. |
| **Face Sensing** (main site since Oct 2025) | `go to (nose/...)`, `point in direction of face tilt`, `set size to face size`, `when face tilts ()`, `when this sprite touches a ()`, `when a face is detected`, `<a face is detected?>`, `(face tilt)`, `(face size)`. Uses Google's BlazeFace model, which runs on the device. | MediaPipe Face Detection (also BlazeFace) or OpenCV Haar cascades, run on a **photo** in Colab (draw a box on the face, print its size). | **2** | Live tracking needs a local webcam and adult setup. Privacy talk: Scratch keeps faces on the device; tell the child to use photos of themselves only, with permission. |
| **micro:bit** | `when (A/B/any) button pressed`, `<(A) button pressed?>`, `when (moved/shaken/jumped)`, `display (pattern)`, `display text ()`, `clear display`, `when tilted (front/back/left/right/any)`, `<tilted ()?>`, `(tilt angle ())`, `when pin (0/1/2) connected`. Uses Bluetooth through Scratch Link. | **MicroPython** in the official **micro:bit Python Editor** (python.microbit.org). `from microbit import *`, `display.scroll("Hi")`, `display.show(Image.HAPPY)`, `button_a.was_pressed()`, `accelerometer.was_gesture("shake")`, `accelerometer.get_x()`, `pin0.is_touched()`. Every Scratch block has a direct equivalent. | **1** (Colab cannot reach it) | **5 in its own editor.** It has a built-in simulator (no board needed), drag-in code snippets and child-friendly docs. Note: Scratch uses a special Scratch hex file, while Python flashes its own program, so the board does one or the other at a time. |
| **LEGO MINDSTORMS EV3** | `motor (A-D) turn this way/that way for () seconds`, `motor () set power () %`, `(motor () position)`, `when button (1-4) pressed`, `when distance < ()`, `when brightness < ()`, `<button () pressed?>`, `(distance)`, `(brightness)`, `beep note () for () secs`. | **LEGO Education EV3 MicroPython** (Pybricks v2 on an ev3dev microSD card, edited in VS Code). `Motor(Port.A).run_time(500, 1000)`, `UltrasonicSensor(Port.S4).distance()`, `ev3.speaker.beep()`. | **1** | **3** with an adult: it needs a microSD card and VS Code setup. EV3 is a retired product. Newer Pybricks versions no longer support EV3. |
| **LEGO BOOST** | `turn motor (A/B/C/D/AB/ABCD) for () seconds` / `for () rotations`, `turn motor () on/off`, `set motor () speed to () %`, `set motor () direction ()`, `(motor () position)`, `when (colour) brick seen`, `<seeing () brick?>`, `when tilted ()`, `(tilt angle ())`, `set light color to ()`. | **Pybricks** (code.pybricks.com in Chrome or Edge, over Bluetooth). `from pybricks.hubs import MoveHub`, `from pybricks.pupdevices import Motor, ColorDistanceSensor`, `Motor(Port.A).run_angle(500, 360)`. | **1** | **4**: browser-based, no install, fully reversible (you can restore the original LEGO firmware). The Move Hub has the least memory of the Pybricks hubs. BOOST is retired, so it is mostly for families who already have one. |
| **LEGO Education WeDo 2.0** | `turn (motor) on for () seconds`, `turn () on/off`, `set () power to ()`, `set () direction to ()`, `set light color to ()`, `when distance (< / >) ()`, `when tilted ()`, `(distance)`, `<tilted ()?>`, `(tilt angle ())`. | No official Python path found. Pybricks lists City, Technic, Move, Inventor, Prime and Essential hubs, **not WeDo 2.0** (I could not confirm any support). Community Bluetooth libraries exist but are not suitable for a child. | **1** | **1**: stay in Scratch for WeDo. A child who wants Python with LEGO should move to SPIKE Essential/Prime (LEGO's own SPIKE Python, or Pybricks). |
| **Go Direct Force & Acceleration** (Vernier) | `when (shaken/started falling/turned face up/turned face down)`, `when force sensor (pushed/pulled)`, `(force)`, `when tilted ()`, `<tilted ()?>`, `(tilt angle ())`, `<falling?>`, `(spin speed (x/y/z))`, `(acceleration (x/y/z))`. Range ±50 N, ±16 g. | Vernier's `godirect` package (`pip install godirect`), with Vernier's simpler `gdx` helper module from their examples. It reads the sensor over USB or Bluetooth on Windows, macOS or Linux. The data can then be plotted with matplotlib. | **1** (Colab has no USB/Bluetooth) | **2** locally with an adult. Nice bridge to **Colab**: record the data locally into a CSV, then plot "how hard did I push?" in Colab. |
| **Makey Makey** | `when (space/up/down/left/right/w/a/s/d/f/g) key pressed`, `when (sequence) pressed in order` (for example "left up right", or "up up down down left right left right"). | The Makey Makey **is a USB keyboard**, so no library is needed. Locally: `turtle.onkey(jump, "space")` + `turtle.listen()`, or `pygame` / Pygame Zero `on_key_down`. Sequences = keep a list of the last N keys and compare it with the target list. | **1** (Colab gets no live key presses; `input()` + Enter is the only way) | **4** locally with turtle (part of standard Python, no install): banana piano or play-dough game controller. In Colab, the *idea* of sequences can be practised with a list and `input()`. |

---

## Gaps and gotchas

1. **Colab plays sound only once the whole cell has finished.** `Audio()` makes a player widget, which waits until the cell ends. So a Scratch `forever` loop of notes or "play a note when the sprite moves" does not carry over. Teach the "build the whole song as a list of notes, then play it" pattern. Also, `IPython.display.Audio` rescales the array's volume to the loudest point automatically (pass `normalize=False` to stop it).
2. **There is no "say while moving" in Colab.** Scratch's `speak` waits until speech ends. gTTS makes an MP3 file instead. Voices like "kitten" or "giant" have no gTTS equivalent. On a Mac, `say -r 300` (fast) or `say -v` with a novelty voice comes close.
3. **Some features need internet and a pip install.** gTTS and deep-translator need `!pip install` in each new Colab session (packages vanish when the runtime resets). Translate wrappers are unofficial, and Google can rate-limit them or change them without warning. Scratch hides this by using its own servers. In Python the child sees the plumbing, which is a useful lesson.
4. **Colab cannot see the child's devices.** Webcam (live), keyboard (live), microphone (live), Bluetooth and USB are all on the *child's* computer, while the Python is running on Google's. This one idea explains why 8 of the 11 extensions do not belong in Colab. Make it an explicit lesson, not a surprise.
5. **There is a different Python for each device.** micro:bit, LEGO and EV3 run **MicroPython**, a small Python that lives on the board. Lists, loops, `if` and functions are the same, but there is no numpy or `pip`, and each board has its own modules (`microbit`, `pybricks`). Say clearly: "same language, different toolbox".
6. **Scratch blocks pause the script; Python needs you to wait or loop yourself.** Hat blocks like "when button pressed" become `while True:` loops that check `was_pressed()` again and again (micro:bit), or callback functions (turtle `onkey`). This is the biggest change in thinking for hardware.
7. **The Scratch and Python micro:bit programs replace each other.** To use the board with Scratch again after Python, re-flash the Scratch micro:bit hex file (from scratch.mit.edu/microbit). Pybricks on BOOST also replaces the LEGO firmware (it can be put back with the LEGO app).
8. **Retired products.** EV3, BOOST and WeDo 2.0 are discontinued by LEGO, and newer Pybricks dropped EV3. Do not buy hardware for this. Use what the family has, or the micro:bit simulator.
9. **Video and Face Sensing are hard to do honestly.** OpenCV and MediaPipe are big libraries with confusing installation and image arrays (rows, columns, colour channels). For a 9-year-old, a pre-written helper that an adult provides (`motion = how_much_changed(photo1, photo2)`) is fine. Writing it from scratch is not. Privacy: use only photos of the child taken with permission.
10. **Scratch note numbers are MIDI note numbers.** Scratch's "note 60" is the same as the MIDI note 60 used by music software. Keep the same numbers in Python so the child can move a Scratch tune across without changing anything.

### Tested code (macOS, numpy 2.3.1, works the same in Colab)

```python
import numpy as np
from IPython.display import Audio

RATE = 22050
tempo = 120                      # like "set tempo to 120"

def note_freq(note):             # Scratch note 60 = middle C
    return 440 * 2 ** ((note - 69) / 12)

def play_note(note, beats):      # like "play note 60 for 0.5 beats"
    secs = 60 / tempo * beats
    t = np.linspace(0, secs, int(RATE * secs), endpoint=False)
    fade = np.minimum(1, np.minimum(t, secs - t) * 50)   # stops clicks
    return np.sin(2 * np.pi * note_freq(note) * t) * fade

def rest(beats):                 # like "rest for 0.5 beats"
    return np.zeros(int(RATE * 60 / tempo * beats))

def drum(beats):                 # noise that fades = a snare-ish drum
    n = int(RATE * 60 / tempo * beats)
    return np.random.uniform(-1, 1, n) * np.exp(-np.linspace(0, 30, n))

song = np.concatenate([play_note(60, .5), play_note(62, .5), play_note(64, .5),
                       rest(.5), drum(.5), play_note(67, 1)])
Audio(song, rate=RATE)           # in Colab this shows a play button
```

Result of the test: 1.75 s of audio (3.5 beats at tempo 120, which matches Scratch's rule), 261.63 Hz for note 60, written to a valid 22050 Hz WAV file. `say -o hello.aiff "Hello from Python"` also worked on macOS.

---

## Teaching ideas for a 9-year-old

**Analogy: extensions are "plug-in toolboxes".** In Scratch you click "Add Extension" and a new colour of blocks appears. In Python you write `import` (or `!pip install` first, which is like fetching the toolbox from the shop) and new commands appear. `from microbit import *` is "Add Extension: micro:bit". And just as some Scratch toolboxes need a gadget plugged in, some Python toolboxes only work on the computer the gadget is plugged into. Colab is a computer far away, so it cannot feel your banana.

**Mini-challenge 1: Build your own Music extension (Colab, 30 to 45 min).**
Give the child `play_note`, `rest` and `tempo` (above) and ask them to:
(a) play "Twinkle Twinkle" (60 60 67 67 69 69 67) as a list of note numbers in a `for` loop,
(b) change the `tempo` and hear it speed up, just like `change tempo by 20`,
(c) bonus: write their own `play_drum()` and make a beat with `*` list repetition.
This shows that a Scratch extension is "just functions someone wrote", and now they are that someone.

**Mini-challenge 2: The talking, translating parrot (Colab, 20 min).**
Step 1: make a dictionary translator `{"hello": "bonjour", "cat": "chat"}` and look words up with `input()`.
Step 2: send the answer to gTTS with `lang="fr"` so the computer says it in French.
Step 3 (optional, with an adult): swap the dictionary for `deep-translator` and talk about why that needs the internet.

**Mini-challenge 3: micro:bit pet (micro:bit Python Editor, simulator is fine).**
Rebuild a familiar Scratch micro:bit project in MicroPython. Show `Image.HAPPY`. When shaken, show `Image.SURPRISED` and scroll "Whee!". When button A is pressed, add 1 to a `food` variable and show it. Run it in the on-screen simulator: they can click the virtual buttons and "shake" it with the mouse. No hardware needed.

(Optional extra if a Makey Makey is in the house: a banana piano with turtle `onkey` on the local computer, with each key playing a note made by the Music code above saved as a WAV.)

---

## Sources

- Scratch Wiki, Extension list: https://en.scratch-wiki.info/wiki/Extension
- Scratch Wiki, Music Extension: https://en.scratch-wiki.info/wiki/Music_Extension
- Scratch Wiki, Video Sensing Extension: https://en.scratch-wiki.info/wiki/Video_Sensing_Extension
- Scratch Wiki, Face Sensing Extension: https://en.scratch-wiki.info/wiki/Face_Sensing_Extension
- Scratch Wiki, Makey Makey Extension: https://en.scratch-wiki.info/wiki/Makey_Makey_Extension
- scratch-vm source, Music: https://github.com/scratchfoundation/scratch-vm/blob/develop/src/extensions/scratch3_music/index.js
- scratch-vm source, Text to Speech: https://github.com/scratchfoundation/scratch-vm/blob/develop/src/extensions/scratch3_text2speech/index.js
- scratch-vm source, Translate: https://github.com/scratchfoundation/scratch-vm/blob/develop/src/extensions/scratch3_translate/index.js
- scratch-vm source, micro:bit: https://github.com/scratchfoundation/scratch-vm/blob/develop/src/extensions/scratch3_microbit/index.js
- scratch-vm source, Makey Makey: https://github.com/scratchfoundation/scratch-vm/blob/develop/src/extensions/scratch3_makeymakey/index.js
- scratch-vm source, EV3: https://github.com/scratchfoundation/scratch-vm/blob/develop/src/extensions/scratch3_ev3/index.js
- scratch-vm source, BOOST: https://github.com/scratchfoundation/scratch-vm/blob/develop/src/extensions/scratch3_boost/index.js
- scratch-vm source, WeDo 2.0: https://github.com/scratchfoundation/scratch-vm/blob/develop/src/extensions/scratch3_wedo2/index.js
- scratch-vm source, Go Direct Force & Acceleration: https://github.com/scratchfoundation/scratch-vm/blob/develop/src/extensions/scratch3_gdx_for/index.js
- micro:bit Python Editor: https://python.microbit.org
- Scratch micro:bit setup page: https://scratch.mit.edu/microbit
- Pybricks supported hubs: https://docs.pybricks.com/en/stable/hubs/index.html
- Pybricks Move Hub (BOOST): https://docs.pybricks.com/en/v3.4.1/hubs/movehub.html
- Pybricks MicroPython repo (EV3/ev3dev status): https://github.com/pybricks/pybricks-micropython
- Brickset, Pybricks overview: https://brickset.com/article/84862/get-the-most-out-of-your-smart-hubs-with-pybricks
- Vernier godirect Python library: https://github.com/vernierst/godirect-py and https://pypi.org/project/godirect/
- Vernier Python page: https://www.vernier.com/engineering/python/
- Vernier GDX-FOR manual: https://www.vernier.com/manuals/gdx-for
- gTTS: https://pypi.org/project/gTTS/
- deep-translator: https://pypi.org/project/deep-translator/
