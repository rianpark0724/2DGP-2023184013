from pico2d import *
from math import *

open_canvas(800, 600)
character = load_image('character.png')

update_canvas()

def draw_character(x, y):
    clear_canvas()
    character.draw(x, y)
    update_canvas()
    delay(0.01)

def move_circle():
    for degree in range(360):
        theta = math.radians(degree)
        x = 400 + 200 * math.cos(theta)
        y = 300 + 200 * math.sin(theta)

        draw_character(x, y)

def draw_top():
    for x in range(100, 700, 5):
        draw_character(x, 500)

def draw_right():
    for y in range(500, 100, -5):
        draw_character(700, y)

def draw_bottom():
    pass

def draw_left():
    pass

def move_rectangle():
    draw_top()
    draw_right()
    draw_bottom()
    draw_left()

def move_triangle():
    print("c")

while True:
    # move_circle()
    move_rectangle()
    move_triangle()

close_canvas()