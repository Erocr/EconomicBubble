from vec import Vec
from inputs import Inputs


class Bubble:
    """
    radius : float
    center : Vec
    fill_level : float between 0 and 1
    timer : int ables the animation, like a frameCount
    """

    def __init__(self, radius: float, center: Vec, fill_level: float):
        self.radius = radius
        self.center = center
        self.fill_level = fill_level
        self.timer = 0
