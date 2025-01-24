from vec import *
from inputs import Inputs


class Bubble:
    """
    radius : float
    center : Vec
    fill_level : float between 0 and 1
    anim_timer : int ables the animation, like a frameCount
    anim_timer : int ables the animation for the click, like a frameCount
    text : The text showed in the center of the circle
    color1 : color of the top part
    color2 : color of the bottom part
    """

    def __init__(self, radius: float, center: Vec, fill_level: float, text: str):
        self.radius = radius
        self.center = center
        self.fill_level = fill_level
        self.color1 = (0, 255, 0)
        self.color2 = (255, 0, 0)
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
            self.fill_level += 0.1

    def draw(self, view):
        view.bubble(self)
