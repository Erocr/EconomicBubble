from math import sqrt


class Vec:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vec(self.x+other.x, self.y+other.y)

    def __sub__(self, other):
        return Vec(self.x-other.x, self.y-other.y)

    def __mul__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return Vec(self.x*other, self.y*other)
        elif isinstance(other, Vec):
            return Vec(self.x * other.x, self.y * other.y)
        else: assert True

    def __truediv__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return Vec(self.x/other, self.y/other)
        elif isinstance(other, Vec):
            return Vec(self.x / other.x, self.y / other.y)
        else:
            assert True

    def __floordiv__(self, other):
        if isinstance(other, int):
            return Vec(int(self.x//other), int(self.y//other))
        elif isinstance(other, Vec):
            return Vec(self.x // other.x, self.y // other.y)
        else:
            assert True

    def __neg__(self):
        return Vec(-self.x, -self.y)

    def __pos__(self):
        return Vec(*self.get)

    def __str__(self):
        return f"vec({self.x}, {self.y})"

    @property
    def get(self):
        return self.x, self.y

    @property
    def size(self):
        return sqrt(self.x**2 + self.y**2)

    def normalise(self):
        return self / self.size

    def negx(self):
        """ Coordonnée x opposée """
        return Vec(-self.x, self.y)

    def negy(self):
        """ Coordonnée y opposée """
        return Vec(self.x, -self.y)


def dist(v1, v2):
    return sqrt((v1.x-v2.x)**2+(v1.y-v2.y)**2)


def min_idx(liste):
    res = None
    for i in range(len(liste)):
        if res is None or liste[i] < liste[res]:
            res = i
    return res


UP = Vec(0, -1)
DOWN = Vec(0, 1)
RIGHT = Vec(1, 0)
LEFT = Vec(-1, 0)
