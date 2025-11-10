from pico2d import *
from game import reset_world, handle_events, update_world, render_world

running = True

open_canvas(1280, 1024)
reset_world()

while running:
    handle_events()
    update_world()
    render_world()
    delay(0.01)

close_canvas()