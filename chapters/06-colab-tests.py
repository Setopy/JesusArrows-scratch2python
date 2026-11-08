# Part 6 (My Blocks): every drawing program, ready to paste into Colab.
# Run "!pip install ColabTurtlePlus" once first. Each piece is complete.

# %% Concept: number input (square)
from ColabTurtlePlus.Turtle import *
clearscreen()
initializeTurtle((480, 360))

def square(size):
    for i in range(4):
        forward(size)
        right(90)

square(50)
square(100)

# %% Concept: several inputs (polygon)
from ColabTurtlePlus.Turtle import *
clearscreen()
initializeTurtle((480, 360))

def polygon(sides, size):
    for i in range(sides):
        forward(size)
        right(360 / sides)

polygon(3, 100)
polygon(6, 50)

# %% Concept: run without screen refresh (animationOff)
from ColabTurtlePlus.Turtle import *
clearscreen()
initializeTurtle((480, 360))

def square(size):
    for i in range(4):
        forward(size)
        right(90)

def flower():
    animationOff()
    for i in range(36):
        square(80)
        right(10)
    animationOn()

flower()

# %% Concept: more sprites (cat and dog)
from ColabTurtlePlus.Turtle import *
clearscreen()
initializeTurtle((480, 360))

cat = Turtle()
dog = Turtle()
cat.pencolor("orange")
dog.pencolor("blue")
cat.forward(100)
dog.left(90)
dog.forward(100)

# %% Concept: passing a sprite into a block
from ColabTurtlePlus.Turtle import *
clearscreen()
initializeTurtle((480, 360))

cat = Turtle()
dog = Turtle()
cat.pencolor("orange")
dog.pencolor("blue")

def square(t, size):
    for i in range(4):
        t.forward(size)
        t.right(90)

square(cat, 60)
square(dog, 100)

# %% Concept: clones as a list of sprites
from ColabTurtlePlus.Turtle import *
clearscreen()
initializeTurtle((480, 360))

army = []
for i in range(5):
    s = Turtle()
    s.shape("turtle")
    s.penup()
    s.goto(-200, 120 - i * 60)
    army.append(s)

for s in army:
    s.forward(100)

# %% Bonus: cookie cutter (a tiny class)
from ColabTurtlePlus.Turtle import *
clearscreen()
initializeTurtle((480, 360))

class Bug:
    def __init__(self, y):
        self.t = Turtle()
        self.t.shape("turtle")
        self.t.penup()
        self.t.goto(-200, y)

    def move(self):
        self.t.forward(30)

bugs = []
for i in range(3):
    bugs.append(Bug(i * 60))

for step in range(5):
    for b in bugs:
        b.move()

# %% Bonus: recursive tree
from ColabTurtlePlus.Turtle import *
clearscreen()
initializeTurtle((480, 360))
speed(13)

def tree(size):
    if size < 10:
        return
    forward(size)
    left(30)
    tree(size * 0.7)
    right(60)
    tree(size * 0.7)
    left(30)
    back(size)

penup()
goto(0, -170)
setheading(90)
pendown()
tree(80)

# %% Mission: Make your own block
from ColabTurtlePlus.Turtle import *
clearscreen()
initializeTurtle((480, 360))

def square(size):
    for i in range(4):
        forward(size)
        right(90)

square(40)
square(80)
square(120)

# %% Mission: Make your own block, flower challenge
from ColabTurtlePlus.Turtle import *
clearscreen()
initializeTurtle((480, 360))
speed(13)

def square(size):
    for i in range(4):
        forward(size)
        right(90)

for i in range(12):
    square(80)
    right(30)

# %% Mission: Shape machine
from ColabTurtlePlus.Turtle import *
clearscreen()
initializeTurtle((480, 360))
speed(13)

def polygon(sides, size):
    for i in range(sides):
        forward(size)
        right(360 / sides)

def flower(petals, sides, size):
    for i in range(petals):
        polygon(sides, size)
        right(360 / petals)

penup()
goto(-170, 60)
pendown()
pencolor("blue")
polygon(5, 70)

penup()
goto(90, 0)
pendown()
pencolor("purple")
flower(12, 6, 40)

# %% Mission: Sprite army
from ColabTurtlePlus.Turtle import *
clearscreen()
initializeTurtle((480, 360))

colours = ["red", "orange", "gold", "green", "blue"]
army = []
for i in range(5):
    s = Turtle()
    s.shape("turtle")
    s.color(colours[i])
    s.speed(13)
    s.penup()
    s.goto(-200, 120 - i * 60)
    s.pendown()
    army.append(s)

def march(steps):
    for s in army:
        s.forward(steps)

for step in range(4):
    march(80)

# %% Translate it yourself: two gold stars
from ColabTurtlePlus.Turtle import *
clearscreen()
initializeTurtle((480, 360))

def star(size):
    for i in range(5):
        forward(size)
        right(144)

pencolor("gold")
star(100)
star(50)
