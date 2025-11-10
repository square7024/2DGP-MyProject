from pico2d import *

idle_sprite = [
    (0, 65), (68, 132), (133, 200), (204, 271), (270, 336),
    (336, 402), (404, 472), (473, 540), (540, 608), (607, 673),
    (680, 748), (748, 814), (814, 882)
]

running = True

def handle_events():
    global running

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False

open_canvas()

character = load_image('knight_spritesheet.png')

frame = 0
while True:
    clear_canvas()
    character.clip_draw(idle_sprite[frame][0], 2275, idle_sprite[frame][1] - idle_sprite[frame][0], 85, 400, 90, 200, 200)
    update_canvas()

    handle_events()
    if not running:
        break

    frame = (frame + 1) % 13
    delay(0.1)

close_canvas()