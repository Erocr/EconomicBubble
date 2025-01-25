import sys
import pygame as pg


class Music:
    def __init__(self):
        pg.mixer.init()
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

    def play(self, music):
        pg.mixer.music.load(sys.path[0] + "/music/" + music)

    def sound(self, sound):
        self.sounds[sound].play()



