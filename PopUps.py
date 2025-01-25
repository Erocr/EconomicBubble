from vec import *
import pygame as pg

FLASH_INFO = 0
POPUP = 1


class FlashInfo:
    def __init__(self, screenSize):
        self.color1 = (255, 0, 0)
        self.color2 = (0, 0, 0)
        self.text = ""
        self.scrolling = 0
        self.screenSize = screenSize
        self.font = pg.font.SysFont("serif", 36)
        self.flash_info_size = Vec(*self.font.size("BREAKING NEWS"))

    def update(self, inputs):
        if self.scrolling > 0:
            self.scrolling += 5
            
            if self.scrolling > self.screenSize.x + self.font.size(self.text)[0] - self.font.size("BREAKING NEWS")[0]:
                self.scrolling = 0
                self.text = ""

    def draw(self, view):
        if self.scrolling > 0:
            font_height = self.flash_info_size.y
            scrolling = self.scrolling
            # scrolling = min(self.scrolling, self.screenSize.x - self.flash_info_size.x - 30)
            view.rect(Vec(0, self.screenSize.y - font_height * 2),
                      Vec(self.screenSize.x, font_height * 2),
                      self.color1)
            view.rect(Vec(0, self.screenSize.y - font_height * 2),
                      self.flash_info_size * Vec(1, 2) + Vec(30, 0),
                      self.color2)
            view.text_font(self.text, self.screenSize + Vec(-scrolling, -font_height * 1.5), self.font, self.color2)
            view.text_font("BREAKING NEWS", Vec(10, self.screenSize.y - font_height * 1.5), self.font, self.color1)

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
        nb_to_delete = 0
        for popup in self.popups:
            if popup.update(inputs):
                nb_to_delete += 1
        for _ in range(nb_to_delete):
            self.popups.pop(0)

    def add_popup(self, text, color=(0, 255, 0)):
        self.popups.append(Popup(text, color))

    def on_notify(self, values):
        if values[0] == POPUP:
            self.add_popup(values[1])


class Popup:
    size = Vec(300, 70)

    def __init__(self, text, color):
        self.text = text
        self.color = color
        self.counter = 0

    def draw(self, view, i):
        pos = view.screenSize - self.size + UP * self.size.y * i
        view.rect(pos, self.size, color=(200, 255, 255))
        view.rect(pos, self.size, color=(0, 0, 0), width=3)
        view.text(self.text, pos + Vec(self.size.x/2, 0), self.size.x*0.8, self.color)

    def update(self, inputs):
        self.counter += 1
        return self.counter > 1000

