"""Keyboard-controlled boy animation for LEC10."""

from pathlib import Path

import pico2d as p2

CANVAS_WIDTH = 800
CANVAS_HEIGHT = 600
ASSET_DIR = Path(__file__).resolve().parent


def load_asset(name):
    path = ASSET_DIR / name
    try:
        return p2.load_image(str(path))
    except Exception as error:
        raise RuntimeError(f'이미지 로드 실패: {path}') from error


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
        background = load_asset('TUK_GROUND.png')
        character = load_asset('animation_sheet.png')
        while handle_events():
            p2.clear_canvas()
            p2.update_canvas()
            p2.delay(0.01)
    except RuntimeError as error:
        print(error)
        return 1
    finally:
        p2.close_canvas()
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
