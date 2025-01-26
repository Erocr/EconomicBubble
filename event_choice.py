from vec import *
import pygame as pg
import sys


class Card:
    image = pg.image.load(sys.path[0] + "/images/card_bg.png")

    def __init__(self, action, narration, index, view):
        self.action = action
        self.narration = narration
        self.is_clicked = False
        self.size = Vec(300, 500)
        self.pos = view.screenSize/2+Vec(-self.size.x*(1-index), -self.size.y/2)
        self.b_pos = self.pos+self.size/Vec(2, 4)
        self.b_rad = self.size.y / 8

    def draw(self, view):
        # bg and narration
        view.screen.blit(self.image, self.pos.get)
        view.rect(self.pos-Vec(2, 2), self.size+Vec(4, 4), (0, 0, 0), width=2)
        view.text(self.narration, self.pos + self.size / 2, self.size.x, (255, 255, 255))
        # button
        view.circle(self.b_pos, self.b_rad, (30, 30, 30), filled=True)
        view.text_centered(self.action, self.b_pos, self.b_rad, (255, 255, 255))

    def update(self, inputs):
        self.is_clicked = inputs.pressed("mouse_left") and dist(inputs.mouse_pos, self.pos) < self.b_rad
        if self.is_clicked: print("zjfojzdzk elj qijsbmajsd ijb")


