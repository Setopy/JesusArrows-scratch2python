# Part 2: Loops. Drawing programs, one per cell. Run "!pip install ColabTurtlePlus" first.

# %% Concept: repeat becomes for (square)
from ColabTurtlePlus.Turtle import *
clearscreen()
initializeTurtle((480, 360))
for i in range(4):
    forward(100)
    right(90)
print("Square done!")

# %% Watch out: the silent indentation bug (draws one long line)
from ColabTurtlePlus.Turtle import *
clearscreen()
initializeTurtle((480, 360))
for i in range(4):
    forward(100)
right(90)

# %% Concept: a loop inside a loop (six triangles)
from ColabTurtlePlus.Turtle import *
clearscreen()
initializeTurtle((480, 360))
for i in range(6):
    for j in range(3):
        forward(80)
        right(120)
    right(60)

# %% Concept: forever becomes while True (runs forever: press the stop button)
from ColabTurtlePlus.Turtle import *
clearscreen()
initializeTurtle((480, 360))
while True:
    forward(100)
    right(90)

# %% Mission: Draw shapes the short way
from ColabTurtlePlus.Turtle import *
clearscreen()
initializeTurtle((480, 360))
pencolor("blue")
pensize(3)
for i in range(3):
    forward(120)
    right(120)

# %% Mission: Stars
from ColabTurtlePlus.Turtle import *
clearscreen()
initializeTurtle((480, 360))
pencolor("gold")
pensize(4)
penup()
goto(-75, 30)
pendown()
for i in range(5):
    forward(150)
    right(144)

# %% Mission: Square spiral
from ColabTurtlePlus.Turtle import *
clearscreen()
initializeTurtle((480, 360))
pencolor("purple")
speed(13)
for i in range(40):
    forward(i * 5)
    right(90)

# %% Mission: Flower of squares
from ColabTurtlePlus.Turtle import *
clearscreen()
initializeTurtle((480, 360))
pencolor("deeppink")
speed(13)
for i in range(12):
    for j in range(4):
        forward(80)
        right(90)
    right(30)

# %% Translate it yourself (answer)
from ColabTurtlePlus.Turtle import *
clearscreen()
initializeTurtle((480, 360))
pensize(4)
pencolor("purple")
for i in range(8):
    for j in range(6):
        forward(40)
        right(60)
    right(45)
penup()
print("Done!")
