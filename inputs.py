import pygame as pg
from vec import *


class Key:
    def __init__(self, d=0):
        self.duration = d

    @property
    def holding(self):
        return self.duration >= 0

    @property
    def pressed(self):
        return self.duration == 0

    @property
    def released(self):
        return self.duration < 0


class Inputs:
    def __init__(self):
        self.keys = {}
        self._pg_events()
        self.events = {}
        self.mouse_pos = Vec(0, 0)
        self.quit = False

    def _pg_events(self):
        pg_keys = pg.__dict__
        for p in pg_keys:
            if p[:2] == "K_":
                self.keys[pg_keys[p]] = p[2:]
        self.keys["mouse_left"] = -1
        self.keys["mouse_right"] = -3

    def update(self):
        self.mouse_pos = Vec(*pg.mouse.get_pos())
        keys = list(self.events.keys())
        for evt in keys:
            if self.events[evt].duration == -1:
                self.events.pop(evt)
            else:
                self.events[evt].duration += 1

        for evt in pg.event.get():
            if evt.type == pg.KEYDOWN:
                self.events[evt.key] = Key()
            elif evt.type == pg.KEYUP:
                self.events[evt.key] = Key(-1)
            elif evt.type == pg.QUIT:
                self.quit = True
            elif evt.type == pg.MOUSEBUTTONDOWN:
                self.events[-evt.button] = Key()
            elif evt.type == pg.MOUSEBUTTONUP:
                self.events[-evt.button] = Key(-1)

    def key_id(self, key):
        if isinstance(key, int):
            return key
        elif key in self.keys:
            return self.keys[key]
        elif "K_" + key in self.keys:
            return self.keys["K_" + key]
        else:
            raise Exception(f"key {key} does not exist")

    def pressed(self, key):
        key = self.key_id(key)
        return key in self.events and self.events[key].pressed

    def holding(self, key):
        key = self.key_id(key)
        return key in self.events and self.events[key].holding

    def released(self, key):
        key = self.key_id(key)
        return key in self.events and self.events[key].released
