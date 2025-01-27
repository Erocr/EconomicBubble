from vec import *
import pygame as pg
import sys
from observer import *


class Card:
    image = pg.image.load("images/clear_grey.png")

    def __init__(self, narration, index, view):
        self.narration = narration
        self.size = Vec(300, 500)
        self.pos = view.screenSize/2+Vec(-self.size.x*(1-index), -self.size.y/2)
        self.pos += Vec(10, 0) * (index * 2 - 1)

    def draw(self, view):
        # bg and narration
        view.screen.blit(self.image, self.pos.get)
        view.rect(self.pos-Vec(2, 2), self.size+Vec(4, 4), (0, 0, 0), width=2)
        view.text(self.narration, self.pos + self.size / Vec(2, 4), self.size.x, (0, 0, 0))

    def update(self, inputs):
        return inputs.pressed("mouse_left") and \
            self.pos.x < inputs.mouse_pos.x < self.pos.x + self.size.x and \
            self.pos.y < inputs.mouse_pos.y < self.pos.y + self.size.y


class CardsPair:
    def __init__(self, view):
        self.card1 = None
        self.card2 = None
        self.view = view

    def set_cards(self, action1, action2):
        self.card1 = Card(action1, 0, self.view)
        self.card2 = Card(action2, 1, self.view)

    def draw(self):
        if self.card1 is not None:
            self.card1.draw(self.view)
        if self.card2 is not None:
            self.card2.draw(self.view)

    def update(self, inputs):
        if not self.actif(): return None
        a = self.card1.update(inputs)
        b = self.card2.update(inputs)
        if a or b:
            res = [self.card1.narration, self.card2.narration]
            self.card1 = self.card2 = None
            return res[b]

    def notify(self, event, notifications):
        if event == EVENT_TRIGGER_CHOICES:
            self.set_cards(*notifications)

    def actif(self):
        return self.card1 is not None


