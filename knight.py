from pico2d import load_image
from sdl2 import SDL_KEYDOWN, SDLK_SPACE, SDLK_RIGHT, SDL_KEYUP, SDLK_LEFT

import game_framework
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

# Knight Run Speed
PIXEL_PER_METER = (10.0 / 0.2)  # 10 pixel 20 cm
RUN_SPEED_KMPH = 20.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# Knight Action Speed
TIME_PER_ACTION = 20 # 액션 당 걸리는 시간
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION # 초당 액션 수
FRAMES_PER_ACTION_RUN = 14
FRAMES_PER_ACTION_IDLE = 13

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
        self.knight.frame = (self.knight.frame + FRAMES_PER_ACTION_RUN * ACTION_PER_TIME * game_framework.frame_time) % 14
        self.knight.x += self.knight.dir * RUN_SPEED_PPS * game_framework.frame_time


    def draw(self):
        idx = int(self.knight.frame)
        x1, y1, x2, y2 = run_sprite[idx]
        width = x2 - x1
        height = y2 - y1

        if self.knight.face_dir == 1:
            self.knight.image.clip_draw(x1, h - y2, width, height, self.knight.x, self.knight.y, 200, 200)
        else:
            self.knight.image.clip_composite_draw(x1, h - y2, width, height, 0, 'h', self.knight.x, self.knight.y, 200, 200)

class Idle:
    def __init__(self, knight):
        self.knight = knight

    def enter(self, e):
        self.knight.dir = 0

    def exit(self, e):
        pass

    def do(self):
        self.knight.frame = (self.knight.frame + FRAMES_PER_ACTION_RUN * ACTION_PER_TIME * game_framework.frame_time) % 13
        pass

    def draw(self):
        if self.knight.face_dir == 1:
            self.knight.image.clip_draw(idle_sprite[int(self.knight.frame)][0], 2283,
                                        idle_sprite[int(self.knight.frame)][1] - idle_sprite[int(self.knight.frame)][0],
                                        77, self.knight.x, self.knight.y, 200, 200)
        else:
            self.knight.image.clip_composite_draw(idle_sprite[int(self.knight.frame)][0], 2283,
                                                  idle_sprite[int(self.knight.frame)][1] - idle_sprite[int(self.knight.frame)][0],
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
