"""Keyboard-controlled boy animation for LEC10."""

import pico2d as p2

CANVAS_WIDTH = 800
CANVAS_HEIGHT = 600


def main():
    p2.open_canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
    try:
        p2.clear_canvas()
        p2.update_canvas()
    finally:
        p2.close_canvas()


if __name__ == '__main__':
    main()
