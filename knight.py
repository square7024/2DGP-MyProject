from pico2d import load_image
from state_machine import StateMachine

idle_sprite = [
    (0, 65), (68, 132), (133, 200), (204, 271), (270, 336),
    (336, 402), (404, 472), (473, 540), (540, 608), (607, 673),
    (680, 748), (748, 814), (814, 882)
]

class IDLE:
    def __init__(self, knight):
        self.knight = knight

    def enter(self):
        pass

    def exit(self):
        pass

    def do(self):
        self.knight.frame = (self.knight.frame + 1) % 13
        pass

    def draw(self):
        if self.knight.face_dir == 1:
            self.knight.image.clip_draw(idle_sprite[self.knight.frame][0], 2275, idle_sprite[self.knight.frame][1] - idle_sprite[self.knight.frame][0], 85, self.knight.x, self.knight.y, 200, 200)
        else:
            self.knight.image.clip_composite_draw(idle_sprite[self.knight.frame][0], 2275, idle_sprite[self.knight.frame][1] - idle_sprite[self.knight.frame][0], 0, 'v',  85, self.knight.x, self.knight.y, 200, 200)

class Knight:
    image = None

    def __init__(self):
        self.x, self.y = 400, 300
        self.frame = 0
        self.face_dir = 1
        self.image = load_image('knight_spritesheet.png')

        self.IDLE = IDLE(self)
        self.state_machine = StateMachine(self.IDLE)

    def update(self):
        self.state_machine.update()

    def draw(self):
        self.state_machine.draw()
