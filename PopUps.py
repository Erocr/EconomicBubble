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
