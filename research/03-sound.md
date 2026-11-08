# 03 Sound blocks: Scratch 3.0 to Python

## Summary

Scratch has 9 Sound blocks: 8 stack blocks and 1 reporter (`volume`). They are pink/magenta. The scratch-blocks source gives the category colour as `#CF63CF` (primary), `#C94FC9` (secondary) and `#BD42BD` (tertiary). These hex values come from my knowledge of `scratch-blocks/core/colours.js`. The Wiki only says "pink", and I could not re-fetch the source file because it has moved.

Python has **no built-in sound**. Each target needs its own approach:

- **Google Colab (main target):** you can't play sound from the Python process. The sound has to be sent to the browser as an `IPython.display.Audio` widget with `autoplay=True`. Python can make the sound itself (as a numpy array or a WAV file) or load a file or URL.
- **Desktop (IDLE/Thonny):**
  - Windows has `winsound` built in.
  - macOS can run `afplay` through `subprocess`.
  - Cross-platform needs `pygame.mixer`, which is the closest match to Scratch: it has a channel volume and stereo pan, and non-blocking playback is the default.

The key idea to teach is **"play sound until done" = blocking (wait)** and **"start sound" = non-blocking (carry on)**. On the Mac I measured `subprocess.run(["afplay", f])` waiting 1.35 s for a 0.3 s file (most of that is startup), while `subprocess.Popen([...])` returned in 0.006 s.

Exact Scratch numbers, checked in the scratch-vm and scratch-audio source:
- **Volume:** 0 to 100, clamped.
- **Pitch effect:** −360 to +360. **10 units = 1 semitone**, so 120 = 1 octave. The formula is `ratio = 2 ** ((pitch/10)/12)`.
- **Pan:** −100 (left) to +100 (right).
- **Per sprite:** effects and volume belong to each sprite. A clone gets a *copy* of its parent's effects when it is created.
- **Reset:** the green flag and the stop sign reset effects. `stop all sounds` does **not** reset them.
- **Timing:** the volume and effect blocks wait one frame.

## Block-by-block mapping table

All Python examples below were tested on macOS with Python 3.13, unless marked "not tested".

| Scratch block (pink `#CF63CF`) | Shape | What it does | Colab equivalent | Desktop equivalent |
|---|---|---|---|---|
| `play sound (Meow v) until done` | stack | Plays the sound and **waits** until it ends | `display(Audio(data, rate=R, autoplay=True)); time.sleep(seconds)`. There is no real "until done", so you sleep for the sound's length yourself. | Win: `winsound.PlaySound("meow.wav", winsound.SND_FILENAME)` (blocks) or `winsound.Beep(440, 500)`. Mac: `subprocess.run(["afplay", "meow.wav"])`. pygame: `ch = snd.play(); while ch.get_busy(): time.sleep(0.01)` |
| `start sound (Meow v)` | stack | Starts the sound, **script carries on** at once | `display(Audio(..., autoplay=True))` with no sleep. Several sounds can overlap. | Win: `PlaySound(f, SND_FILENAME \| SND_ASYNC)`. Mac: `p = subprocess.Popen(["afplay", f])`. pygame: `snd.play()` |
| `stop all sounds` | stack | Stops every sound from every sprite | `from IPython.display import clear_output; clear_output()` removes the audio players (it also clears printed text). | Win: `winsound.PlaySound(None, winsound.SND_PURGE)`. Mac: `p.terminate()` for each Popen you kept. pygame: `pygame.mixer.stop()` |
| `change [pitch v] effect by (10)` | stack | Raises pitch by 1 semitone per 10 (also makes the sound faster/shorter) | Keep a variable `pitch += 10`, then make the tone with `freq = base * 2**((pitch/10)/12)`. For a recorded sound, resample: `Audio(data, rate=int(R * ratio))`, which shifts pitch *and* speed just like Scratch. | Same maths. `winsound.Beep(int(freq), ms)`. Mac: `afplay -r RATE` changes speed, but **not** pitch. pygame has no pitch control, so make a new tone. |
| `change [pan left/right v] effect by (10)` | stack | Moves the sound left (−) or right (+) | Build a stereo array `np.vstack([left*x, right*x])`, where `left = min(1, 1 - pan/100)` and `right = min(1, 1 + pan/100)` | pygame: `ch.set_volume(left, right)`. winsound/afplay: no pan, so write a stereo WAV with the `wave` module (tested). |
| `set [pitch v] effect to (100)` | stack | Sets pitch directly (−360 to 360) | `pitch = 100`, then as above | as above |
| `set [pan left/right v] effect to (0)` | stack | Sets pan directly (−100 to 100) | `pan = 0`, then as above | as above |
| `clear sound effects` | stack | Pitch = 0 and pan = 0 (volume is untouched) | `pitch = 0; pan = 0` | same |
| `change volume by (-10)` | stack | Changes volume, clamped to 0 to 100 | `volume = max(0, min(100, volume - 10))`, then `Audio(x * volume/100, rate=R, normalize=False)` | pygame: `snd.set_volume(volume/100)`. Mac: `afplay -v 0.5 f`. winsound: no volume control, so scale the samples in the WAV. |
| `set volume to (100)%` | stack | Sets volume | `volume = 100` | as above |
| `(volume)` | reporter (round) | Reports this sprite's volume | `print(volume)`, or just use the variable | pygame: `round(snd.get_volume() * 100)` |

