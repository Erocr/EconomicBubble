from vec import *
from inputs import Inputs


class Bubble:
    """
    radius : float
    center : Vec
    fill_level : float between 0 and 1
    anim_timer : int ables the animation, like a frameCount
    anim_timer : int ab
    es the animation for the click, like a frameCount
    text : The text showed in the center of the circle
    color1 : color of the top part
    color2 : color of the bottom part
    """

    def __init__(self, radius: float, center: Vec, fill_level: float, text: str,
                 color1=(0, 255, 0), color2=(255, 0, 0)):
        self.radius = radius
        self.center = center
        self.fill_level = fill_level
        self.color1 = color1
        self.color2 = color2
        self.click_timer = 0
        self.anim_timer = 0
        self.text = text

    def update(self, inputs):
        self.anim_timer = (self.anim_timer + 1/3) % 10000
        if self.click_timer > 0:
            self.click_timer += 1
            if self.click_timer > 50:
                self.click_timer = 0
        if inputs.pressed("mouse_left") and dist(inputs.mouse_pos, self.center) < self.radius:
            self.click_timer = 1

    def draw(self, view):
        view.bubble(self)

    def clicked(self):
        return self.click_timer == 1

    def set_text(self, text):
        self.text = text

    def set_fill_level(self, fill_level):
        fill_level = min(1, max(0, fill_level))
        self.fill_level = fill_level
