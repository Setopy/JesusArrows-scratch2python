# Colab tests for chapter 09 (The Bug Zoo). Run the magic first cell
# (!pip install ColabTurtlePlus) once before these.

# %% Bug hunt 9 (broken on purpose): draws one long line, not a square
from ColabTurtlePlus.Turtle import *
clearscreen()
initializeTurtle((480, 360))
for i in range(4):
    forward(50)
right(90)

# %% Bug hunt 9 (fixed): draws a square
from ColabTurtlePlus.Turtle import *
clearscreen()
initializeTurtle((480, 360))
for i in range(4):
    forward(50)
    right(90)

# %% Bug zoo card 4 (broken on purpose): expect NameError ... Did you mean: 'forward'?
from ColabTurtlePlus.Turtle import *
clearscreen()
initializeTurtle((480, 360))
forwad(100)
