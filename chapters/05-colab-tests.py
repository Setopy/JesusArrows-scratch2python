# Part 5: Sensing and Decisions -- drawing programs for Colab
# Run the magic first cell (!pip install ColabTurtlePlus) once, then paste
# each piece into its own cell.

# %% Concept: touching a spot (distance to a point)
from ColabTurtlePlus.Turtle import *
clearscreen()
initializeTurtle((480, 360))
dot(20, "red")
penup()
goto(-200, 0)
pendown()
while distance(0, 0) >= 20:
    forward(10)
print("Touched it!")

# %% Concept: touching another sprite
from ColabTurtlePlus.Turtle import *
clearscreen()
initializeTurtle((480, 360))
shape("turtle")
dog = Turtle()
dog.shape("circle")
dog.penup()
dog.goto(150, 0)
while distance(dog.pos()) >= 20:
    forward(10)
print("Got you, dog!")

# %% Concept: key pressed? becomes input() turns
# needs typing: f, l, f, r, f (one per turn, then Enter)
from ColabTurtlePlus.Turtle import *
clearscreen()
initializeTurtle((480, 360))
shape("turtle")
for i in range(5):
    key = input("f, l or r? ")
    if key == "l":
        left(90)
    elif key == "r":
        right(90)
    forward(50)

# %% Concept: if on edge, bounce (home-made)
from ColabTurtlePlus.Turtle import *
clearscreen()
initializeTurtle((480, 360))
speed(13)
setheading(30)
for i in range(300):
    forward(10)
    if xcor() > 230 or xcor() < -230:
        setheading(180 - heading())
    if ycor() > 170 or ycor() < -170:
        setheading(0 - heading())
