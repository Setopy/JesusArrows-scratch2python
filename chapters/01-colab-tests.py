# Part 1 (Motion and Pen): every drawing program, ready to paste into Colab.
# Run "!pip install ColabTurtlePlus" once first. Each piece is one cell.

# %% Concept: move and turn
from ColabTurtlePlus.Turtle import *
clearscreen()
initializeTurtle((480, 360))
forward(100)
right(90)
forward(100)
left(45)
backward(50)

# %% Concept: go to x y
from ColabTurtlePlus.Turtle import *
clearscreen()
initializeTurtle((480, 360))
goto(100, 50)
goto(-100, 50)
goto(0, 0)

# %% Concept: glide (speed and goto)
from ColabTurtlePlus.Turtle import *
clearscreen()
initializeTurtle((480, 360))
speed(1)
goto(150, 100)
speed(13)
goto(-150, 100)

# %% Concept: point in direction
from ColabTurtlePlus.Turtle import *
clearscreen()
initializeTurtle((480, 360))
setheading(90 - 0)
forward(100)
setheading(90 - 180)
forward(50)

# %% Concept: point towards
from ColabTurtlePlus.Turtle import *
clearscreen()
initializeTurtle((480, 360))
setheading(towards(100, 100))
forward(100)

# %% Concept: change x, set x, change y, set y
from ColabTurtlePlus.Turtle import *
clearscreen()
initializeTurtle((480, 360))
setx(xcor() + 50)
sety(ycor() + 50)
setx(-100)
sety(0)

# %% Concept: x position, y position, direction
from ColabTurtlePlus.Turtle import *
clearscreen()
initializeTurtle((480, 360))
forward(100)
left(90)
print(xcor())
print(ycor())
print(heading())

# %% Concept: go to random position
from ColabTurtlePlus.Turtle import *
clearscreen()
initializeTurtle((480, 360))
import random
goto(random.randint(-240, 240),
     random.randint(-180, 180))

# %% Concept: pen up and pen down
from ColabTurtlePlus.Turtle import *
clearscreen()
initializeTurtle((480, 360))
forward(50)
penup()
forward(50)
pendown()
forward(50)

# %% Concept: set pen colour
from ColabTurtlePlus.Turtle import *
clearscreen()
initializeTurtle((480, 360))
pencolor("red")
forward(100)
pencolor("#ff8800")
forward(100)

# %% Concept: pen size and erase all
from ColabTurtlePlus.Turtle import *
clearscreen()
initializeTurtle((480, 360))
pensize(10)
forward(100)
clear()

# %% Concept: stamp
from ColabTurtlePlus.Turtle import *
clearscreen()
initializeTurtle((480, 360))
shape("turtle")
stamp()
forward(100)
stamp()

# %% Concept: bonus powers
from ColabTurtlePlus.Turtle import *
clearscreen()
initializeTurtle((480, 360))
shape("turtle")
circle(50)
dot(30, "gold")
fillcolor("skyblue")
begin_fill()
circle(-40)
end_fill()
write("Hi!")

# %% Mission: a square the long way
from ColabTurtlePlus.Turtle import *
clearscreen()
initializeTurtle((480, 360))
shape("turtle")
pencolor("blue")
pensize(3)
forward(100)
right(90)
forward(100)
right(90)
forward(100)
right(90)
forward(100)
right(90)

# %% Mission: draw a house
from ColabTurtlePlus.Turtle import *
clearscreen()
initializeTurtle((480, 360))
speed(8)
pensize(3)

penup()
goto(-100, -150)
pendown()
fillcolor("tan")
begin_fill()
goto(100, -150)
goto(100, 50)
goto(-100, 50)
goto(-100, -150)
end_fill()

penup()
goto(-120, 50)
pendown()
fillcolor("firebrick")
begin_fill()
goto(120, 50)
goto(0, 150)
goto(-120, 50)
end_fill()

penup()
goto(-25, -150)
pendown()
fillcolor("saddlebrown")
begin_fill()
goto(-25, -70)
goto(25, -70)
goto(25, -150)
end_fill()

penup()
goto(55, -10)
dot(40, "skyblue")
hideturtle()

# %% Mission: robot face
from ColabTurtlePlus.Turtle import *
clearscreen()
initializeTurtle((480, 360))
speed(10)
pensize(4)
pencolor("slategray")

penup()
goto(0, -100)
pendown()
fillcolor("lightgray")
begin_fill()
circle(100)
end_fill()

penup()
goto(-40, 30)
dot(40, "white")
dot(16, "black")
goto(40, 30)
dot(40, "white")
dot(16, "black")

goto(-50, -40)
pendown()
pencolor("red")
goto(50, -40)

penup()
goto(0, 100)
pendown()
pencolor("slategray")
goto(0, 140)
dot(20, "gold")

penup()
goto(120, -150)
write("I am Robo!")
shape("turtle")
color("seagreen")
goto(-150, -120)
stamp()
hideturtle()

# %% Translate it yourself (answer)
from ColabTurtlePlus.Turtle import *
clearscreen()
initializeTurtle((480, 360))
penup()
goto(-100, 0)
pendown()
pencolor("red")
pensize(4)
setheading(90 - 0)
forward(80)
right(90)
forward(80)
stamp()

# %% Two-line puzzle (answer)
from ColabTurtlePlus.Turtle import *
clearscreen()
initializeTurtle((480, 360))
setheading(90 - 180)
forward(100)
