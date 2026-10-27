from math import pi

from pico2d import load_image
from transitions import Machine

class Boy:
    def __init__(self):
        self.x, self.y = 400, 90
        self.frame = 0
        self.face_dir = 1
        self.image = load_image('animation_sheet.png')
        self.machine = Machine(
            model=self,
            states=['IDLE', 'SLEEP'],
            transitions=[
                {'trigger': 'sleep', 'source': 'IDLE', 'dest': 'SLEEP'},
                {'trigger': 'wake', 'source': 'SLEEP', 'dest': 'IDLE'},
            ],
            initial='IDLE',
            auto_transitions=False,
        )

    def update(self):
        if self.state == 'IDLE':
            self.frame = (self.frame + 1) % 8

    def draw(self):
        angle = self.face_dir * pi / 2 if self.state == 'SLEEP' else 0
        bottom = 300 if self.face_dir == 1 else 200
        self.image.clip_composite_draw(
            self.frame * 100, bottom, 100, 100, angle, '', self.x, self.y, 100, 100
        )