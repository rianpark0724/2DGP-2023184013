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

def draw_moveX(fromX, toX, y):
    step = 3 if fromX < toX else -3
    for x in range(fromX, toX, step):
        draw_character(x, y)

def draw_moveY(fromY, toY, x):
    step = 3 if fromY < toY else -3
    for y in range(fromY, toY, step):
        draw_character(x, y)

def move_rectangle():
    draw_moveX(400, 700, 500)
    draw_moveY(500, 100, 700)
    draw_moveX(700, 100, 100)
    draw_moveY(100, 500, 100)
    draw_moveX(100, 400, 500)

# def draw_triRight():
#     for t in range(0, 150, 1):
#         t = t / 150.0
#         x = 400.0 + (300.0 * t)
#         y = 500.0 - (400.0 * t)
#         draw_character(x, y)

# def draw_triLeft():
#     for t in range(0, 150, 1):
#         t = t / 150.0
#         x = 100.0 + (300.0 * t)
#         y = 100.0 + (400.0 * t)
#         draw_character(x, y)

def draw_triMove(fromX, toX, fromY, toY, step):
    for t in range(0, step, 1):
            t = t / step
            x = fromX + (toX - fromX) * t
            y = fromY + (toY - fromY) * t
            draw_character(x, y)

def move_triangle():
    draw_triMove(400, 700, 500, 100, 150)
    draw_moveX(700, 100, 100)
    draw_triMove(100, 400, 100, 500, 150)

while True:
    move_circle()
    move_rectangle()
    move_triangle()

close_canvas()