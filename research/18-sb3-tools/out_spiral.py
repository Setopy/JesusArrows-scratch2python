from turtle import *
from time import sleep

# Scratch variables
side = 0   # variable for all sprites

# ---- Sprite: Pencil ----
def when_flag_clicked_1():
    global answer, side
    answer = input('What is your name?')
    if answer == 'Ada':
        print('Hello, programmer!')
        sleep(2)
    else:
        print('Hi ' + str(answer))
    pendown()
    side = 5
    for count in range(20):
        forward(side)
        left(90)
        side = side + 5
    penup()

def when_space_key_pressed():
    goto(0, 0)
    clear()

onkey(when_space_key_pressed, 'space')
listen()
when_flag_clicked_1()   # the green flag
# (skipped 1 loose block(s) with no hat: motion_movesteps)
