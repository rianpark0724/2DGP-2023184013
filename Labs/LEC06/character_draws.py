from pico2d import *
from math import *

open_canvas(800, 600)
character = load_image('character.png')

update_canvas()

def move_circle():
    print("a")

def move_rectangle():
    clear_canvas()
    character.draw(400,300)
    update_canvas()

def move_triangle():
    print("c")

while True:
    move_circle()
    move_rectangle()
    move_triangle()

close_canvas()