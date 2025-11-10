from pico2d import *
from forest import Forest
from knight import Knight

def handle_events():
    global running

    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        else:
            knight.handle_event(event)


def reset_world():
    global world
    global knight

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

running = True

w = 1280
h = 1024

open_canvas(w, h)
reset_world()
# game loop
while running:
    handle_events()
    update_world()
    render_world()
    delay(0.01)
# finalization code
close_canvas()
