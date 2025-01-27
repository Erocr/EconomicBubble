import pygame as pg


class SplashScreen:
    def __init__(self, screenSize):
        self.bg = pg.image.load("images/Splash_Screen.jpg")
        self.bg = pg.transform.scale(self.bg, screenSize.get)

    def draw(self, view):
        view.screen.blit(self.bg, (0, 0))

    def update(self, inputs):
        if len(inputs.events) > 0:
            return True
        return False
