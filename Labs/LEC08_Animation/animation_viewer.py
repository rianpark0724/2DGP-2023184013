"""Drill #8 애니메이션 뷰어 — 14단계: 가변 크기 프레임 렌더링 분리."""

import json
from pathlib import Path
from time import perf_counter

from pico2d import (
    SDL_KEYDOWN,
    SDL_QUIT,
    SDLK_ESCAPE,
    clear_canvas,
    close_canvas,
    delay,
    get_events,
    load_image,
    open_canvas,
    update_canvas,
)


CANVAS_WIDTH = 800
CANVAS_HEIGHT = 600
CHARACTER_HEIGHT_RATIO = 0.55  # 첫 프레임을 창 높이의 55% 크기로 표시한다.
ANIMATION_FPS = 10  # 애니메이션 재생 속도. 화면 갱신 속도와 별개다.
LOOP_DELAY = 0.01  # 루프가 CPU를 계속 점유하지 않도록 양보한다.
BASE_DIR = Path(__file__).resolve().parent
SPRITE_SHEET_PATH = BASE_DIR / "assets" / "reimu_sheet.png"
ANIMATION_DATA_PATH = BASE_DIR / "assets" / "animations.json"


def load_animations(path):
    """UTF-8 JSON에서 동작별 프레임 목록을 읽는다. 좌표는 좌상단 기준이다."""
    with path.open("r", encoding="utf-8") as file:
        data = json.load(file)
    return data["animations"]


def get_draw_position(frame, display_width, display_height, target_x, target_y):
    """프레임의 기준점이 화면의 목표 위치에 오도록 그리기 중심을 계산한다.

    JSON의 anchor_x, anchor_y는 잘라낸 프레임의 좌상단 기준 좌표다.
    생략하면 프레임 중심을 사용한다. 예: 110×166 프레임은 (55, 83).
    """
    anchor_x = frame.get("anchor_x", frame["width"] / 2)
    anchor_y = frame.get("anchor_y", frame["height"] / 2)

    # 실제 출력 크기를 사용해 반올림된 확대 크기에도 기준점을 맞춘다.
    draw_x = target_x + (0.5 - anchor_x / frame["width"]) * display_width
    # 프레임의 Y는 아래로, 캔버스의 Y는 위로 증가하므로 부호가 다르다.
    draw_y = target_y + (anchor_y / frame["height"] - 0.5) * display_height
    return draw_x, draw_y


def draw_frame(sprite_sheet, frame, display_scale, target_x, target_y):
    """크기가 서로 다른 프레임을 공통 배율과 개별 기준점으로 그린다.

    원본 영역과 출력 크기를 구분한다. 모든 프레임을 같은 사각형에
    맞추지 않고 각 프레임의 폭과 높이에 동일한 확대 배율을 적용한다.
    """
    display_width = round(frame["width"] * display_scale)
    display_height = round(frame["height"] * display_scale)
    draw_x, draw_y = get_draw_position(
        frame, display_width, display_height, target_x, target_y
    )

    # pico2d의 잘라내기 좌표는 좌하단 기준이므로 Y 좌표를 변환한다.
    frame_bottom = sprite_sheet.h - frame["top"] - frame["height"]
    sprite_sheet.clip_draw(
        frame["left"],
        frame_bottom,
        frame["width"],
        frame["height"],
        draw_x,
        draw_y,
        display_width,
        display_height,
    )


def main():
    """첫 동작을 계속 반복하고 창 닫기 또는 Escape로 종료한다."""
    if not SPRITE_SHEET_PATH.is_file():
        raise FileNotFoundError(
            f"스프라이트 시트를 찾을 수 없습니다: {SPRITE_SHEET_PATH}\n"
            "레이무 시트를 LEC08/assets/reimu_sheet.png로 배치해 주세요."
        )

    # 이번 단계에서는 첫 동작만 반복 재생한다.
    animations = load_animations(ANIMATION_DATA_PATH)
    frames = animations[0]["frames"]
    first_frame = frames[0]

    # 첫 프레임을 기준으로 배율을 한 번 계산한다. 가로·세로에 같은 배율을 쓴다.
    display_scale = CANVAS_HEIGHT * CHARACTER_HEIGHT_RATIO / first_frame["height"]

    open_canvas(CANVAS_WIDTH, CANVAS_HEIGHT)

    try:
        # 이미지는 캔버스를 연 뒤 한 번만 불러오고, 반복문에서 재사용한다.
        sprite_sheet = load_image(str(SPRITE_SHEET_PATH))
        print(f"스프라이트 로딩 완료: {SPRITE_SHEET_PATH.name}")

        # 이미지 로딩 시간은 재생 시간에서 제외한다.
        animation_started_at = perf_counter()
        running = True
        while running:
            # 창이 응답하도록 매 반복에서 운영체제 이벤트를 처리한다.
            for event in get_events():
                if event.type == SDL_QUIT:
                    running = False
                elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
                    running = False

            if not running:
                break

            # 실제 경과 시간으로 프레임을 선택해 화면 갱신 횟수에 의존하지 않는다.
            elapsed_time = perf_counter() - animation_started_at
            # 마지막 프레임의 표시 시간이 끝나면 첫 프레임으로 돌아간다.
            frame_index = int(elapsed_time * ANIMATION_FPS) % len(frames)
            frame = frames[frame_index]

            clear_canvas()
            draw_frame(
                sprite_sheet,
                frame,
                display_scale,
                CANVAS_WIDTH / 2,
                CANVAS_HEIGHT / 2,
            )
            update_canvas()
            delay(LOOP_DELAY)
    finally:
        close_canvas()


if __name__ == "__main__":
    main()
