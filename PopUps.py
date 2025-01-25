from vec import *
import pygame as pg


class FlashInfo:
    def __init__(self, screenSize):
        self.color1 = (255, 0, 0)
        self.color2 = (0, 0, 0)
        self.text = ""
        self.scrolling = 0
        self.screenSize = screenSize
        self.font = pg.font.SysFont("serif", 36)
        self.flash_info_size = Vec(*self.font.size("FLASH INFO"))

    def update(self, inputs):
        if self.scrolling > 0:
            self.scrolling += 5
            if self.scrolling > 2 * self.screenSize.x:
                self.scrolling = 0
                self.text = ""

    def draw(self, view):
        if self.scrolling > 0:
            font_height = self.flash_info_size.y
            scrolling = min(self.scrolling, self.screenSize.x - self.flash_info_size.x - 30)
            view.rect(Vec(0, self.screenSize.y - font_height * 2),
                      Vec(self.screenSize.x, font_height * 2),
                      self.color1)
            view.rect(Vec(0, self.screenSize.y - font_height * 2),
                      self.flash_info_size * Vec(1, 2) + Vec(30, 0),
                      self.color2)
            view.text_font("FLASH INFO", Vec(10, self.screenSize.y - font_height * 1.5), self.font, self.color1)
            view.text_font(self.text, self.screenSize + Vec(-scrolling, -font_height * 1.5), self.font, self.color2)

    def new_msg(self, text):
        self.text = text
        self.scrolling = 1


class PopupsContainer:
    def __init__(self):
        self.popups = []

    def draw(self, view):
        for i in range(len(self.popups)):
            self.popups[i].draw(view, i)

    def update(self, inputs):
        for popup in self.popups:
            popup.update(inputs)

    def add_popup(self, text, type):
        """
        type can be "investment", "
        """
        pass
    # TODO

class Popup:
    size = Vec(100, 70)

    def __init__(self, text, color):
        self.text = text
        self.color = color

    def draw(self, view, i):
        pos = view.screenSize - self.size + UP * self.size.y * i
        view.rect(pos, self.size)
        view.text(self.text, pos + self.size/2, self.size.x)

