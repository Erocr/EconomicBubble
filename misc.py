class Queue(list):
    def __init__(self, max_size):
        self.max_size = max_size
    
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

