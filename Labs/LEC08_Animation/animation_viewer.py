"""Drill #8 애니메이션 뷰어 — 07단계: 첫 캐릭터 프레임 표시."""

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
LOOP_DELAY = 0.01  # 빈 화면에서도 루프가 CPU를 계속 점유하지 않도록 양보한다.
BASE_DIR = Path(__file__).resolve().parent
SPRITE_SHEET_PATH = BASE_DIR / "assets" / "reimu_sheet.png"

# 첨부된 899×2048 시트의 왼쪽 위 첫 자세. 좌상단 기준으로 기록한다.
FIRST_FRAME_LEFT = 0
FIRST_FRAME_TOP = 27
FIRST_FRAME_WIDTH = 34
FIRST_FRAME_HEIGHT = 52


def main():
    """첫 프레임을 중앙에 표시하고 창 닫기 또는 Escape로 종료한다."""
    if not SPRITE_SHEET_PATH.is_file():
        raise FileNotFoundError(
            f"스프라이트 시트를 찾을 수 없습니다: {SPRITE_SHEET_PATH}\n"
            "레이무 시트를 LEC08/assets/reimu_sheet.png로 배치해 주세요."
        )

    open_canvas(CANVAS_WIDTH, CANVAS_HEIGHT)

    try:
        # 이미지는 캔버스를 연 뒤 한 번만 불러오고, 반복문에서 재사용한다.
        sprite_sheet = load_image(str(SPRITE_SHEET_PATH))
        print(f"스프라이트 로딩 완료: {SPRITE_SHEET_PATH.name}")

        # pico2d의 잘라내기 좌표는 좌하단 기준이므로 Y 좌표를 변환한다.
        frame_bottom = sprite_sheet.h - FIRST_FRAME_TOP - FIRST_FRAME_HEIGHT

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
                FIRST_FRAME_LEFT,
                frame_bottom,
                FIRST_FRAME_WIDTH,
                FIRST_FRAME_HEIGHT,
                CANVAS_WIDTH // 2,
                CANVAS_HEIGHT // 2,
            )
            update_canvas()
            delay(LOOP_DELAY)
    finally:
        close_canvas()


if __name__ == "__main__":
    main()
