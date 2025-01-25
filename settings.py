import pygame as pg
import sys
from vec import *


class Settings:
    def __init__(self):
        self.activated = False
        self.setting_image = pg.image.load(sys.path[0] + "/images/settings_icon.png")

    def update(self, inputs):
        if (inputs.pressed("mouse_left") and
                dist(Vec(*self.setting_image.get_size()), inputs.mouse_pos) < self.setting_image.get_width()/2):
            self.activated = not self.activated

    def draw(self, view):
        view.screen.blit(self.setting_image, (0, 0))
