# Drawing snippets from chapters/00-front.tex (paste each piece into Colab).
# Run the magic first cell once first:  !pip install ColabTurtlePlus

# %% Meet Google Colab: first line
from ColabTurtlePlus.Turtle import *
clearscreen()
initializeTurtle((480, 360))
forward(100)

# %% Scratch words: go to and point in direction
from ColabTurtlePlus.Turtle import *
clearscreen()
initializeTurtle((480, 360))
goto(100, 80)
setheading(90 - 180)
forward(50)

# %% Habit 1: spaces show what is inside
from ColabTurtlePlus.Turtle import *
clearscreen()
initializeTurtle((480, 360))
for i in range(4):
    forward(100)
    right(90)
penup()

# %% How Colab is different: one loop moves all sprites
from ColabTurtlePlus.Turtle import *
clearscreen()
initializeTurtle((480, 360))
cat = Turtle()
dog = Turtle()
dog.left(90)
for i in range(10):
    cat.forward(10)
    dog.forward(10)

# %% How Colab is different: shapes and colours
from ColabTurtlePlus.Turtle import *
clearscreen()
initializeTurtle((480, 360))
shape("turtle")
color("gold")
forward(100)
