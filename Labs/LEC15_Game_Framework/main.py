from pico2d import *
import playMode

open_canvas()
playMode.init()
# game loop
while playMode.running:
    playMode.handle_events()
    playMode.update()
    playMode.render()
    delay(0.01)
# finalization code
playMode.finish()
close_canvas()