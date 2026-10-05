"""LEC09: Sonic 스프라이트 애니메이션 뷰어."""

import pico2d

CANVAS_WIDTH = 800
CANVAS_HEIGHT = 600
LOOP_DELAY = 0.005


def should_quit(events):
    return any(event.type == pico2d.SDL_QUIT or
               (event.type == pico2d.SDL_KEYDOWN and
                event.key == pico2d.SDLK_ESCAPE) for event in events)


def main():
    """애니메이션 뷰어의 실행 진입점."""
    pico2d.open_canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
    try:
        while not should_quit(pico2d.get_events()):
            pico2d.clear_canvas()
            pico2d.update_canvas()
            pico2d.delay(LOOP_DELAY)
    finally:
        pico2d.close_canvas()
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
