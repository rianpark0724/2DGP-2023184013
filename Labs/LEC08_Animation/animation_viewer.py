"""Drill #8 애니메이션 뷰어 — 17단계: 일반 공격 동작 추가."""

import json
from math import isfinite
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
PREVIEW_ANIMATION_ID = "attack"  # "idle", "move", "attack" 중 미리 볼 동작을 선택한다.
LOOP_DELAY = 0.01  # 루프가 CPU를 계속 점유하지 않도록 양보한다.
BASE_DIR = Path(__file__).resolve().parent
SPRITE_SHEET_PATH = BASE_DIR / "assets" / "reimu_sheet.png"
ANIMATION_DATA_PATH = BASE_DIR / "assets" / "animations.json"


def load_animations(path):
    """UTF-8 JSON을 읽고 프레임 구조를 검사한다. 좌표는 좌상단 기준이다."""
    try:
        with path.open("r", encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"애니메이션 데이터 파일을 찾을 수 없습니다: {path}") from None
    except json.JSONDecodeError as error:
        raise ValueError(
            f"{path.name}: JSON 문법 오류 ({error.lineno}행 {error.colno}열): {error.msg}"
        ) from None

    if not isinstance(data, dict):
        raise ValueError(f"{path.name}: 최상위 데이터는 객체여야 합니다.")

    animations = data.get("animations")
    validate_animations(animations)
    return animations


def is_finite_number(value):
    """문자열, 불리언, NaN, 무한대 등을 제외한 수인지 확인한다."""
    if type(value) not in (int, float):
        return False
    try:
        return isfinite(value)
    except OverflowError:
        return False


def validate_animations(animations):
    """이미지를 불러오기 전에 동작 목록과 프레임 수치를 검사한다."""
    if not isinstance(animations, list) or not animations:
        raise ValueError("animations는 하나 이상의 동작을 가진 목록이어야 합니다.")

    for animation_index, animation in enumerate(animations, start=1):
        if not isinstance(animation, dict):
            raise ValueError(f"동작 {animation_index}: 동작 데이터는 객체여야 합니다.")
        label = f"동작 {animation_index} ({animation.get('name', animation.get('id', '이름 없음'))})"
        frames = animation.get("frames")
        if not isinstance(frames, list) or not frames:
            raise ValueError(f"{label}: frames는 하나 이상의 프레임을 가진 목록이어야 합니다.")

        for frame_index, frame in enumerate(frames, start=1):
            frame_label = f"{label}, 프레임 {frame_index}"
            if not isinstance(frame, dict):
                raise ValueError(f"{frame_label}: 프레임 데이터는 객체여야 합니다.")

            for key in ("left", "top", "width", "height"):
                value = frame.get(key)
                minimum = 1 if key in ("width", "height") else 0
                if type(value) is not int or value < minimum:
                    raise ValueError(
                        f"{frame_label}: {key}는 {minimum} 이상의 정수여야 합니다. 현재 값: {value!r}"
                    )

            for key, size_key in (("anchor_x", "width"), ("anchor_y", "height")):
                if key not in frame:
                    continue  # 기준점 생략 시 기존처럼 프레임 중심을 사용한다.
                value = frame[key]
                if not is_finite_number(value) or not 0 <= value <= frame[size_key]:
                    raise ValueError(
                        f"{frame_label}: {key}는 0~{frame[size_key]} 범위의 유한한 수여야 합니다. "
                        f"현재 값: {value!r}"
                    )


def validate_frame_bounds(animations, sprite_sheet):
    """실제로 불러온 이미지의 크기로 모든 프레임 영역을 검사한다."""
    for animation_index, animation in enumerate(animations, start=1):
        label = f"동작 {animation_index} ({animation.get('name', animation.get('id', '이름 없음'))})"
        for frame_index, frame in enumerate(animation["frames"], start=1):
            right = frame["left"] + frame["width"]
            bottom = frame["top"] + frame["height"]
            if right > sprite_sheet.w or bottom > sprite_sheet.h:
                raise ValueError(
                    f"{label}, 프레임 {frame_index}: 프레임 영역이 이미지 경계를 벗어납니다. "
                    f"영역=({frame['left']}, {frame['top']}, {frame['width']}, {frame['height']}), "
                    f"이미지={sprite_sheet.w}×{sprite_sheet.h}"
                )


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
    """선택한 동작을 계속 반복하고 창 닫기 또는 Escape로 종료한다."""
    if not is_finite_number(ANIMATION_FPS) or ANIMATION_FPS <= 0:
        raise ValueError("ANIMATION_FPS는 0보다 큰 유한한 수여야 합니다.")

    if not SPRITE_SHEET_PATH.is_file():
        raise FileNotFoundError(
            f"스프라이트 시트를 찾을 수 없습니다: {SPRITE_SHEET_PATH}\n"
            "레이무 시트를 LEC08/assets/reimu_sheet.png로 배치해 주세요."
        )

    # 자동 순환을 구현하기 전에는 ID로 선택한 동작을 개별 확인한다.
    animations = load_animations(ANIMATION_DATA_PATH)
    animation = next(
        (item for item in animations if item.get("id") == PREVIEW_ANIMATION_ID),
        None,
    )
    if animation is None:
        raise ValueError(f"미리보기 동작을 찾을 수 없습니다: {PREVIEW_ANIMATION_ID}")
    frames = animation["frames"]
    first_frame = animations[0]["frames"][0]

    # 대기의 첫 프레임을 기준으로 배율을 고정해 동작이 달라도 체격을 유지한다.
    display_scale = CANVAS_HEIGHT * CHARACTER_HEIGHT_RATIO / first_frame["height"]

    open_canvas(CANVAS_WIDTH, CANVAS_HEIGHT)

    try:
        # 이미지는 캔버스를 연 뒤 한 번만 불러오고, 반복문에서 재사용한다.
        sprite_sheet = load_image(str(SPRITE_SHEET_PATH))
        validate_frame_bounds(animations, sprite_sheet)
        print(f"스프라이트 로딩 완료: {SPRITE_SHEET_PATH.name}")
        print(f"재생 동작: {animation.get('name', PREVIEW_ANIMATION_ID)} ({len(frames)}프레임)")

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
