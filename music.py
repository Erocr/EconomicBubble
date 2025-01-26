import sys
import pygame as pg
from observer import *


class Music:
    def __init__(self):
        self.activated = True
        self.playing_normal = True
        self.play_normal = False
        self.play_critical = False
        pg.mixer.init()
        self.music_channel = pg.mixer.find_channel()
        pg.mixer.music.load(sys.path[0] + "/music/pleasant-dream.wav")
        pg.mixer.music.play(-1)
        self.sounds = {
            "cash_chaching": pg.mixer.Sound(sys.path[0] + "/music/ui-sounds/cash_chaching.mp3"),
            "cash_counter": pg.mixer.Sound(sys.path[0] + "/music/ui-sounds/cash_counter.mp3"),
            "crime_ching": pg.mixer.Sound(sys.path[0] + "/music/ui-sounds/crime_ching.mp3"),
            "good_or_bad": pg.mixer.Sound(sys.path[0] + "/music/ui-sounds/good_or_bad.mp3"),
            "menu_click": pg.mixer.Sound(sys.path[0] + "/music/ui-sounds/menu_click.mp3"),
            "news_popup": pg.mixer.Sound(sys.path[0] + "/music/ui-sounds/news_popup.mp3")
        }
        self.musics = {
            "normal": pg.mixer.Sound(sys.path[0] + "/music/pleasant-dream.wav"),
            "critical": pg.mixer.Sound(sys.path[0] + "/music/the-burst.wav")
        }

    def play(self, music):
        self.music_channel.play(self.musics[music], loops=-1)

    def hardstop(self):
        pg.mixer.music.stop()

    def sound(self, sound):
        if self.activated:
            self.sounds[sound].play()

    def pause(self):
        pg.mixer.music.pause()
        self.music_channel.pause()
        self.activated = False

    def unpause(self):
        pg.mixer.music.unpause()
        self.music_channel.unpause()
        self.activated = True

    def notify(self, event, notifications):
        if event == EVENT_SOUND:
            self.sound(notifications[0])
        elif event == EVENT_PLAY_NORMAL:
            self.play_normal = True
        elif event == EVENT_PLAY_CRITICAL:
            self.play_critical = True

    def update(self, inputs):
        if inputs.pressed("mouse_left"):
            self.sound("menu_click")
        if self.play_normal and (not self.play_critical) and (not self.playing_normal):
            self.hardstop()
            self.play('normal')
            self.playing_normal = True
        elif self.play_critical and self.playing_normal:
            self.hardstop()
            self.play("critical")
            self.playing_normal = False
        self.play_normal = self.play_critical = False



