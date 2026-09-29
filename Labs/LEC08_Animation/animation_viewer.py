"""Drill #8 애니메이션 뷰어 — 09단계: 캐릭터 비율 유지 확대."""

import json
from pathlib import Path

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
LOOP_DELAY = 0.01  # 빈 화면에서도 루프가 CPU를 계속 점유하지 않도록 양보한다.
BASE_DIR = Path(__file__).resolve().parent
SPRITE_SHEET_PATH = BASE_DIR / "assets" / "reimu_sheet.png"
ANIMATION_DATA_PATH = BASE_DIR / "assets" / "animations.json"


def load_animations(path):
    """UTF-8 JSON에서 동작별 프레임 목록을 읽는다. 좌표는 좌상단 기준이다."""
    with path.open("r", encoding="utf-8") as file:
        data = json.load(file)
    return data["animations"]


def main():
    """첫 프레임을 확대해 중앙에 표시하고 창 닫기 또는 Escape로 종료한다."""
    if not SPRITE_SHEET_PATH.is_file():
        raise FileNotFoundError(
            f"스프라이트 시트를 찾을 수 없습니다: {SPRITE_SHEET_PATH}\n"
            "레이무 시트를 LEC08/assets/reimu_sheet.png로 배치해 주세요."
        )

    # 이번 단계에서는 첫 동작의 첫 프레임만 표시한다.
    animations = load_animations(ANIMATION_DATA_PATH)
    first_frame = animations[0]["frames"][0]

    # 첫 프레임을 기준으로 배율을 한 번 계산한다. 가로·세로에 같은 배율을 쓴다.
    display_scale = CANVAS_HEIGHT * CHARACTER_HEIGHT_RATIO / first_frame["height"]
    display_width = round(first_frame["width"] * display_scale)
    display_height = round(first_frame["height"] * display_scale)

    open_canvas(CANVAS_WIDTH, CANVAS_HEIGHT)

    try:
        # 이미지는 캔버스를 연 뒤 한 번만 불러오고, 반복문에서 재사용한다.
        sprite_sheet = load_image(str(SPRITE_SHEET_PATH))
        print(f"스프라이트 로딩 완료: {SPRITE_SHEET_PATH.name}")

        # pico2d의 잘라내기 좌표는 좌하단 기준이므로 Y 좌표를 변환한다.
        frame_bottom = sprite_sheet.h - first_frame["top"] - first_frame["height"]

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

            clear_canvas()
            sprite_sheet.clip_draw(
                first_frame["left"],
                frame_bottom,
                first_frame["width"],
                first_frame["height"],
                CANVAS_WIDTH // 2,
                CANVAS_HEIGHT // 2,
                display_width,
                display_height,
            )
            update_canvas()
            delay(LOOP_DELAY)
    finally:
        close_canvas()


if __name__ == "__main__":
    main()
