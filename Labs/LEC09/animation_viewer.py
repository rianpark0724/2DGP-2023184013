"""LEC09: Sonic 스프라이트 애니메이션 뷰어."""

import pico2d

CANVAS_WIDTH = 800
CANVAS_HEIGHT = 600


def main():
    """애니메이션 뷰어의 실행 진입점."""
    pico2d.open_canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
    try:
        pico2d.clear_canvas()
        pico2d.update_canvas()
    finally:
        pico2d.close_canvas()
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
