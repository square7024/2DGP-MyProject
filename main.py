from pico2d import *
import game_framework
import play_mode as start_mode

width = 1280
height = 1024

open_canvas(width, height)
game_framework.run(start_mode)
close_canvas()
