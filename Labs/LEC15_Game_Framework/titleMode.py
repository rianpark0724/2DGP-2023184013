import game_framework
from pico2d import *

image = None


def init():
    global image
    image = load_image('title.png')


def finish():
    global image
    del image


def update():
    pass


def render():
    clear_canvas()
    image.draw(get_canvas_width() // 2, get_canvas_height() // 2)
    update_canvas()


def handle_events():
    for event in get_events():
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
