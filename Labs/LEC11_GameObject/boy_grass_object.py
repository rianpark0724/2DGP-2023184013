from pico2d import *
import random


# Game object class here
class Grass:
    def __init__(self): # 생성자 함수. 객체가 생성될 때 자동 처음으로 호출됨. 초기 상태를 설정.
        self.image = load_image("grass.png") 

    def draw(self):
        self.image.draw(400, 30) # 이미지의 중심 좌표를 기준으로 그림. (400, 30) 좌표에 그림.
    
    def update(self):
        pass

class Character:
    def __init__(self):
        self.image = load_image("animation_sheet.png")
        self.x, self.y = 0, 90
        self.frame = 0

    def draw(self):
        self.image.clip_draw(self.frame * 100, 100, 100, 100, self.x, self.y)

    def update(self):
        self.frame = (self.frame + 1) % 8
        self.x += 5

def handle_events():
    global running
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False

def reset_world():
    global running
    running = True

    global grass
    grass = Grass()

    global character
    character = Character()

def update_world():
    global grass
    grass.update()

    global character
    character.update()

def render_world():
    global grass
    global character
    clear_canvas()
    grass.draw()
    character.draw()
    update_canvas()

open_canvas()

reset_world()
while running:
    handle_events()
    update_world()
    render_world()
    delay(0.01)

close_canvas()
