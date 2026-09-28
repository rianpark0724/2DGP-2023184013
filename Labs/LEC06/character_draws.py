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

# def draw_recTopStart():
#     for x in range(400, 700, 3):
#         draw_character(x, 500)

# def draw_recTopEnd():
#     for x in range(100, 400, 3):
#         draw_character(x, 500)

# def draw_recRight():
#     for y in range(500, 100, -3):
#         draw_character(700, y)

# def draw_recBottom():
#     for x in range(700, 100, -3):
#         draw_character(x, 100)

# def draw_recLeft():
#     for y in range(100, 500, 3):
#         draw_character(100, y)

def draw_recX(fromX, toX, y):
    step = 3 if fromX < toX else -3
    for x in range(fromX, toX, step):
        draw_character(x, y)

def draw_recY(fromY, toY, x):
    print(fromY, toY, x)

def move_rectangle():
    draw_recX(400, 700, 500)
    draw_recY(500, 100, 700)
    draw_recX(700, 100, 100)
    draw_recY(100, 500, 100)
    draw_recX(100, 400, 500)

def draw_triRight():
    for t in range(0, 150, 1):
        t = t / 150.0
        x = 400.0 + (300.0 * t)
        y = 500.0 - (400.0 * t)
        draw_character(x, y)

def draw_triBottom():
    for x in range(700, 100, -3):
        draw_character(x, 100)

def draw_triLeft():
    for t in range(0, 150, 1):
        t = t / 150.0
        x = 100.0 + (300.0 * t)
        y = 100.0 + (400.0 * t)
        draw_character(x, y)

def move_triangle():
    draw_triRight()
    draw_triBottom()
    draw_triLeft()

while True:
    # move_circle()
    move_rectangle()
    # move_triangle()

close_canvas()