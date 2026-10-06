"""Keyboard-controlled boy animation for LEC10."""

import pico2d as p2

CANVAS_WIDTH = 800
CANVAS_HEIGHT = 600


def handle_events():
    for event in p2.get_events():
        if event.type == p2.SDL_QUIT:
            return False
        if event.type == p2.SDL_KEYDOWN and event.key == p2.SDLK_ESCAPE:
            return False
    return True


def main():
    p2.open_canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
    try:
        while handle_events():
            p2.clear_canvas()
            p2.update_canvas()
            p2.delay(0.01)
    finally:
        p2.close_canvas()


if __name__ == '__main__':
    main()
