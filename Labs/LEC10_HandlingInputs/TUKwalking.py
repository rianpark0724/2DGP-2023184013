"""Keyboard-controlled boy animation for LEC10."""

from pathlib import Path
from math import hypot
from time import perf_counter

import pico2d as p2

CANVAS_WIDTH = 800
CANVAS_HEIGHT = 600
ASSET_DIR = Path(__file__).resolve().parent
FRAME_SIZE = 100
FRAME_COUNT = 8
ANIMATION_FPS = 10
MOVE_SPEED = 200
ANIMATION_ROWS = {'idle_right': 300, 'idle_left': 200}
ARROW_KEYS = {p2.SDLK_LEFT, p2.SDLK_RIGHT, p2.SDLK_UP, p2.SDLK_DOWN}


class Character:
    def __init__(self):
        self.x = CANVAS_WIDTH / 2
        self.y = CANVAS_HEIGHT / 2
        self.frame = 0
        self.facing = 'right'
        self.state = 'idle_right'
        self.animation_time = 0.0

    def update_movement(self, pressed_keys, dt):
        dx = int(p2.SDLK_RIGHT in pressed_keys) - int(p2.SDLK_LEFT in pressed_keys)
        dy = int(p2.SDLK_UP in pressed_keys) - int(p2.SDLK_DOWN in pressed_keys)
        length = hypot(dx, dy)
        if length:
            dx /= length
            dy /= length
        self.x += dx * MOVE_SPEED * dt
        self.y += dy * MOVE_SPEED * dt

    def update_animation(self, dt):
        self.animation_time += dt
        frame_duration = 1 / ANIMATION_FPS
        while self.animation_time >= frame_duration:
            self.animation_time -= frame_duration
            self.frame = (self.frame + 1) % FRAME_COUNT


def load_asset(name):
    path = ASSET_DIR / name
    try:
        return p2.load_image(str(path))
    except Exception as error:
        raise RuntimeError(f'이미지 로드 실패: {path}') from error


def handle_events(pressed_keys):
    for event in p2.get_events():
        if event.type == p2.SDL_QUIT:
            return False
        if event.type == p2.SDL_KEYDOWN and event.key == p2.SDLK_ESCAPE:
            return False
        if event.type == p2.SDL_KEYDOWN and event.key in ARROW_KEYS:
            pressed_keys.add(event.key)
        elif event.type == p2.SDL_KEYUP and event.key in ARROW_KEYS:
            pressed_keys.discard(event.key)
    return True


def draw(background, character, boy):
    p2.clear_canvas()
    background.draw(CANVAS_WIDTH / 2, CANVAS_HEIGHT / 2,
                    CANVAS_WIDTH, CANVAS_HEIGHT)
    character.clip_draw(boy.frame * FRAME_SIZE, ANIMATION_ROWS[boy.state],
                        FRAME_SIZE, FRAME_SIZE,
                        boy.x, boy.y, FRAME_SIZE, FRAME_SIZE)
    p2.update_canvas()


def main():
    p2.open_canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
    try:
        background = load_asset('TUK_GROUND.png')
        character = load_asset('animation_sheet.png')
        boy = Character()
        pressed_keys = set()
        previous_time = perf_counter()
        while handle_events(pressed_keys):
            current_time = perf_counter()
            dt = current_time - previous_time
            previous_time = current_time
            boy.update_movement(pressed_keys, dt)
            boy.update_animation(dt)
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
