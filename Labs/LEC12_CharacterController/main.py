from pico2d import *
import sys
import random
import time

sys.path.insert(0, r"C:\Users\rianp\OneDrive\visual\2dgame\2DGP-2023184013\Labs\LEC12_CharacterController")

from grass import Grass
from boy import Boy

# Game object class here


def handle_events():
    global running
    global last_input_time

    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                running = False
            else:
                last_input_time = time.monotonic()
                if event.key == SDLK_SPACE and boy.state == 'SLEEP':
                    boy.wake()


def reset_world():
    global world
    global boy
    global last_input_time

    world = []
    last_input_time = time.monotonic()

    grass = Grass()
    world.append(grass)

    boy = Boy()
    world.append(boy)



def update_world():
    if boy.state == 'IDLE' and time.monotonic() - last_input_time >= 5:
        boy.sleep()

    for o in world:
        o.update()
    pass


def render_world():
    clear_canvas()
    for o in world:
        o.draw()
    update_canvas()


running = True

open_canvas()
reset_world()
# game loop
while running:
    handle_events()
    update_world()
    render_world()
    delay(0.01)
# finalization code
close_canvas()
