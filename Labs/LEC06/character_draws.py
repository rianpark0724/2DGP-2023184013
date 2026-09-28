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
    for degree in range(450, 90, -1):
        theta = math.radians(degree)
        x = 400 + 200 * math.cos(theta)
        y = 300 + 200 * math.sin(theta)

        draw_character(x, y)

def draw_recTop():
    for x in range(100, 700, 5):
        draw_character(x, 500)

def draw_recRight():
    for y in range(500, 100, -5):
        draw_character(700, y)

def draw_recBottom():
    for x in range(700, 100, -5):
        draw_character(x, 100)

def draw_recLeft():
    for y in range(100, 500, 5):
        draw_character(100, y)

def move_rectangle():
    draw_recTop()
    draw_recRight()
    draw_recBottom()
    draw_recLeft()

def draw_triBottom():
    for x in range(100, 700, 5):
        draw_character(x, 100)

def draw_triRight():
    for t in range(0, 100, 1):
        t = t / 100.0
        x = 700.0 - (300.0 * t)
        y = 100.0 + (400.0 * t)
        draw_character(x, y)

def draw_triLeft():
    print("c")

def move_triangle():
    draw_triBottom()
    draw_triRight()
    draw_triLeft()

while True:
    # move_circle()
    # move_rectangle()
    move_triangle()

close_canvas()