from pico2d import load_image


class Forest:
    def __init__(self):
        self.image = load_image('forest.png')

    def draw(self):
        self.image.draw(1280 / 2, 1024 / 2)

    def update(self):
        pass
