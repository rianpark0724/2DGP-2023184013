"""LEC09: Sonic 스프라이트 애니메이션 뷰어."""

from pathlib import Path
import sys

import pico2d

CANVAS_WIDTH = 800
CANVAS_HEIGHT = 600
LOOP_DELAY = 0.005
SPRITE_PATH = Path(__file__).resolve().with_name('sonic-sprite.png')


def should_quit(events):
    return any(event.type == pico2d.SDL_QUIT or
               (event.type == pico2d.SDL_KEYDOWN and
                event.key == pico2d.SDLK_ESCAPE) for event in events)


def load_sheet(path):
    """실패한 파일 경로를 포함해 이미지 로드 오류를 전달한다."""
    try:
        if not path.is_file():
            raise FileNotFoundError('파일이 없습니다.')
        sheet = pico2d.load_image(str(path))
        if sheet is None:
            raise OSError('이미지 로더가 결과를 반환하지 않았습니다.')
        return sheet
    except (OSError, ValueError) as error:
        raise OSError(f'스프라이트 로드 실패: {path} ({error})') from error


def main():
    """애니메이션 뷰어의 실행 진입점."""
    pico2d.open_canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
    sheet = None
    try:
        sheet = load_sheet(SPRITE_PATH)
        while not should_quit(pico2d.get_events()):
            pico2d.clear_canvas()
            pico2d.update_canvas()
            pico2d.delay(LOOP_DELAY)
    except OSError as error:
        print(error, file=sys.stderr)
        return 1
    finally:
        # SDL 렌더러가 파괴되기 전에 이미지 텍스처를 해제한다.
        del sheet
        pico2d.close_canvas()
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
