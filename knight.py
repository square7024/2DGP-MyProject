from pico2d import load_image, load_font, draw_rectangle
from sdl2 import SDL_KEYDOWN, SDLK_RIGHT, SDL_KEYUP, SDLK_LEFT, SDLK_a, SDLK_SPACE

import game_framework
from state_machine import StateMachine

sprite_h = 2360

idle_sprite = [
    (0, 65), (68, 132), (133, 200), (204, 271), (270, 336),
    (336, 402), (404, 472), (473, 540), (540, 606), (607, 673),
    (680, 747), (748, 814), (814, 882)
]

run_sprite = [
    (0, 284, 81, 353), (82, 284, 154, 353), (154, 287, 225, 356), (227, 288, 296, 360), (308, 288, 386, 356),
    (386, 288, 459, 358), (458, 291, 531, 359), (531, 295, 603, 364), (608, 290, 688, 362), (688, 291, 760, 363),
    (761, 292, 833, 362), (833, 295, 908, 361), (909, 294, 976, 362), (976, 295, 1045, 362)
]

jump_sprite = [
    (35, 378, 76, 462), (92, 376, 160, 451), (174, 377, 235, 453), (237, 391, 324, 448), (351, 367, 416, 448),
    (428, 371, 504, 451), (511, 377, 580, 447), (597, 370, 673, 453), (683, 383, 763, 457)
]

attack_sprite = [
    (14, 662, 84, 736), (94, 661, 151, 736), (172, 650, 289, 736), (304, 672, 363, 742), (389, 668, 441, 741)
]

def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT

def left_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT

def right_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT

def left_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT

def a_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_a

def space_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE

attack = lambda e: e[0] == 'ATTACK'

jump = lambda e: e[0] == 'JUMP'


# Knight Run Speed
PIXEL_PER_METER = (10.0 / 0.2)  # 10 pixel 20 cm
RUN_SPEED_KMPH = 20.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)
GRAVITY = 9.8

# Knight Action Speed
TIME_PER_ACTION = 1 # 액션 당 걸리는 시간
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION # 초당 액션 수
FRAMES_PER_ACTION_RUN = 14
FRAMES_PER_ACTION_IDLE = 13
FRAMES_PER_ACTION_ATTACK = 5
FRAMES_PER_ACTION_JUMP = 9

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
            self.knight.image.clip_draw(x1, sprite_h - y2, width, height, self.knight.x - 45, self.knight.y, 200, 200)
        else:
            self.knight.image.clip_composite_draw(x1, sprite_h - y2, width, height, 0, 'h', self.knight.x + 45, self.knight.y, 200, 200)

class Idle:
    def __init__(self, knight):
        self.knight = knight

    def enter(self, e):
        self.knight.dir = 0

    def exit(self, e):
        pass

    def do(self):
        self.knight.frame = (self.knight.frame + FRAMES_PER_ACTION_RUN * ACTION_PER_TIME * game_framework.frame_time) % 13

    def draw(self):
        idx = int(self.knight.frame)
        x1, x2 = idle_sprite[idx]
        width = x2 - x1

        if self.knight.face_dir == 1:
            self.knight.image.clip_draw(x1, 2283, width, 77, self.knight.x - 45, self.knight.y, 200, 200)
        else:
            self.knight.image.clip_composite_draw(x1, 2283, width, 77, 0, 'h', self.knight.x + 45, self.knight.y, 200, 200)

class Attack:
    def __init__(self, knight):
        self.knight = knight

    def enter(self, e):
        self.knight.frame = 0

    def exit(self, e):
        pass

    def do(self):
        self.knight.frame = self.knight.frame + FRAMES_PER_ACTION_ATTACK * ACTION_PER_TIME * 2 * game_framework.frame_time

        if self.knight.frame >= 5:
            self.knight.frame = 0
            self.knight.state_machine.handle_state_event(('ATTACK', None))

    def draw(self):
        idx = int(self.knight.frame)
        idx = max(0, min(idx, len(attack_sprite) - 1))
        x1, y1, x2, y2 = attack_sprite[idx]
        width = x2 - x1
        height = y2 - y1

        if self.knight.face_dir == 1:
            self.knight.image.clip_draw(x1, sprite_h - y2, width, height, self.knight.x - 45, self.knight.y, 200, 200)
        else:
            self.knight.image.clip_composite_draw(x1, sprite_h - y2, width, height, 0, 'h', self.knight.x + 45, self.knight.y, 200, 200)

class Jump:
    def __init__(self, knight):
        self.knight = knight

    def enter(self, e):
        self.knight.frame = 0
        self.knight.yv = 10

    def exit(self, e):
        pass

    def do(self):
        self.knight.frame = self.knight.frame + FRAMES_PER_ACTION_JUMP * ACTION_PER_TIME * game_framework.frame_time
        self.knight.yv -= GRAVITY * game_framework.frame_time
        self.knight.y += self.knight.yv * game_framework.frame_time * PIXEL_PER_METER
        if self.knight.y < 300:
            self.knight.y = 300
            self.knight.yv = 10
            self.knight.frame = 0
            self.knight.state_machine.handle_state_event(('JUMP', None))

    def draw(self):
        idx = int(self.knight.frame)
        idx = max(0, min(idx, len(jump_sprite) - 1))
        x1, y1, x2, y2 = jump_sprite[idx]
        width = x2 - x1
        height = y2 - y1

        if self.knight.face_dir == 1:
            self.knight.image.clip_draw(x1, sprite_h - y2, width, height, self.knight.x - 45, self.knight.y, 200, 200)
        else:
            self.knight.image.clip_composite_draw(x1, sprite_h - y2, width, height, 0, 'h', self.knight.x + 45, self.knight.y, 200, 200)


class Knight:
    def __init__(self):
        self.font = load_font('ENCR10B.TTF', 16)

        self.x, self.y = 400, 300
        self.yv = 10
        self.frame = 0
        self.face_dir = 1
        self.dir = 0
        self.image = load_image('knight_spritesheet.png')

        self.IDLE = Idle(self)
        self.RUN = Run(self)
        self.ATTACK = Attack(self)
        self.JUMP = Jump(self)
        self.state_machine = StateMachine(
            self.IDLE,
            {
                self.IDLE : {right_down: self.RUN, right_up: self.RUN, left_down: self.RUN, left_up: self.RUN, a_down: self.ATTACK, space_down: self.JUMP},
                self.RUN : {right_down: self.IDLE, right_up: self.IDLE, left_down: self.IDLE, left_up: self.IDLE, a_down: self.ATTACK, space_down: self.JUMP},
                self.ATTACK : {attack: self.IDLE},
                self.JUMP : {jump: self.IDLE}
            }

        )

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_state_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()
        # self.font.draw(self.x - 60, self.y + 50, f'{self.frame}', (255, 255, 0))
        # draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 20, self.y - 50, self.x + 20, self.y + 50
