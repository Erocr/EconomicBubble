from vec import *
import pygame as pg
import sys


class Card:
    image = pg.image.load(sys.path[0] + "/images/card_bg.png")

    def __init__(self, narration, index, view):
        self.narration = narration
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

    def update(self, inputs):
        return inputs.pressed("mouse_left") and dist(inputs.mouse_pos, self.pos) < self.b_rad


class CardsPair:
    def __init__(self):
        self.card1 = None

        self.card2 = None

    def set_cards(self, action1, action2, view):
        self.card1 = Card(action1, 0, view)
        self.card2 = Card(action2, 1, view)

    def draw(self, view):
        self.card1.draw(view)
        self.card2.draw(view)

    def update(self, inputs):
        a = self.card1.update(inputs)
        b = self.card2.update(inputs)
        if a:
            return 0
        elif b:
            return 1
        else:
            return -1


