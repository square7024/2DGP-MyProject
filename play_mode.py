import game_framework
from pico2d import *

from forest import Forest
from knight import Knight
import game_world

def pause():
    pass

def resume():
    pass

def handle_events():

    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            knight.handle_event(event)


def init():
    global knight

    forest = Forest()
    game_world.add_object(forest, 0)

    knight = Knight()
    game_world.add_object(knight, 1)


def update():
    game_world.update()


def draw():
    clear_canvas()
    game_world.render()
    update_canvas()


def finish():
    game_world.clear()

