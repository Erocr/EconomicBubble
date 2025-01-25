import pygame as pg
from vec import *
from math import cos, sin, pi


class View:
    def __init__(self):
        pg.font.init()
        self.screenSize = Vec(700, 700)
        self.screen = pg.display.set_mode(self.screenSize.get)
        self.font = pg.font.Font('freesansbold.ttf', 24)

    def flip(self):
        pg.display.flip()
        self.screen.fill((0, 0, 0))

    def circle(self, center: Vec, radius, color=(255, 255, 255), surf=None, filled=False):
        if surf is None: surf = self.screen
        width = 5
        if filled: width = 0
        pg.draw.circle(surf, color, center.get, radius, width=width)

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

    def semi_up(self, radius, height, col) -> pg.Surface:
        semi_up = pg.Surface((radius * 2, height))
        self.circle(Vec(radius, radius), radius, col, semi_up, filled=True)
        return semi_up

    def semi_down(self, radius, height, color):
        semi_down = pg.Surface((radius * 2, height))
        self.circle(Vec(radius, -radius + height), radius, color, semi_down, filled=True)
        return semi_down

    def mini_circles(self, bubble, radius, nb_circles: int):
        h = radius - radius * bubble.fill_level * 2
        x = sqrt(radius ** 2 - h ** 2)
        d = x * 2
        mini_rad = d / nb_circles / 2
        start = bubble.center + Vec(-x, h) + RIGHT
        flag = False
        for i in range(nb_circles-1):
            self.circle(start + RIGHT * mini_rad * (2 * i + 2), mini_rad, [bubble.color1, bubble.color2][flag], filled=True)
            flag = not flag

    def bubble(self, bubble):
        # cos(...) is for the animation
        radius = bubble.radius + 0.1 * bubble.radius * sin(bubble.click_timer ** 2 / (50 * pi))

        semi_up = self.semi_up(radius, radius * 2 * (1 - bubble.fill_level), bubble.color1)
        semi_down = self.semi_down(radius, radius * 2 * bubble.fill_level, bubble.color2)

        self.screen.blit(semi_up, (bubble.center - Vec(radius, radius)).get)
        self.screen.blit(semi_down, (bubble.center + Vec(-radius, radius - bubble.fill_level * radius * 2)).get)

        self.circle(bubble.center, radius, (255, 255, 255))

        self.mini_circles(bubble, radius, 20)

        # UP * bubble.radius * 0.9 to keep the text inside vertically
        # bubble.radius * 0.75 to keep the text inside horizontally the circle
        self.text(bubble.text, bubble.center + UP * bubble.radius * 0.9, bubble.radius * 0.75)

