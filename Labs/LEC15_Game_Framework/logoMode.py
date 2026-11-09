import game_framework 
from pico2d import *
import titleMode

image = None
logo_start_time = 0.0

def init():
    global image, logo_start_time

    image = load_image('tuk_credit.png')
    logo_start_time = get_time()

def finish():
    global image
    del image

def update():
    global logo_start_time

    if get_time() - logo_start_time >= 2.0:
        game_framework.change_mode(titleMode)

def render():
    global image
    clear_canvas()
    image.draw(get_canvas_width() // 2, get_canvas_height() // 2)
    update_canvas()

def handle_events():
    for event in get_events():
        if event.type == SDL_QUIT:
            game_framework.quit()