from pico2d import *
from math import *

open_canvas(800, 600)
character = load_image('character.png')

update_canvas()

def draw_top():
    for x in range(100, 600, 5):
        y = 500
        
        clear_canvas()
        character.draw(x, y)
        update_canvas()
        delay(0.01)

def draw_right():
    pass

def draw_bottom():
    pass

def draw_left():
    pass

def move_circle():
    for degree in range(360):
        theta = math.radians(degree)
        x = 400 + 200 * math.cos(theta)
        y = 300 + 200 * math.sin(theta)

        clear_canvas()
        character.draw(x, y)
        update_canvas()
        delay(0.01)

def move_rectangle():
    draw_top()
    draw_right()
    draw_bottom()
    draw_left()

def move_triangle():
    print("c")

while True:
    move_circle()
    move_rectangle()
    move_triangle()

close_canvas()