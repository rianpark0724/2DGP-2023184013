"""Keyboard-controlled boy animation for LEC10."""

from pathlib import Path

import pico2d as p2

CANVAS_WIDTH = 800
CANVAS_HEIGHT = 600
ASSET_DIR = Path(__file__).resolve().parent
FRAME_SIZE = 100
FRAME_COUNT = 8


class Character:
    def __init__(self):
        self.x = CANVAS_WIDTH / 2
        self.y = CANVAS_HEIGHT / 2
        self.frame = 0


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


def draw(background, character, boy):
    p2.clear_canvas()
    background.draw(CANVAS_WIDTH / 2, CANVAS_HEIGHT / 2,
                    CANVAS_WIDTH, CANVAS_HEIGHT)
    character.clip_draw(boy.frame * FRAME_SIZE, 300, FRAME_SIZE, FRAME_SIZE,
                        boy.x, boy.y, FRAME_SIZE, FRAME_SIZE)
    p2.update_canvas()


def main():
    p2.open_canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
    try:
        background = load_asset('TUK_GROUND.png')
        character = load_asset('animation_sheet.png')
        boy = Character()
        while handle_events():
            draw(background, character, boy)
            p2.delay(0.01)
    except RuntimeError as error:
        print(error)
        return 1
    finally:
        p2.close_canvas()
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
