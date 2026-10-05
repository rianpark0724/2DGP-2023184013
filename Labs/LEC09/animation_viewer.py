"""LEC09: Sonic 스프라이트 애니메이션 뷰어."""

from dataclasses import dataclass
from pathlib import Path
import sys

import pico2d

CANVAS_WIDTH = 800
CANVAS_HEIGHT = 600
SCALE = 4
LOOP_DELAY = 0.005
SPRITE_PATH = Path(__file__).resolve().with_name('sonic-sprite.png')

# 원본 399x525, 좌상단 기준. 명칭은 공식 동작명이 아닌 시각적 분류다.
# 같은 줄에서도 포즈가 달라지는 영역은 별도 동작으로 나눈다.
ANIMATION_NOTES = (
    ('idle', '대기', '1행 앞 7장: 서 있는 자세와 손·발 변화'),
    ('look_up', '위 보기', '1행 다음 2장: 머리를 위로 드는 자세'),
    ('crouch', '웅크리기', '1행 10번째: 몸을 낮춘 단일 포즈'),
    ('curl', '몸 말기', '1행 마지막: 몸을 접은 단일 포즈'),
    ('walk', '걷기', '2행 12장: 발과 팔이 교차하는 연속 동작'),
    ('run', '달리기', '3행 6장: 보폭과 붉은 발 궤적 변화'),
    ('roll', '회전', '4행 앞 8장: 몸을 말고 회전'),
    ('ball', '공 모양', '4행 마지막: 원형 단일 포즈'),
    ('ball_spin', '공 회전', '5행 6장: 타원형과 하이라이트 변화'),
    ('dash_a', '대시 A', '6행 6장: 좁은 붉은 궤적을 포함한 동작'),
    ('dash_b', '대시 B', '7행 6장: 넓은 붉은 궤적을 포함한 동작'),
    ('turn', '공중 방향 전환', '8행 앞 6장: 정면·측면·뒷면 연속 포즈'),
    ('hurt', '넘어짐', '8행 마지막 2장: 옆으로 누운 포즈'),
    ('brake', '제동', '9행 8장: 뒤로 기울며 방향이 바뀌는 포즈'),
    ('fall', '낙하', '10행 앞 2장: 팔을 벌린 포즈'),
    ('victory', '손짓', '10행 마지막 2장: 서서 손을 움직이는 포즈'),
)
# 제외: y=1..32 제목, y>=472 제작자 문구 및 하단의 노랑/갈색 캐릭터.
# 하단 두 캐릭터는 서로 다른 색·형상의 각 1장으로, 크레딧 영역의 부가
# 그림으로 분류했다. 파란 Sonic 동작과 연결되는 연속 프레임은 없다.
# 불확실성: idle/look_up 경계와 dash_a/dash_b 명칭은 이미지 기반 해석이다.
# 이 해석과 무관하게 본문 캐릭터 76장은 모두 포함한다.


@dataclass(frozen=True)
class Frame:
    """좌상단 기준 원본 영역. 너비와 높이는 프레임마다 다를 수 있다."""
    x: int
    y: int
    width: int
    height: int


@dataclass(frozen=True)
class Animation:
    id: str
    frames: tuple[Frame, ...]


