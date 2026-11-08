# Part 3: Variables and Lists. Drawing programs, one per cell.
# Run the “In the beginning” cell once per session: !pip install ColabTurtlePlus

# %% Concept page: Variables can draw too (two squares)
from ColabTurtlePlus.Turtle import *
clearscreen()
initializeTurtle((480, 360))
size = 50
for i in range(4):
    forward(size)
    right(90)
size = size + 50
for i in range(4):
    forward(size)
    right(90)

# %% Mission: Growing spiral
from ColabTurtlePlus.Turtle import *
clearscreen()
initializeTurtle((480, 360))
speed(13)
pencolor("purple")
size = 5
for i in range(40):
    forward(size)
    right(90)
    size = size + 5

# %% Mission: Growing spiral, challenge (turn 91)
from ColabTurtlePlus.Turtle import *
clearscreen()
initializeTurtle((480, 360))
speed(13)
pencolor("purple")
size = 5
for i in range(40):
    forward(size)
    right(91)
    size = size + 5

# %% Mission: Rainbow from a colour list
from ColabTurtlePlus.Turtle import *
clearscreen()
initializeTurtle((480, 360))
speed(13)
pensize(15)
colours = ["red", "orange", "yellow",
           "green", "blue", "purple"]
y = 60
for colour in colours:
    pencolor(colour)
    penup()
    goto(-150, y)
    pendown()
    forward(300)
    y = y - 15
hideturtle()

# %% Answers: Rainbow challenge (append "pink", bigger gap)
from ColabTurtlePlus.Turtle import *
clearscreen()
initializeTurtle((480, 360))
speed(13)
pensize(15)
colours = ["red", "orange", "yellow",
           "green", "blue", "purple"]
colours.append("pink")
y = 60
for colour in colours:
    pencolor(colour)
    penup()
    goto(-150, y)
    pendown()
    forward(300)
    y = y - 20
hideturtle()

# %% Answers: Growing spiral, looser (+ 8)
from ColabTurtlePlus.Turtle import *
clearscreen()
initializeTurtle((480, 360))
speed(13)
pencolor("purple")
size = 5
for i in range(40):
    forward(size)
    right(90)
    size = size + 8

# %% Answers: Growing spiral, thicker pen
from ColabTurtlePlus.Turtle import *
clearscreen()
initializeTurtle((480, 360))
speed(13)
pencolor("purple")
size = 5
thick = 1
for i in range(40):
    pensize(thick)
    forward(size)
    right(90)
    size = size + 5
    thick = thick + 0.2

# %% Answers: Shrinking spiral
from ColabTurtlePlus.Turtle import *
clearscreen()
initializeTurtle((480, 360))
speed(13)
pencolor("purple")
penup()
goto(-100, 100)
pendown()
size = 200
for i in range(40):
    forward(size)
    right(90)
    size = size - 5

# %% Answers: Rainbow super challenge (shorter stripes)
from ColabTurtlePlus.Turtle import *
clearscreen()
initializeTurtle((480, 360))
speed(13)
pensize(15)
colours = ["red", "orange", "yellow",
           "green", "blue", "purple"]
y = 60
length = 300
for colour in colours:
    pencolor(colour)
    penup()
    goto(-150, y)
    pendown()
    forward(length)
    y = y - 15
    length = length - 30
hideturtle()

