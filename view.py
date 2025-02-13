import pygame as pg
from vec import *
from math import cos, sin, pi, floor, ceil


class View:
    def __init__(self):
        pg.font.init()
        self.screenSize = Vec(1100, 700)
        self.screen = pg.display.set_mode(self.screenSize.get, pg.NOFRAME)
        self.screenSize = Vec(*self.screen.get_size())
        self.font = pg.font.Font("fonts/FuzzyBubbles-Regular.ttf", 19)
        self.mini_font = pg.font.Font("fonts/Oswald-Medium.ttf", 12)
        #self.background = self.import_background()
        self.background = pg.image.load("images/Game_Jam_Desk_Classy.jpg")

    def import_background(self):
        background = pg.image.load("images/Game_Jam_Desk_new_york_cropped.jpg")
        scale_x = self.screenSize.x / background.get_width()
        scale_y = self.screenSize.y / background.get_height()
        background = pg.transform.scale_by(background, max(scale_y, scale_x))
        real_background = pg.Surface(self.screenSize.get)
        p = - Vec(*background.get_size())/2 + self.screenSize/2
        real_background.blit(background, p.get)
        return real_background

    def flip(self):
        pg.display.flip()
        # self.screen.fill((165, 245, 240))
        self.screen.blit(self.background, (0, 0))

    def circle(self, center: Vec, radius, color=(255, 255, 255), surf=None, filled=False):
        if surf is None:
            surf = self.screen
        width = 5
        if filled:
            width = 0
        pg.draw.circle(surf, color, center.get, radius, width=width)

    def rect(self, pos, size, color=(255, 255, 255), width=0):
        pg.draw.rect(self.screen, color, pg.Rect(*pos.get, *size.get), width=width)

    def text_font(self, msg, pos, font, color=(0, 0, 0)):
        im = font.render(msg, False, color)
        self.screen.blit(im, pos.get)

    def text_ul(self, msg, pos, color=(0, 0, 0)):
        im = self.font.render(msg, False, color)
        self.screen.blit(im, pos.get)

    def renders(self, msg, width, color):
        res = []
        for line in msg.split("\n"):
            res += self.render_line(line, width, color)
        return res

    def render_line(self, msg, width, color=(255, 255, 255)):
        messages = msg.split(" ")
        images = []
        line = " " + messages[0]
        for i in range(1, len(messages)):
            count = self.font.size(line + " " + messages[i])[0]
            if count > width:
                images.append(self.font.render(line[1:], True, color))
                line = ""
            line += " " + messages[i]

        images.append(self.font.render(line[1:], True, color))
        return images

    def text(self, msg, pos, width, color=(255, 255, 255)):
        """
        If text doesn't fit, choose it different
        """
        images = self.renders(msg, width, color)

        for im in images:
            self.screen.blit(im, (pos-Vec(im.get_width()/2, 0)).get)
            pos += Vec(0, im.get_height())

    def text_centered(self, msg, pos, width, color=(255, 255, 255)):
        images = self.renders(msg, width, color)
        mid_y = sum([image.get_height() for image in images]) / 2
        pos += Vec(0, -mid_y)
        for im in images:
            self.screen.blit(im, (pos-Vec(im.get_width()/2, 0)).get)
            pos += Vec(0, im.get_height())

    def semi_up(self, radius, height, col) -> pg.Surface:
        semi_up = pg.Surface((radius * 2, height))
        self.circle(Vec(radius, radius), radius, col, semi_up, filled=True)
        semi_up.set_colorkey((0, 0, 0))
        return semi_up

    def semi_down(self, radius, height, color):
        semi_down = pg.Surface((radius * 2, height))
        self.circle(Vec(radius, -radius + height),
                    radius, color, semi_down, filled=True)
        semi_down.set_colorkey((0, 0, 0))
        return semi_down

    def miniNotOut(self, mini_pos: Vec, mini_rad, big_pos: Vec, big_rad, color: tuple):
        res = pg.Surface((mini_rad * 2, mini_rad * 2))
        pg.draw.circle(res, color, (mini_rad, mini_rad), mini_rad)
        res.set_colorkey((0, 0, 0))
        for y in range(res.get_height()):
            for x in range(res.get_width()):
                if dist(mini_pos - Vec(mini_rad, mini_rad) + Vec(x, y), big_pos) > big_rad:
                    res.set_at((x, y), (0, 0, 0, 0))
        return res

    def miniCircles(self, bubble, radius, nb_circles: int):
        h = radius - radius * bubble.fill_level * 2
        x = sqrt(radius ** 2 - h ** 2)
        d = x * 2
        mini_rad = d / nb_circles / 2
        if mini_rad == 0:
            return
        start = bubble.center + \
            Vec(-x, h) + (RIGHT * bubble.anim_timer / 1) % (mini_rad * 2)
        flag = (bubble.anim_timer / 1) % (mini_rad * 4) > mini_rad * 2
        for i in range(-1, nb_circles+1):
            # Small variation of the height of the waves
            mini_pos = start + RIGHT * mini_rad * (2 * i)
            col = [bubble.color1, bubble.color2][flag]
            if not (i <= 0 or i >= nb_circles-1):
                self.circle(mini_pos, mini_rad, col, filled=True)
            else:
                surf = self.miniNotOut(
                    mini_pos, mini_rad, bubble.center, radius, col)
                self.screen.blit(
                    surf, (mini_pos - Vec(mini_rad, mini_rad)).get)
            flag = not flag

    def bubble(self, bubble):
        # cos(...) is for the animation
        radius = bubble.radius + 0.1 * bubble.radius * \
            sin(bubble.click_timer ** 2 / (50 * pi))

        semi_up = self.semi_up(radius, radius * 2 *
                               (1 - bubble.fill_level), bubble.color1)
        semi_down = self.semi_down(
            radius, radius * 2 * bubble.fill_level, bubble.color2)

        self.screen.blit(semi_up, (bubble.center - Vec(radius, radius)).get)
        self.screen.blit(semi_down, (bubble.center + Vec(-radius,
                         radius - bubble.fill_level * radius * 2)).get)

        self.miniCircles(bubble, radius, 13)
        #outter circles
        self.circle(bubble.center, radius+5, bubble.color_border)

        # UP * bubble.radius * 0.9 to keep the text inside vertically
        # bubble.radius * 0.75 to keep the text inside horizontally the circle
        self.text_centered(bubble.text, bubble.center, bubble.radius * 0.75)

    def single_curve(self, pos: Vec, size: Vec, curve, color=(255, 255, 255)):
        pg.draw.rect(self.screen, (0, 0, 0), pg.Rect(*pos.get, *size.get))
        max_y = curve[0]
        min_y = curve[0]
        for y in curve:
            if y > max_y:
                max_y = y
            if y < min_y:
                min_y = y

        center = (max_y + min_y) / 2
        var_y = size.y / (max_y - min_y) * 0.9
        var_x = size.x / len(curve)
        self.curve(curve, var_x, var_y, pos, size, center, color)
        pg.draw.rect(self.screen, (0, 0, 0), pg.Rect(*pos.get, *size.get), width=2)

    def multiple_curves(self, pos: Vec, size: Vec, curves, colors=None):
        if (any([len(curve) < 2 for curve in curves])):
            return

        pg.draw.rect(self.screen, (0, 0, 0), pg.Rect(*pos.get, *size.get))
        if colors is None:
            colors = [(255, 255, 255)] * len(curves)
        max_y = -1000000
        min_y = 1000000
        for curve in curves:
            for y in curve:
                if y > max_y:
                    max_y = y
                if y < min_y:
                    min_y = y
        if (max_y == min_y):
            var_y = 0
        else:
            var_y = size.y / (max_y - min_y) * 0.9

        center = (max_y + min_y) / 2
        for i in range(len(curves)):
            var_x = size.x / len(curves[i])
            self.curve(curves[i], var_x, var_y, pos, size, center, colors[i])
        pg.draw.rect(self.screen, (255, 255, 255), pg.Rect(*pos.get, *size.get), width=2)
        self.axis(pos, size, var_y, center, min_y, max_y)

    def curve(self, curve, var_x, var_y, pos, size, center, color=(255, 255, 255)):
        positions = []
        for i in range(1, len(curve)+1):
            positions.append((pos + RIGHT * (var_x * i - 5) + DOWN *
                             var_y * (center - curve[i-1]) + DOWN * size.y/2).get)

        pg.draw.lines(self.screen, color, False, positions, width=2)

    def relative_pos_y(self, var_y, y, center, size):
        return DOWN * var_y * (center - y) + DOWN * size.y / 2

    def round(self, nb, error, up=False):
        if up:
            return ceil(nb/error) * error
        else:
            return floor(nb/error) * error

    def axis(self, pos, size, var_y, center, min_y, max_y):
        possible_values = (0.1, 0.5, 1, 5, 10, 25, 20, 100, 200)
        value = 500
        for v in possible_values:
            if v * 20 > max_y - min_y:
                value = v
                break
        y = round(self.round(min_y, value, True), 1)
        while y < max_y:
            p1 = (pos.x, pos.y + self.relative_pos_y(var_y, y, center, size).y)
            p2 = (pos.x + 10, p1[1])
            pg.draw.line(self.screen, (255, 255, 255), p1, p2)
            text = self.mini_font.render(str(y), True, (255, 255, 255))
            self.screen.blit(text, (Vec(*p2) + RIGHT*10 +
                             UP * text.get_height()/2).get)
            y += value
            y = round(y, 1)