ANIMATIONS = (
    Animation('idle', (
        Frame(1, 39, 29, 39), Frame(31, 40, 26, 38),
        Frame(58, 39, 29, 39), Frame(87, 40, 29, 38),
        Frame(118, 40, 30, 38), Frame(150, 40, 30, 38),
        Frame(182, 40, 29, 38),
    )),
    Animation('look_up', (Frame(211, 39, 29, 38), Frame(240, 39, 29, 38))),
    Animation('crouch', (Frame(270, 45, 24, 32),)),
    Animation('curl', (Frame(302, 51, 29, 26),)),
    Animation('walk', (
        Frame(8, 80, 26, 37), Frame(37, 80, 27, 37),
        Frame(65, 80, 31, 38), Frame(97, 80, 37, 37),
        Frame(135, 80, 32, 35), Frame(170, 79, 32, 38),
        Frame(206, 79, 26, 38), Frame(238, 80, 24, 37),
        Frame(263, 80, 30, 37), Frame(295, 80, 36, 37),
        Frame(334, 80, 32, 36), Frame(370, 79, 29, 38),
    )),
    Animation('run', (
        Frame(1, 124, 33, 40), Frame(39, 124, 35, 39),
        Frame(89, 125, 35, 38), Frame(130, 121, 34, 42),
        Frame(181, 122, 34, 41), Frame(228, 122, 33, 40),
    )),
    Animation('roll', (
        Frame(1, 169, 29, 30), Frame(35, 167, 29, 31),
        Frame(67, 169, 30, 29), Frame(98, 169, 31, 29),
        Frame(131, 168, 29, 30), Frame(162, 168, 29, 31),
        Frame(193, 170, 30, 29), Frame(230, 170, 31, 29),
    )),
    Animation('ball', (Frame(268, 170, 30, 30),)),
    Animation('ball_spin', (
        Frame(1, 206, 30, 27), Frame(36, 206, 29, 27),
        Frame(70, 206, 29, 27), Frame(105, 206, 29, 27),
        Frame(139, 206, 29, 27), Frame(174, 206, 29, 27),
    )),
    Animation('dash_a', (
        Frame(1, 239, 29, 35), Frame(36, 239, 30, 35),
        Frame(74, 239, 31, 35), Frame(111, 238, 31, 36),
        Frame(149, 239, 30, 35), Frame(186, 238, 31, 36),
    )),
    Animation('dash_b', (
        Frame(1, 283, 29, 35), Frame(36, 283, 30, 35),
        Frame(72, 286, 39, 31), Frame(123, 285, 39, 32),
        Frame(172, 286, 39, 31), Frame(218, 285, 38, 32),
    )),
    Animation('turn', (
        Frame(1, 326, 24, 45), Frame(31, 327, 29, 44),
        Frame(65, 327, 20, 44), Frame(90, 327, 25, 43),
        Frame(119, 327, 25, 43), Frame(149, 327, 20, 44),
    )),
    Animation('hurt', (Frame(184, 341, 40, 28), Frame(232, 341, 39, 27))),
    Animation('brake', (
        Frame(1, 379, 27, 38), Frame(31, 379, 31, 36),
        Frame(64, 379, 31, 36), Frame(99, 377, 33, 38),
        Frame(136, 379, 32, 36), Frame(176, 379, 33, 36),
        Frame(217, 379, 33, 36), Frame(254, 378, 33, 36),
    )),
    Animation('fall', (Frame(6, 429, 34, 40), Frame(49, 426, 34, 43))),
    Animation('victory', (Frame(96, 427, 23, 39), Frame(125, 427, 23, 39))),
)


def clip_rect(frame, image_height):
    """원본 좌상단 영역을 pico2d의 좌하단 좌표로 변환한다."""
    return (frame.x, image_height - frame.y - frame.height,
            frame.width, frame.height)


def validate_animations(animations, image_width, image_height):
    if not animations:
        raise ValueError('동작 목록이 비어 있습니다.')
    ids = set()
    for animation in animations:
        if not animation.id or animation.id in ids:
            raise ValueError(f'동작 ID가 비어 있거나 중복됩니다: {animation.id}')
        ids.add(animation.id)
        if not animation.frames:
            raise ValueError(f'{animation.id}: 프레임이 없습니다.')
        for index, frame in enumerate(animation.frames):
            values = (frame.x, frame.y, frame.width, frame.height)
            if (not all(type(value) is int for value in values) or
                    frame.x < 0 or frame.y < 0 or
                    frame.width <= 0 or frame.height <= 0 or
                    frame.x + frame.width > image_width or
                    frame.y + frame.height > image_height):
                raise ValueError(f'{animation.id}[{index}]: 잘못된 프레임 영역 {frame}')


def should_quit(events):
    return any(event.type == pico2d.SDL_QUIT or
               (event.type == pico2d.SDL_KEYDOWN and
                event.key == pico2d.SDLK_ESCAPE) for event in events)


def draw_frame(sheet, frame):
    sheet.clip_draw(*clip_rect(frame, sheet.h),
                    CANVAS_WIDTH // 2, CANVAS_HEIGHT // 2,
                    frame.width * SCALE, frame.height * SCALE)


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
    pico2d.hide_lattice()
    sheet = None
    try:
        sheet = load_sheet(SPRITE_PATH)
        validate_animations(ANIMATIONS, sheet.w, sheet.h)
        while not should_quit(pico2d.get_events()):
            pico2d.clear_canvas()
            draw_frame(sheet, ANIMATIONS[0].frames[0])
            pico2d.update_canvas()
            pico2d.delay(LOOP_DELAY)
    except (OSError, ValueError) as error:
        print(error, file=sys.stderr)
        return 1
    finally:
        # SDL 렌더러가 파괴되기 전에 이미지 텍스처를 해제한다.
        del sheet
        pico2d.close_canvas()
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
