from vec import Vec


class Bubble:
    """
    radius : float
    center : Vec
    fill_level : float between 0 and 1
    """

    def __init__(self, radius: float, center: Vec, fill_level: float):
        self.radius = radius
        self.center = center
        self.fill_level = fill_level
