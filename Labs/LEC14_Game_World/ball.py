from pico2d import get_canvas_width, load_image


class Ball:
    def __init__(self, x, y, direction):
        self.image = load_image('ball21x21.png')
        self.x = x + direction * 40
        self.y = y
        self.direction = direction

    def update(self):
        self.x += self.direction * 10

    def draw(self):
        self.image.draw(self.x, self.y)

    def is_out_of_canvas(self):
        return self.x < -10 or self.x > get_canvas_width() + 10
