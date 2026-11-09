import game_framework
import game_world
from pico2d import *

image = None

PAUSED_GLYPHS = {
    'P': ('11110', '10001', '10001', '11110', '10000', '10000', '10000'),
    'A': ('01110', '10001', '10001', '11111', '10001', '10001', '10001'),
    'U': ('10001', '10001', '10001', '10001', '10001', '10001', '01110'),
    'S': ('01111', '10000', '10000', '01110', '00001', '00001', '11110'),
    'E': ('11111', '10000', '10000', '11110', '10000', '10000', '11111'),
    'D': ('11110', '10001', '10001', '10001', '10001', '10001', '11110'),
}


def init():
    global image
    image = load_image('tuk_credit.png')


def finish():
    global image
    del image


def update():
    pass


def render():
    clear_canvas()
    game_world.render()

    center_x = get_canvas_width() // 2
    center_y = get_canvas_height() // 2
    image.draw(center_x, center_y)

    pixel_size = 8
    letter_width = 5 * pixel_size
    spacing = 2 * pixel_size
    label_width = len('PAUSED') * letter_width + (len('PAUSED') - 1) * spacing
    left = center_x - label_width // 2
    bottom = center_y - 180

    for letter_index, letter in enumerate('PAUSED'):
        for row, pattern in enumerate(PAUSED_GLYPHS[letter]):
            for column, pixel in enumerate(pattern):
                if pixel == '1':
                    x = left + letter_index * (letter_width + spacing) + column * pixel_size
                    y = bottom + (6 - row) * pixel_size
                    draw_rectangle(x, y, x + pixel_size, y + pixel_size,
                                   20, 55, 100, 255, True)

    update_canvas()


def handle_events():
    for event in get_events():
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_p:
            game_framework.pop_mode()
