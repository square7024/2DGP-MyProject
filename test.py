from pico2d import *

open_canvas()

character = load_image('knight_spritesheet.png')

frame = 0
for x in range(0, 800, 10):
    clear_canvas()
    character.clip_draw(frame * 66, 2360 - 85, 65, 85, x + 50, 90)
    update_canvas()
    frame = (frame + 1) % 13
    delay(0.05)

close_canvas()