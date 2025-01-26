import pygame as pg
import sys
from vec import *

class EndScreen():
    def __init__(self,view):
        self.import_images()
        self.screenSize = view.screenSize
        self.bg = pg.transform.scale(self.bg, (self.screenSize.get[0],self.screenSize.get[1]))
        self.play_again_bool = False
        self.quit_pos = self.screenSize / Vec(2,2) - Vec(self.screenSize.get[0]/9, 0) #- Vec(*self.play_image.get_size())
        self.play_pos = self.screenSize / Vec(2,2) + Vec(self.screenSize.get[0]/9, 0) # + Vec(*self.play_image.get_size())
        self.top_left_quit_pos = self.quit_pos - Vec(*self.quit_image.get_size()) /2
        self.top_left_play_pos = self.play_pos - Vec(*self.play_image.get_size()) /2

    def import_images(self):
        self.bg = pg.image.load(sys.path[0] + "/images/game-over.png")
        self.quit_image = pg.image.load(sys.path[0] + "/images/quit_icon.png")
        self.quit_image = pg.transform.scale(self.quit_image, (100,100))
        self.play_image = pg.image.load(sys.path[0] + "/images/play_image.png")
        self.play_image = pg.transform.scale(self.play_image, (100,100))



    def update(self, inputs):
        # left quit and right restart
        if (inputs.pressed("mouse_left") and
                dist(self.quit_pos, inputs.mouse_pos) < max(self.quit_image.get_size()) / 2):
            inputs.quit = True
        elif(inputs.pressed("mouse_left") and
                dist(self.play_pos, inputs.mouse_pos) < max(self.play_image.get_size()) / 2):
            self.play_again_bool = True
        else:
            None
    
    def draw(self, view):
        view.screen.blit(self.bg, (0,0))
        view.screen.blit(self.quit_image, self.top_left_quit_pos.get)
        view.screen.blit(self.play_image, self.top_left_play_pos.get)
        
