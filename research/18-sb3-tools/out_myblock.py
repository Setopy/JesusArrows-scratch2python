from turtle import *

# ---- Sprite: Cat ----
# My Block: define draw polygon (sides)
def draw_polygon(sides):
    for count in range(sides):
        forward(50)
        right(360 / sides)

def when_flag_clicked_1():
    when_i_receive_draw()   # broadcast

def when_i_receive_draw():
    draw_polygon(6)
    draw_polygon(3)

when_flag_clicked_1()   # the green flag
