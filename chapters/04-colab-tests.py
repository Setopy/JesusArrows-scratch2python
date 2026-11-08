# Part 4 (Operators): drawing programs for Colab.
# Run the magic first cell (!pip install ColabTurtlePlus) once first.

# %% Mission: Random dot art
from ColabTurtlePlus.Turtle import *
clearscreen()
initializeTurtle((480, 360))
import random

colours = ["red", "gold", "skyblue", "pink", "lime"]
speed(13)
penup()
hideturtle()
for i in range(50):
    x = random.randint(-240, 240)
    y = random.randint(-180, 180)
    goto(x, y)
    size = random.randint(10, 40)
    colour = colours[random.randint(0, 4)]
    dot(size, colour)

# %% Mission: Random dot art, challenge version (night sky, 7 colours)
from ColabTurtlePlus.Turtle import *
clearscreen()
initializeTurtle((480, 360))
import random
bgcolor("black")

colours = ["red", "gold", "skyblue", "pink", "lime",
           "orange", "purple"]
speed(13)
penup()
hideturtle()
for i in range(200):
    x = random.randint(-240, 240)
    y = random.randint(0, 180)
    goto(x, y)
    size = random.randint(10, 40)
    colour = colours[random.randint(0, len(colours) - 1)]
    dot(size, colour)
