import pygame as pg


class SplashScreen:
    def __init__(self, screenSize):
        self.bg = pg.Surface(screenSize.get)

    def draw(self, view):
        view.screen.blit(self.bg, (0, 0))

    def update(self, inputs):
        if len(inputs.events) > 0:
            return True
        return False
