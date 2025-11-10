from pico2d import *

idle_sprite = [
    (0, 65), (68, 132), (133, 200), (204, 271), (270, 336),
    (336, 402), (404, 472), (473, 540), (540, 608), (607, 673),
    (680, 748), (748, 814), (814, 882)
]

running = True

def handle_events():
    global running
    global x, dir

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_RIGHT:
                dir += 1
            elif event.key == SDLK_LEFT:
                dir -= 1
            elif event.key == SDLK_ESCAPE:
                running = False
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_RIGHT:
                dir -= 1
            elif event.key == SDLK_LEFT:
                dir += 1


open_canvas(1280, 1024)

character = load_image('knight_spritesheet.png')

x = 800 // 2
frame = 0
dir = 0

while True:
    clear_canvas()
    character.clip_draw(idle_sprite[frame][0], 2275, idle_sprite[frame][1] - idle_sprite[frame][0], 85, x, 90, 200, 200)
    update_canvas()
    handle_events()
    if not running:
        break
    frame = (frame + 1) % 13
    x += dir * 5
    delay(0.01)

close_canvas()