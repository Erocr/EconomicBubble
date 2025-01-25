import random

def clamp(val, min_, max_):
    return min(max(val, min_), max_)

class Queue(list):
    def __init__(self, max_size):
        self.max_size = max_size
        self.append(1)    
        for _ in range(max_size - 1):
            self.append(clamp(self[-1] + random.random()/4_000 + random.gauss(0, 50)/2_000,
                              random.randint(3, 12)/100, random.randint(163, 194)/100))
    
    def push(self, value):
        self.append(value)
        if (len(self) > self.max_size):
            self.pop(0)


def to_readable_int(x):
    if x < 1_000:
        return f"{x:.2f}"
    elif (1_000 <= x < 1_000_000):
        return f"{x / 1_000:.2f}K"
    elif(1_000_000 <= x < 1_000_000_000):
        return f"{x / 1_000_000:.2f}M"
    else:
        return f"{x / 1_000_000_000:.2f}B"

