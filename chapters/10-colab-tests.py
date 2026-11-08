# Drawing snippets from the Block Dictionary and cheat sheet (Part 10).
# Each piece is complete with the three starting lines.

# %% Dictionary: Motion rows
from ColabTurtlePlus.Turtle import *
clearscreen()
initializeTurtle((480, 360))
import random
cat = Turtle()
cat.penup()
cat.goto(-100, 50)
forward(10)
back(10)
right(15)
left(15)
x = random.randint(
    -240, 240)
y = random.randint(
    -180, 180)
goto(x, y)
goto(cat.pos())
goto(0, 0)
home()
speed(2)
goto(50, 50)
speed(1)
goto(0, 0)
setheading(0)
setheading(90 - 180)
p = cat.pos()
d = towards(p)
setheading(d)
setx(xcor() + 10)
setx(0)
sety(ycor() + 10)
sety(0)
for i in range(60):
    forward(10)
    h = heading()
    if abs(xcor()) > 240:
        setheading(180-h)
    if abs(ycor()) > 180:
        setheading(-h)
shape("circle")
print(round(xcor()), round(ycor()), 90 - heading())

# %% Dictionary: Looks rows
from ColabTurtlePlus.Turtle import *
clearscreen()
initializeTurtle((480, 360))
import time
print("Hello!")
time.sleep(2)
write("Hello!")
print("(Hmm...)")
shape("turtle")
costumes = ["turtle", "circle", "square", "arrow"]
n = 0
for i in range(4):
    n = (n + 1) % 4
    shape(costumes[n])
    time.sleep(0.5)
skies = ["white", "skyblue", "gold"]
b = 0
b = (b + 1) % 3
bgcolor(skies[b])
bgcolor("skyblue")
size = 100
size = size + 10
shapesize(size / 100)
shapesize(2)
fillcolor("gold")
color("gold")
fillcolor("pink")
color("black")
hideturtle()
showturtle()
print(n + 1, shape(), b + 1, bgcolor(), size)

# %% Dictionary: clones and sensing rows
from ColabTurtlePlus.Turtle import *
clearscreen()
initializeTurtle((480, 360))
star = Turtle()
stars = []
for i in range(3):
    s = Turtle()
    s.shape("circle")
    s.goto(-100 + 100 * i, 100)
    stars.append(s)
s.hideturtle()
stars.remove(s)
cat = Turtle()
cat.goto(10, 0)
p = cat.pos()
print(distance(p) < 20, distance(cat.pos()), cat.xcor(), cat.ycor(), cat.heading())
print(ycor() < -100, abs(xcor()) > 240)

# %% Dictionary: Pen rows
from ColabTurtlePlus.Turtle import *
clearscreen()
initializeTurtle((480, 360))
speed(13)
pendown()
pencolor("red")
forward(50)
stamp()
clearstamps()
rainbow = ["red", "gold", "green"]
c = 0
for i in range(6):
    c = (c + 1) % 3
    pencolor(rainbow[c])
    forward(20)
    right(60)
pencolor("cyan")
pencolor("darkred")
pencolor("pink")
w = pensize() + 1
pensize(w)
pensize(5)
penup()
goto(-100, -100)
pendown()
fillcolor("gold")
begin_fill()
circle(50)
end_fill()
clear()

# %% Cheat sheet: all drawing tiles together
from ColabTurtlePlus.Turtle import *
clearscreen()
initializeTurtle((480, 360))
speed(13)
def square(size):
    for i in range(4):
        forward(size)
        right(90)
square(50)
def double(n):
    return n * 2
print(double(4))
cat = Turtle()
cat.shape("turtle")
cat.goto(-100, 0)
cat.forward(50)
print(cat.distance(pos()) < 20)
