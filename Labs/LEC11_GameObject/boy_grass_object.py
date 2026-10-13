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
        self.x, self.y = random.randint(150, 400), 90
        self.frame = 0

    def draw(self):
        self.image.clip_draw(self.frame * 100, 100, 100, 100, self.x, self.y)

    def update(self):
        self.frame = (self.frame + 1) % 8
        self.x += random.randint(1, 10)

        
class Zombie:
    def __init__(self):
        self.image = load_image("zombie_run_animation.png")
        self.x, self.y = random.randint(0, 100), 110
        self.frame = 0

    def draw(self):
        self.image.clip_draw(self.frame * self.image.w // 10, 0, self.image.w // 10, self.image.h, self.x, self.y, 100, 121)

    def update(self):
        self.frame = (self.frame + 1) % 8
        self.x += random.randint(1, 5)

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

    global world
    world = [] # 월드의 모든 객체를 담은 리스트

    grass = Grass()
    world.append(grass)

    team = [Character() for i in range(11)]
    world += team # append를 이용하여 리스트에 추가하는 방법도 있지만, += 연산자를 이용하여 리스트를 합치는 방법도 있음.

    zombies = [Zombie() for i in range(5)]
    world += zombies


def update_world():
    for obj in world:
        obj.update()

def render_world():
    global world
    clear_canvas()
    for obj in world:
        obj.draw()
    update_canvas()

open_canvas()

reset_world()
while running:
    handle_events()
    update_world()
    render_world()
    delay(0.1)

close_canvas()