### Tested pure-Python tone maker (works in Colab and on desktop, needs only the standard library)

```python
import math, wave, struct

RATE = 22050

def make_tone(filename, freq=440, seconds=0.5, volume=100, pan=0):
    left  = min(1, 1 - pan/100) * volume/100
    right = min(1, 1 + pan/100) * volume/100
    with wave.open(filename, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(RATE)
        frames = bytearray()
        for i in range(int(RATE * seconds)):
            s = math.sin(2 * math.pi * freq * i / RATE) * 30000
            frames += struct.pack("<hh", int(s * left), int(s * right))
        w.writeframes(frames)

def pitch_to_freq(base, pitch_effect):        # Scratch maths
    return base * 2 ** ((pitch_effect / 10) / 12)
# pitch_to_freq(440, 120) -> 880.0 (one octave);  pitch_to_freq(440, 10) -> 466.16 (one semitone)
```

Colab: `from IPython.display import Audio, display; display(Audio("beep.wav", autoplay=True))`.

### Colab helper that feels like Scratch (numpy, tested)

```python
import numpy as np, time
from IPython.display import Audio, display
R = 22050
volume, pitch, pan = 100, 0, 0

def tone(freq=440, secs=0.4):
    f = freq * 2 ** ((pitch/10)/12)
    t = np.linspace(0, secs, int(R*secs), endpoint=False)
    x = np.sin(2*np.pi*f*t) * volume/100
    left, right = min(1, 1 - pan/100), min(1, 1 + pan/100)
    return np.vstack([x*left, x*right]), secs

def start_sound(freq=440, secs=0.4):
    data, _ = tone(freq, secs)
    display(Audio(data, rate=R, autoplay=True, normalize=False))

def play_sound_until_done(freq=440, secs=0.4):
    start_sound(freq, secs)
    time.sleep(secs + 0.1)          # wait like Scratch does
```

## Gaps and gotchas

**Colab**
- The sound plays in the **browser**, not on the Colab server. Each `display(Audio(...))` adds a small player to the output. Autoplay works because running the cell counts as a user click. Some browsers (Safari, or when the tab is muted) may block it, and the child then has to press play.
- `Audio(numpy_array)` **normalises by default** (`normalize=True`), so quiet sounds get made loud and a "volume" variable does nothing. Use `normalize=False`. Values must then stay between −1 and 1, otherwise you get `ValueError: Audio data must be between -1 and 1 when normalize=False` (tested).
- Stereo means a 2-row array, shape `(2, n)`. A 1-D array is mono, so it has no pan.
- No real "until done": Python finishes the cell *before* the browser starts playing, so you have to `time.sleep()` for the length. Also, all the audio players from one cell may only appear when the cell finishes in some setups. For a tune, it is safer to **join the notes into one array** (`np.concatenate`) and play once.
- `stop all sounds` has no clean equivalent: `clear_output()` removes the players but also wipes the turtle canvas and printed text.
- ColabTurtlePlus has no sound functions, so sound is separate from the turtle.
- gTTS (text-to-speech) needs the internet and a pip install. To make sounds without it, generate tones with numpy, or use `Audio(url=...)` with a sound file the child is allowed to use.

