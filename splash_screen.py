import pygame as pg
import sys


class SplashScreen:
    def __init__(self, screenSize):
        self.bg = pg.image.load(sys.path[0] + "/images/Splash_Screen.jpg")

    def draw(self, view):
        view.screen.blit(self.bg, (0, 0))

    def update(self, inputs):
        if len(inputs.events) > 0:
            return True
        return False
