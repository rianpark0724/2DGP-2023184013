from pico2d import *

image = None
running = True
logo_start_time = 0.0

def init():
    global image, running, logo_start_time

    image = load_image('tuk_credit.png')
    running - True
    logo_start_time = get_time()

def finish():
    global image
    del image

def update():
    global running, logo_start_time

    if get_time() - logo_start_time >= 2.0:
        running = False

def render():
    global image
    clear_canvas()
    image.draw(get_canvas_width() // 2, get_canvas_height() // 2)
    update_canvas()

def handle_events():
    events = get_events()