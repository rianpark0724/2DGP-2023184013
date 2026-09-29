"""Drill #8 애니메이션 뷰어 — 04단계: 창과 기본 렌더링 루프."""

from pico2d import (
    SDL_QUIT,
    clear_canvas,
    close_canvas,
    delay,
    get_events,
    open_canvas,
    update_canvas,
)


CANVAS_WIDTH = 800
CANVAS_HEIGHT = 600
LOOP_DELAY = 0.01  # 빈 화면에서도 루프가 CPU를 계속 점유하지 않도록 양보한다.


def main():
    """창을 열고 배경을 갱신하다가 창 닫기 요청을 받으면 종료한다."""
    open_canvas(CANVAS_WIDTH, CANVAS_HEIGHT)

    try:
        running = True
        while running:
            # 창이 응답하도록 매 반복에서 운영체제 이벤트를 처리한다.
            for event in get_events():
                if event.type == SDL_QUIT:
                    running = False

            if not running:
                break

            clear_canvas()
            # 이후 단계에서 여기에 캐릭터 프레임을 그린다.
            update_canvas()
            delay(LOOP_DELAY)
    finally:
        close_canvas()


if __name__ == "__main__":
    main()