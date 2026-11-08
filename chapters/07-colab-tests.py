# Part 7: Looks, Sound and Events. Colab test programs.
# Run the magic first cell (!pip install ColabTurtlePlus) before these.
# Each piece is complete. Sound pieces need the "sound cell" piece first.

# %% Concept: words on the stage (say for 2 seconds)
from ColabTurtlePlus.Turtle import *
clearscreen()
initializeTurtle((480, 360))
import time

shape("turtle")
speech = Turtle()
speech.hideturtle()
speech.penup()
speech.goto(0, 30)
speech.write("Hello!", align="center",
             font=("Arial", 20, "normal"))
time.sleep(2)
speech.clear()

# %% Concept: think on the stage
from ColabTurtlePlus.Turtle import *
clearscreen()
initializeTurtle((480, 360))
import time

shape("turtle")
speech = Turtle()
speech.hideturtle()
speech.penup()
speech.goto(0, 30)
speech.write("Hmm...", align="center",
             font=("Arial", 20, "italic"))
time.sleep(2)
speech.clear()

# %% Concept: switch costume
from ColabTurtlePlus.Turtle import *
clearscreen()
initializeTurtle((480, 360))

shape("turtle")

# %% Concept: next costume
from ColabTurtlePlus.Turtle import *
clearscreen()
initializeTurtle((480, 360))
import time

costumes = ["turtle", "circle", "square"]
n = 0
shape(costumes[n])
for i in range(6):
    time.sleep(1)
    n = (n + 1) % len(costumes)
    shape(costumes[n])

# %% Concept: set size and change size
from ColabTurtlePlus.Turtle import *
clearscreen()
initializeTurtle((480, 360))
import time

shape("turtle")
shapesize(2)
time.sleep(1)
size = 200
for i in range(5):
    size = size + 50
    shapesize(size / 100)
    time.sleep(0.5)

# %% Concept: show and hide
from ColabTurtlePlus.Turtle import *
clearscreen()
initializeTurtle((480, 360))
import time

shape("turtle")
for i in range(3):
    hideturtle()
    time.sleep(0.5)
    showturtle()
    time.sleep(0.5)

# %% Concept: backdrop and colour effect
from ColabTurtlePlus.Turtle import *
clearscreen()
initializeTurtle((480, 360))
import time

shape("turtle")
shapesize(3)
bgcolor("skyblue")
rainbow = ["red", "orange",
           "gold", "green"]
for c in rainbow:
    color(c)
    time.sleep(0.5)

# %% Concept: sound cell (run once)
import numpy as np
from IPython.display import Audio, display

def beep(freq=440, secs=0.5):
    times = np.linspace(0, secs, int(22050 * secs))
    sound = np.sin(2 * np.pi * freq * times)
    display(Audio(sound, rate=22050, autoplay=True))

# %% Concept: start sound and play until done
import time
beep(262)
time.sleep(0.5)
beep(330)
time.sleep(0.5)
beep(392, 1)

# %% Concept: a tune from a list
import time
notes = [262, 294, 330, 349, 392, 440, 494, 523]
for note in notes:
    beep(note, 0.3)
    time.sleep(0.4)

# %% Concept: tune in one piece (if notes pile up)
def play_tune(notes, secs=0.4):
    parts = []
    for note in notes:
        times = np.linspace(0, secs, int(22050 * secs))
        parts.append(np.sin(2 * np.pi * note * times))
    song = np.concatenate(parts)
    display(Audio(song, rate=22050, autoplay=True))

play_tune([262, 262, 392, 392, 440, 440, 392])

# %% Concept: key presses become input turns
# needs typing: f, l, f, r, f (one per question)
from ColabTurtlePlus.Turtle import *
clearscreen()
initializeTurtle((480, 360))

shape("turtle")
for turn in range(5):
    key = input("f, l or r? ")
    if key == "f":
        forward(50)
    elif key == "l":
        left(90)
    elif key == "r":
        right(90)

# %% Concept: one loop moves every sprite
from ColabTurtlePlus.Turtle import *
clearscreen()
initializeTurtle((480, 360))

hideturtle()
cat = Turtle()
cat.shape("turtle")
dog = Turtle()
dog.shape("circle")
dog.left(90)
for step in range(20):
    cat.forward(10)
    dog.forward(5)

# %% Mission: Costume parade
from ColabTurtlePlus.Turtle import *
clearscreen()
initializeTurtle((480, 360))
import time

costumes = ["turtle", "circle", "square", "triangle"]
colours = ["green", "red", "blue", "orange"]
n = 0
size = 100
bgcolor("lavender")
for i in range(8):
    shape(costumes[n])
    color(colours[n])
    shapesize(size / 100)
    print("Costume", n + 1, costumes[n])
    time.sleep(0.5)
    n = (n + 1) % len(costumes)
    size = size + 50
hideturtle()
print("Ta-da!")

# %% Mission: Make music (run the sound cell first)
import time
C = 262
D = 294
E = 330
F = 349
G = 392
A = 440

tune = [C, C, G, G, A, A, G]
beats = [1, 1, 1, 1, 1, 1, 2]
for i in range(len(tune)):
    secs = beats[i] * 0.4
    beep(tune[i], secs)
    time.sleep(secs + 0.1)
print("Twinkle, twinkle, little star!")

# %% Mission: Make music, Happy Birthday challenge answer
import time
G = 392
A = 440
B = 494
C2 = 523
tune = [G, G, A, G, C2, B]
beats = [0.75, 0.25, 1, 1, 1, 2]
for i in range(len(tune)):
    secs = beats[i] * 0.5
    beep(tune[i], secs)
    time.sleep(secs + 0.1)

# %% Mission: Turtle race
from ColabTurtlePlus.Turtle import *
clearscreen()
initializeTurtle((480, 360))
import random

def make_racer(colour, y):
    racer = Turtle()
    racer.shape("turtle")
    racer.color(colour)
    racer.penup()
    racer.goto(-200, y)
    racer.pendown()
    return racer

hideturtle()
red = make_racer("red", 50)
blue = make_racer("blue", -50)

while red.xcor() < 200 and blue.xcor() < 200:
    red.forward(random.randint(1, 20))
    blue.forward(random.randint(1, 20))

if red.xcor() > blue.xcor():
    print("Red wins!")
    red.write("I win!", font=("Arial", 16, "bold"))
else:
    print("Blue wins!")
    blue.write("I win!", font=("Arial", 16, "bold"))

# %% Translate it yourself (answer)
from ColabTurtlePlus.Turtle import *
clearscreen()
initializeTurtle((480, 360))
import time

shape("turtle")
shapesize(3)
for i in range(3):
    hideturtle()
    time.sleep(0.5)
    showturtle()
    time.sleep(0.5)
print("Boo!")
time.sleep(2)