**Windows (IDLE/Thonny)**
- `winsound` is built in. Not tested here because this machine is a Mac.
  - `winsound.Beep(freq, ms)` always blocks.
  - `PlaySound(..., SND_ASYNC)` is non-blocking but plays only **one sound at a time**: a new sound stops the old one.
  - It plays only WAV files and has no volume or pan control.

**macOS**
- `afplay` is built in and was tested.
  - `-v` sets volume (1 is normal).
  - `-r` sets rate, which changes speed only.
  - Use `subprocess.run` to block and `subprocess.Popen` to carry on, then `.terminate()` to stop.
  - Each call has a startup delay of up to about 1 s.

**Everywhere**
- `print("\a")` (the bell) is unreliable. It is silent in IDLE, Thonny and Colab, and only sometimes beeps in a real terminal.
- `pygame.mixer` is the best Scratch match: overlapping sounds, `Sound.set_volume`, `Channel.set_volume(left, right)` for pan, and `mixer.stop()`. But it needs `pip install pygame` (Thonny: Tools > Manage packages), and it has no pitch control.
- `simpleaudio` is archived and has no wheels for recent Python versions. `playsound` 1.3 has known install bugs. Avoid both for a child.
- **Per-sprite state:** Scratch keeps volume and effects for each sprite. In Python they are plain variables (or attributes on a class), and the child must reset them, because nothing is reset when the program starts.
- **Pitch changes speed too:** Scratch's pitch effect speeds the sound up like a chipmunk. With generated tones in Python you can change pitch only, which is a nice "Python can do more" moment.

## Teaching ideas for a 9-year-old

**Analogy:** "play sound until done" is like **waiting at the door until the song on the radio finishes**. "start sound" is **switching on the radio and walking off to do other things**. In Python, `time.sleep()` (or `subprocess.run`) is "wait at the door".

**Mini-challenges**
1. **Doorbell vs radio.** Play three beeps with `start_sound` and then with `play_sound_until_done`. What is different? (With start, they pile up; with until done, they come one after another.)
2. **Chipmunk ladder.** Use a `for` loop that does `pitch += 20` (2 semitones) eight times and plays a note each time. That makes a scale. Bonus: use `input()` to ask "how many steps?". Scratch link: `repeat` + `change pitch effect by 20`.
3. **Ping-pong pan (wear headphones).** Bounce a beep from `pan = -100` to `pan = 100` and back while the turtle moves left and right. Then add a volume knob: `volume = int(input("Volume 0-100? "))`. Clamp it with `max(0, min(100, volume))`, which is exactly what Scratch does.

## Sources

- Scratch Wiki, Sound Blocks: https://en.scratch-wiki.info/wiki/Sound_Blocks
- Scratch Wiki, Change () Effect by () (Sound block): https://en.scratch-wiki.info/wiki/Change_()_Effect_by_()_(Sound_block)
- scratch-vm sound blocks source (ranges, per-target state, clone copy, one-tick yield): https://github.com/scratchfoundation/scratch-vm/blob/develop/src/blocks/scratch3_sound.js
- scratch-audio pitch effect (`2 ** ((val/10)/12)`): https://github.com/scratchfoundation/scratch-audio/blob/develop/src/effects/PitchEffect.js
- scratch-blocks colours (`sounds: #CF63CF`): https://github.com/scratchfoundation/scratch-blocks (core/colours.js)
- IPython `Audio` docs: https://ipython.readthedocs.io/en/stable/api/generated/IPython.display.html#IPython.display.Audio
- Python `winsound`: https://docs.python.org/3/library/winsound.html
- Python `wave`: https://docs.python.org/3/library/wave.html
- pygame.mixer: https://www.pygame.org/docs/ref/mixer.html
- macOS `afplay`: `man afplay`
