from pico2d import *

from forest import Forest
from knight import Knight

def handle_events():
    global running

    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            main.running = False
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                main.running = False


def reset_world():
    global world

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
