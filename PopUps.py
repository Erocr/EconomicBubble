from vec import *
import pygame as pg
from observer import *
import sys


class FlashInfo:
    def __init__(self, screenSize):
        self.color1 = (255, 0, 0)
        self.color2 = (0, 0, 0)
        self.text = ""
        self.scrolling = 0
        self.screenSize = screenSize
        self.font = pg.font.Font(sys.path[0] + "/fonts/Oswald-Medium.ttf", 25)
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

    def notify(self, event, notifications):
        """ notifications doit etre de la forme (msg,) """
        if event == EVENT_FLASH_INFO:
            self.new_msg(notifications[0])


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

    def notify(self, event, notifications):
        """ notifications doit etre de la forme (texts, color) """
        if event == EVENT_NEW_POPUP:
            if len(notifications) == 1:
                self.add_popup(notifications[0], (0, 0, 0))
            else:
                self.add_popup(notifications[0], notifications[1])


class Popup:
    size = Vec(300, 70)

    def __init__(self, texts, color):
        self.texts = texts
        self.color = color
        self.counter = 0

    def draw(self, view, i):
        pos = view.screenSize - self.size + UP * (self.size.y + 10) * i
        view.rect(pos, self.size, color=(200, 255, 255))
        view.rect(pos, self.size, color=(0, 0, 0), width=3)

        if len(self.texts) > 0:
            text_pos_y = (self.size.y - (view.font.size(self.texts[0])[1] + 2) * (len(self.texts))) / 2
            for text in self.texts:
                view.text(text, pos + Vec(self.size.x/2, text_pos_y), self.size.x, self.color)
                text_pos_y += (view.font.size(self.texts[0])[1] + 2)

    def update(self, inputs):
        self.counter += 1
        return self.counter > 100

