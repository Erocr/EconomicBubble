import pygame as pg
from vec import *


class View:
    def __init__(self):
        self.screenSize = Vec(700, 700)
        self.screen = pg.display.set_mode(self.screenSize.get)


