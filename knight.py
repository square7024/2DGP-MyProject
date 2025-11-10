from pico2d import load_image
from sdl2 import SDL_KEYDOWN, SDLK_SPACE, SDLK_RIGHT, SDL_KEYUP, SDLK_LEFT

from state_machine import StateMachine

h = 2360

idle_sprite = [
    (0, 65), (68, 132), (133, 200), (204, 271), (270, 336),
    (336, 402), (404, 472), (473, 540), (540, 608), (607, 673),
    (680, 748), (748, 814), (814, 882)
]

run_sprite = [
    (0, 284, 81, 353), (82, 284, 154, 353), (154, 287, 225, 356), (227, 288, 296, 360), (308, 288, 386, 356),
    (386, 288, 459, 358), (458, 291, 531, 359), (531, 295, 603, 364), (608, 290, 688, 362), (688, 291, 761, 363),
    (761, 292, 834, 362), (833, 295, 908, 361), (909, 294, 976, 362), (976, 295, 1045, 362)

]

def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT

def left_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT

def right_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT

def left_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT

class Run:
    def __init__(self, knight):
        self.knight = knight

    def enter(self, e):
        if right_down(e) or left_up(e):
            self.knight.dir = self.knight.face_dir = 1
        elif left_down(e) or right_up(e):
            self.knight.dir = self.knight.face_dir = -1

    def exit(self, e):
        pass

    def do(self):
        self.knight.frame = (self.knight.frame + 1) % 13
        self.knight.x += self.knight.dir * 5

    def draw(self):
        if self.knight.face_dir == 1:
            self.knight.image.clip_draw(run_sprite[self.knight.frame][0], h - run_sprite[self.knight.frame][3],
                                        idle_sprite[self.knight.frame][1] - idle_sprite[self.knight.frame][0], run_sprite[self.knight.frame][3] - run_sprite[self.knight.frame][1],
                                        self.knight.x, self.knight.y, 200, 200)
        else:
            self.knight.image.clip_composite_draw(run_sprite[self.knight.frame][0], h - run_sprite[self.knight.frame][3],
                                        idle_sprite[self.knight.frame][1] - idle_sprite[self.knight.frame][0], run_sprite[self.knight.frame][3] - run_sprite[self.knight.frame][1],
                                                  0, 'h', self.knight.x, self.knight.y, 200, 200)

class Idle:
    def __init__(self, knight):
        self.knight = knight

    def enter(self, e):
        self.knight.dir = 0

    def exit(self, e):
        pass

    def do(self):
        self.knight.frame = (self.knight.frame + 1) % 13
        pass

    def draw(self):
        if self.knight.face_dir == 1:
            self.knight.image.clip_draw(idle_sprite[self.knight.frame][0], 2283,
                                        idle_sprite[self.knight.frame][1] - idle_sprite[self.knight.frame][0],
                                        77, self.knight.x, self.knight.y, 200, 200)
        else:
            self.knight.image.clip_composite_draw(idle_sprite[self.knight.frame][0], 2283,
                                                  idle_sprite[self.knight.frame][1] - idle_sprite[self.knight.frame][0],
                                                  77, 0, 'h', self.knight.x, self.knight.y, 200, 200)

class Knight:
    def __init__(self):
        self.x, self.y = 400, 300
        self.frame = 0
        self.face_dir = 1
        self.dir = 0
        self.image = load_image('knight_spritesheet.png')

        self.IDLE = Idle(self)
        self.RUN = Run(self)
        self.state_machine = StateMachine(
            self.IDLE,
            {
                self.IDLE : {right_down: self.RUN, right_up: self.RUN, left_down: self.RUN, left_up: self.RUN},
                self.RUN : {right_down: self.IDLE, right_up: self.IDLE, left_down: self.IDLE, left_up: self.IDLE}
            }

        )

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_state_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()
