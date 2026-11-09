from pico2d import *
import logoMode

open_canvas()
logoMode.init()
# game loop
while logoMode.running:
    logoMode.handle_events()
    logoMode.update()
    logoMode.render()
    delay(0.01)
# finalization code
logoMode.finish()
close_canvas()