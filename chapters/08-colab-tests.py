# 08 Big Projects: drawing programs for Colab (run "!pip install ColabTurtlePlus" once first)

# %% Big Project: Animate your name
# needs typing: What is your name? (e.g. Zainab)
from ColabTurtlePlus.Turtle import *
clearscreen()
initializeTurtle((480, 360))
import random
import time

bgcolor("black")
hideturtle()
penup()
speed(13)
colours = ["red", "orange", "gold", "lime", "skyblue",
           "violet", "hotpink"]

name = input("What is your name? ")
gap = 40
if len(name) > 10:
    gap = 400 / len(name)
start = 0 - (len(name) - 1) * gap / 2

for frame in range(8):
    clear()
    x = start
    for letter in name:
        color(random.choice(colours))
        goto(x, random.randint(-20, 20))
        write(letter, align="center",
              font=("Arial", 40, "bold"))
        x = x + gap
    time.sleep(0.3)

goto(0, -120)
color("white")
write("Hello, " + name + "!", align="center",
      font=("Arial", 24, "italic"))

# %% Big Project: Pen flower
# needs typing: How many petals? (e.g. 8)
from ColabTurtlePlus.Turtle import *
clearscreen()
initializeTurtle((480, 360))

bgcolor("black")
speed(13)
pensize(2)
colours = ["red", "orange", "gold", "lime",
           "skyblue", "violet"]

def petal(size):
    circle(size, 60)
    left(120)
    circle(size, 60)
    left(120)

petals = int(input("How many petals? (3 to 20) "))
for p in range(petals):
    color(colours[p % 6])
    petal(100)
    left(360 / petals)

color("white")
for ring in range(36):
    circle(40)
    left(10)

penup()
goto(0, 0)
dot(25, "gold")
hideturtle()

# %% Big Project: Chase game
# needs typing: w, a, s or d + Enter, up to 20 times
from ColabTurtlePlus.Turtle import *
clearscreen()
initializeTurtle((480, 360))
import random

speed(13)
shape("turtle")
color("green")
penup()

cat = Turtle()
cat.speed(13)
cat.shape("circle")
cat.color("orange")
cat.penup()
cat.goto(200, 140)

star = Turtle()
star.speed(13)
star.shape("triangle")
star.color("gold")
star.penup()
star.goto(120, -80)

score = 0
for turn in range(20):
    move = input("Move with w, a, s or d: ").lower()
    if move == "w":
        setheading(90)
    elif move == "s":
        setheading(270)
    elif move == "a":
        setheading(180)
    elif move == "d":
        setheading(0)
    forward(40)
    if xcor() > 220 or xcor() < -220:
        back(40)
    if ycor() > 160 or ycor() < -160:
        back(40)

    if star.distance(pos()) < 20:
        score = score + 1
        print("You got the star! Score:", score)
        x = random.randint(-5, 5) * 40
        y = random.randint(-4, 4) * 40
        star.goto(x, y)

    cat.setheading(cat.towards(pos()))
    cat.forward(25)
    if cat.distance(pos()) < 30:
        print("The cat caught you!")
        break

print("Game over! Stars:", score)

# %% Big Project: Catch game
# needs typing: basket x five times (e.g. 0, 80, -80, 160, 0)
from ColabTurtlePlus.Turtle import *
clearscreen()
initializeTurtle((480, 360))
import random

bgcolor("skyblue")
hideturtle()

basket = Turtle()
basket.shape("square")
basket.color("brown")
basket.penup()
basket.goto(0, -150)

apple = Turtle()
apple.shape("circle")
apple.color("red")
apple.penup()
apple.speed(13)

score = 0
for apples in range(5):
    x = random.choice([-80, 0, 80])
    drift = random.choice([-20, 0, 20])
    apple.jumpto(x, 160)
    for fall in range(4):
        apple.goto(apple.xcor() + drift,
                   apple.ycor() - 40)

    spot = int(input("Basket x (-240 to 240): "))
    basket.goto(spot, -150)

    for fall in range(4):
        apple.goto(apple.xcor() + drift,
                   apple.ycor() - 40)
    if basket.distance(apple.pos()) < 50:
        score = score + 1
        print("Caught it!")
    else:
        print("Splat! It landed at x =",
              round(apple.xcor()))

print("You caught", score, "out of 5 apples")

# %% Answers: Pen flower garden (level up)
# needs typing: How many petals? (e.g. 7)
from ColabTurtlePlus.Turtle import *
clearscreen()
initializeTurtle((480, 360))

bgcolor("black")
speed(13)
pensize(2)
colours = ["red", "orange", "gold", "lime",
           "skyblue", "violet"]

def petal(size):
    circle(size, 60)
    left(120)
    circle(size, 60)
    left(120)

def flower(x, y):
    penup()
    goto(x, y)
    pendown()
    for p in range(petals):
        color(colours[p % 6])
        petal(50)
        left(360 / petals)

petals = int(input("How many petals? (3 to 20) "))
flower(-150, 0)
flower(0, 0)
flower(150, 0)
hideturtle()

# %% Answers: Catch game computer player (level up)
from ColabTurtlePlus.Turtle import *
clearscreen()
initializeTurtle((480, 360))
import random

bgcolor("skyblue")
hideturtle()

basket = Turtle()
basket.shape("square")
basket.color("brown")
basket.penup()
basket.goto(0, -150)

apple = Turtle()
apple.shape("circle")
apple.color("red")
apple.penup()
apple.speed(13)

score = 0
for apples in range(5):
    x = random.choice([-80, 0, 80])
    drift = random.choice([-20, 0, 20])
    apple.jumpto(x, 160)
    for fall in range(4):
        apple.goto(apple.xcor() + drift,
                   apple.ycor() - 40)

    spot = apple.xcor() + 4 * drift
    basket.goto(spot, -150)

    for fall in range(4):
        apple.goto(apple.xcor() + drift,
                   apple.ycor() - 40)
    if basket.distance(apple.pos()) < 50:
        score = score + 1
        print("Caught it!")
    else:
        print("Splat! It landed at x =",
              round(apple.xcor()))

print("You caught", score, "out of 5 apples")
