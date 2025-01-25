from bubble import *


class Game:
    def __init__(self):
        self.bubble = Bubble(100, Vec(100, 100), 0.3, "salurtttt est ce que ca va ")

    def update(self, inputs):
        self.bubble.update(inputs)

    def draw(self, view):
        self.bubble.draw(view)