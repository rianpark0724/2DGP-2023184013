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

def draw_triMove(fromX, toX, fromY, toY, step):
    for t in range(0, step, 1):
            t = t / step
            x = fromX + (toX - fromX) * t
            y = fromY + (toY - fromY) * t
            draw_character(x, y)

def move_triangle(x1, y1, x2, y2, x3, y3):
    draw_triMove(x1, x2, y1, y2, 150)
    draw_moveX(x2, x3, y3)
    draw_triMove(x3, x1, y3, y1, 150)

while True:
    # move_circle()
    # move_rectangle()
    move_triangle(400, 500, 700, 100, 100, 100)

close_canvas()