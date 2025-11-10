from pico2d import *

idle_sprite = [
    (0, 65), (68, 132), (133, 200), (204, 271), (270, 336),
    (336, 402), (404, 472), (473, 540), (540, 608), (607, 673),
    (680, 748), (748, 814), (814, 882)
]

class Forest:
    def __init__(self):
        self.image = load_image('forest.png')

    def draw(self):
        self.image.draw(1280 / 2, 1024 / 2)

    def update(self):
        pass

class Knight:
    def __init__(self):
        self.x, self.y = 400, 300
        self.frame = 0
        self.image = load_image('knight_spritesheet.png')

    def update(self):
        self.frame = (self.frame + 1) % 13
        self.x += 2

    def draw(self):
        self.image.clip_draw(idle_sprite[self.frame][0], 2275, idle_sprite[self.frame][1] - idle_sprite[self.frame][0], 85, self.x, self.y, 200, 200)


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