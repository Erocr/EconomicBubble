import pygame as pg
import sys
from vec import *


class Settings:
    def __init__(self):
        self.activated = False
        self.music_activated = True
        self.setting_image = self.music_on = self.music_off = self.quit_image = None
        self.import_images()

    def import_images(self):
        self.setting_image = pg.image.load("images/settings_icon.png")
        self.setting_image = pg.transform.scale(self.setting_image, (50, 50))
        self.music_on = pg.image.load("images/music_off.png")
        self.music_on = pg.transform.scale(self.music_on, (50, 50))
        self.music_off = pg.image.load("images/music_on.png")
        self.music_off = pg.transform.scale(self.music_off, (50, 50))
        self.quit_image = pg.image.load("images/quit_icon.png")
        self.quit_image = pg.transform.scale(self.quit_image, (50, 50))

    def update(self, inputs, music):
        """ return if it changes the activated """
        if (inputs.pressed("mouse_left") and
                dist(Vec(*self.setting_image.get_size())/2, inputs.mouse_pos) < self.setting_image.get_width()/2):
            self.activated = not self.activated
            return True
        music_pos = Vec(*self.setting_image.get_size()) * Vec(1, 0) + Vec(*self.music_on.get_size()) / 2
        if (self.activated and inputs.pressed("mouse_left") and
                dist(music_pos, inputs.mouse_pos) < self.music_on.get_width()/2):
            self.music_activated = not self.music_activated
            if self.music_activated:
                music.unpause()
            else:
                music.pause()
        quit_pos = music_pos + Vec(self.quit_image.get_width(), 0)
        if (self.activated and inputs.pressed("mouse_left") and
                dist(quit_pos, inputs.mouse_pos) < self.music_on.get_width() / 2):
            inputs.quit = True
        return False

    def draw(self, view):
        view.screen.blit(self.setting_image, (0, 0))
        if self.activated:
            if self.music_activated:
                view.screen.blit(self.music_on, (self.setting_image.get_width(), 0))
            else:
                view.screen.blit(self.music_off, (self.setting_image.get_width(), 0))
            view.screen.blit(self.quit_image, (self.setting_image.get_width()+self.music_off.get_width(), 0))
            view.text_ul("GAME PAUSED", DOWN * self.setting_image.get_height(), 10000)
            view.text_ul("Hover for explanations", DOWN * (self.setting_image.get_height()+view.font.size(" ")[1]), 10000)

