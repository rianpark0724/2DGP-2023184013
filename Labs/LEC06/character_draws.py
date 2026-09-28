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

def move_circle(x, y, radius, start_degree):
    for degree in range(start_degree, start_degree - 360, -1):
        theta = math.radians(degree)
        ax = x + radius * math.cos(theta)
        ay = y + radius * math.sin(theta)

        draw_character(ax, ay)

def draw_moveX(fromX, toX, y):
    step = 3 if fromX < toX else -3
    for x in range(fromX, toX, step):
        draw_character(x, y)

def draw_moveY(fromY, toY, x):
    step = 3 if fromY < toY else -3
    for y in range(fromY, toY, step):
        draw_character(x, y)

def move_rectangle(x1, y1, x2, y2, x3, y3, x4, y4, x5, y5):
    draw_moveX(x1, x2, y1)
    draw_moveY(y2, y3, x2)
    draw_moveX(x3, x4, y3)
    draw_moveY(y4, y5, x4)
    draw_moveX(x5, x1, y5)

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
    move_circle(400, 300, 200, 450)
    move_rectangle(400, 500, 700, 500, 700, 100, 100, 100, 100, 500)
    move_triangle(400, 500, 700, 100, 100, 100)

close_canvas()