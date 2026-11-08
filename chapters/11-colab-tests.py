# Colab tests for 11-grown-ups.tex (no drawing programs in this chapter)

# %% Sound helper (For grown-ups: Sound in Colab)
import numpy as np
from IPython.display import Audio, display

def beep(freq=440, secs=0.5):
    times = np.linspace(0, secs, int(22050 * secs))
    sound = np.sin(2 * np.pi * freq * times)
    display(Audio(sound, rate=22050, autoplay=True))

beep(262)

# %% Peek inside an .sb3 (needs an uploaded file called my-project.sb3)
import zipfile, json

with zipfile.ZipFile("my-project.sb3") as z:
    project = json.loads(z.read("project.json"))

for sprite in project["targets"]:
    print("Sprite:", sprite["name"])
    for block in sprite["blocks"].values():
        if isinstance(block, dict):
            print("   ", block["opcode"])
