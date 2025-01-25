from vec import *
from misc import Queue

class Curve:
    def __init__(self, pos: Vec, size: Vec):
        self.pos = pos
        self.size = size
        self.values = []
        self.nb_values_max = 100

    def add_value(self, value):
        self.values.append(value)
        if len(self.values) > self.nb_values_max:
            self.values.pop(0)

    def draw(self, view):
        view.single_curve(self.pos, self.size, self.values)

    def update(self, inputs):
        pass


class MultiCurve:
    def __init__(self, pos, size, nb_curves, colors=None):
        self.pos = pos
        self.size = size
        self.values = [Queue(60) for _ in range(nb_curves)]
        self.colors = colors
        if colors is None:
            self.colors = [(255, 255, 255) for _ in range(nb_curves)]
        assert len(self.colors) == len(self.values) == nb_curves

    def add_values(self, values):
        """ add one value to each curves """
        for our_vals, v in zip(self.values, values):
            our_vals.push(v)

    def draw(self, view):
        view.multiple_curves(self.pos, self.size, self.values, self.colors)
