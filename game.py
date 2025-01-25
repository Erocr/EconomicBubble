from bubble import *


class Game:
    def __init__(self):
        self.bubbles = [
            Bubble(100, Vec(100, 100), 0.3, "Marketing", (0, 0, 255), (0, 255, 255)),
            Bubble(100, Vec(100, 350), 0.6, "Espionage", (50, 0, 0), (100, 0, 0)),
            Bubble(100, Vec(350, 225), 0.8, "Security", (255, 0, 0), (255, 100, 100)),
        ]

    def update(self, inputs):
        for bubble in self.bubbles:
            bubble.update(inputs)

    def draw(self, view):
        for bubble in self.bubbles:
            bubble.draw(view)
