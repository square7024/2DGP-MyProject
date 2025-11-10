from pico2d import *

from forest import Forest
from knight import Knight

def reset_world():
    global running
    global world

    running = True
    world = []

    forest = Forest()
    world.append(forest)

    knight = Knight()
    world.append(knight)


def update_world():
    for o in world:
        o.update()


def render_world():
    clear_canvas()
    for o in world:
        o.draw()
    update_canvas()

def handle_events():
    global running

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                running = False


open_canvas(1280, 1024)

reset_world()

while running:
    handle_events()
    update_world()
    render_world()
    delay(0.01)

close_canvas()