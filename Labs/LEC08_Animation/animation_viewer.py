"""Drill #8 애니메이션 뷰어 — 23단계: 동작 순차 전환과 전체 무한 반복."""

import json
from math import isfinite
from pathlib import Path
from time import perf_counter

from pico2d import (
    SDL_KEYDOWN,
    SDL_QUIT,
    SDLK_1,
    SDLK_2,
    SDLK_3,
    SDLK_4,
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
DEFAULT_ANIMATION_FPS = 10  # JSON에 fps가 없을 때 사용하는 기본 속도.
REPEAT_LIMIT = 5  # 한 동작을 완전히 재생할 횟수.
WAIT_SECONDS = 1.0  # 5회 완주 후 마지막 프레임을 유지하는 시간.
PREVIEW_ANIMATION_ID = "idle"  # 시작할 동작. 실행 중 숫자 1~4로 바꿀 수 있다.
ANIMATION_KEYS = {SDLK_1: 0, SDLK_2: 1, SDLK_3: 2, SDLK_4: 3}
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
        fps = animation.get("fps", DEFAULT_ANIMATION_FPS)
        if not is_finite_number(fps) or fps <= 0:
            raise ValueError(f"{label}: fps는 0보다 큰 유한한 수여야 합니다. 현재 값: {fps!r}")
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


def begin_animation(animation):
    """선택한 동작의 목록·속도를 적용하고 첫 프레임부터 시작한다."""
    frames = animation["frames"]
    fps = animation.get("fps", DEFAULT_ANIMATION_FPS)
    print(f"재생 동작: {animation.get('name', animation.get('id'))} ({len(frames)}프레임, {fps} FPS)")
    return frames, fps, perf_counter()


def main():
    """각 동작을 5회 재생하고 1초 대기하며 전체 순서를 무한 반복한다."""
    if not is_finite_number(DEFAULT_ANIMATION_FPS) or DEFAULT_ANIMATION_FPS <= 0:
        raise ValueError("DEFAULT_ANIMATION_FPS는 0보다 큰 유한한 수여야 합니다.")

    if not SPRITE_SHEET_PATH.is_file():
        raise FileNotFoundError(
            f"스프라이트 시트를 찾을 수 없습니다: {SPRITE_SHEET_PATH}\n"
            "레이무 시트를 LEC08/assets/reimu_sheet.png로 배치해 주세요."
        )

    # JSON에 등록된 순서대로 순환하되 시작할 동작은 ID로 찾는다.
    animations = load_animations(ANIMATION_DATA_PATH)
    animation_index = next(
        (index for index, item in enumerate(animations) if item.get("id") == PREVIEW_ANIMATION_ID),
        None,
    )
    if animation_index is None:
        raise ValueError(f"시작할 동작을 찾을 수 없습니다: {PREVIEW_ANIMATION_ID}")
    animation = animations[animation_index]
    first_frame = animations[0]["frames"][0]

    # 대기의 첫 프레임을 기준으로 배율을 고정해 동작이 달라도 체격을 유지한다.
    display_scale = CANVAS_HEIGHT * CHARACTER_HEIGHT_RATIO / first_frame["height"]

    open_canvas(CANVAS_WIDTH, CANVAS_HEIGHT)

    try:
        # 이미지는 캔버스를 연 뒤 한 번만 불러오고, 반복문에서 재사용한다.
        sprite_sheet = load_image(str(SPRITE_SHEET_PATH))
        validate_frame_bounds(animations, sprite_sheet)
        print(f"스프라이트 로딩 완료: {SPRITE_SHEET_PATH.name}")
        print("동작 선택: 1 대기 / 2 이동 / 3 일반 공격 / 4 특수 공격")
        print(f"자동 순환: 각 동작 {REPEAT_LIMIT}회 재생 → {WAIT_SECONDS:g}초 대기 → 다음 동작")

        # 이미지 로딩 시간은 재생 시간에서 제외한다.
        frames, animation_fps, animation_started_at = begin_animation(animation)
        completed_loops = 0
        frame_index = 0
        playback_state = "playing"
        waiting_started_at = None
        running = True
        while running:
            # 창이 응답하도록 매 반복에서 운영체제 이벤트를 처리한다.
            for event in get_events():
                if event.type == SDL_QUIT:
                    running = False
                    break
                elif event.type == SDL_KEYDOWN:
                    if event.key == SDLK_ESCAPE:
                        running = False
                        break
                    selected_index = ANIMATION_KEYS.get(event.key)
                    if selected_index is not None and selected_index < len(animations):
                        animation_index = selected_index
                        animation = animations[animation_index]
                        frames, animation_fps, animation_started_at = begin_animation(animation)
                        completed_loops = 0
                        frame_index = 0
                        playback_state = "playing"
                        waiting_started_at = None

            if not running:
                break

            now = perf_counter()
            if playback_state == "playing":
                # 마지막 프레임의 표시 시간이 끝나야 완주 횟수가 증가한다.
                elapsed_time = now - animation_started_at
                elapsed_frames = int(elapsed_time * animation_fps)
                current_loops, frame_index = divmod(elapsed_frames, len(frames))
                current_loops = min(current_loops, REPEAT_LIMIT)

                if current_loops > completed_loops:
                    completed_loops = current_loops
                    print(f"완주: {animation.get('name', animation.get('id'))} — {completed_loops}회")

                if completed_loops == REPEAT_LIMIT:
                    frame_index = len(frames) - 1
                    playback_state = "waiting"
                    waiting_started_at = now
                    print(f"5회 재생 완료: {WAIT_SECONDS:g}초 대기 시작")

            elif playback_state == "waiting":
                # 긴 정지 호출 없이 시간을 확인하므로 위의 이벤트 처리가 계속된다.
                if now - waiting_started_at >= WAIT_SECONDS:
                    # 마지막 동작 다음에는 첫 동작으로 돌아간다.
                    animation_index = (animation_index + 1) % len(animations)
                    animation = animations[animation_index]
                    frames, animation_fps, animation_started_at = begin_animation(animation)
                    completed_loops = 0
                    frame_index = 0
                    playback_state = "playing"
                    waiting_started_at = None

            # 대기 중에는 마지막 프레임, 동작 전환 직후에는 새 첫 프레임을 그린다.
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
