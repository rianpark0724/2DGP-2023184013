from pico2d import *

open_canvas()
grass = load_image('grass.png')
character = load_image('animation_sheet.png')


running = True
dir = 0
x = 800 // 2
y = 90


def handle_events():
    global running, dir
    global x, y
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                running = False
            elif event.key == SDLK_LEFT:
                dir -= 1
            elif event.key == SDLK_RIGHT:
                dir += 1
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_LEFT:
                dir += 1
            elif event.key == SDLK_RIGHT:
                dir -= 1
        elif event.type == SDL_MOUSEBUTTONDOWN and event.button == SDL_BUTTON_LEFT:
            print(event.x, event.y)
    pass


frame = 0
while running:

    handle_events()
    if not running:
        break

    clear_canvas()
    grass.draw(400, 30)

    x += dir * 10
    if x < 0:
        x = 0
    elif x > 800:
        x = 800
    
    character.clip_draw(frame * 100, 100, 100, 100, x, y)
    
    update_canvas()
    frame = (frame + 1) % 8
    delay(0.05)
    


close_canvas()
