from pico2d import load_image

idle_sprite = [
    (0, 65), (68, 132), (133, 200), (204, 271), (270, 336),
    (336, 402), (404, 472), (473, 540), (540, 608), (607, 673),
    (680, 748), (748, 814), (814, 882)
]


class Knight:
    image = None

    def __init__(self):
        self.x, self.y = 400, 300
        self.frame = 0
        if self.image == None:
            self.image = load_image('knight_spritesheet.png')

    def update(self):
        self.frame = (self.frame + 1) % 13
        self.x += 2

    def draw(self):
        self.image.clip_draw(idle_sprite[self.frame][0], 2275, idle_sprite[self.frame][1] - idle_sprite[self.frame][0], 85, self.x, self.y, 200, 200)
