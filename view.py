import pygame as pg
from vec import *


class View:
    def __init__(self):
        pg.font.init()
        self.screenSize = Vec(700, 700)
        self.screen = pg.display.set_mode(self.screenSize.get)
        self.font = pg.font.Font('freesansbold.ttf', 32)

    def flip(self):
        pg.display.flip()
        self.screen.fill((0, 0, 0))

    def circle(self, center: Vec, radius, color=(255, 255, 255)):
        pg.draw.circle(self.screen, color, center.get, radius)

    def text(self, msg, pos, width, color=(255, 255, 255)):
        """
        If text doesn't fit, choose it different
        """
        messages = msg.split(" ")
        count = 0
        images = []
        line = ""
        for i in range(0, len(messages)):
            w = self.font.size(messages[i])[0]
            count += w
            if count > width:
                images.append(self.font.render(line[1:], True, color))
                line = ""
            line += " " + messages[i]

        images.append(self.font.render(line[1:], True, color))

        for im in images:
            self.screen.blit(im, (pos-Vec(im.get_width()/2, 0)).get)
            pos += Vec(0, im.get_height())

    def bubble(self, bubble):
        self.circle(bubble.center, bubble.radius)
