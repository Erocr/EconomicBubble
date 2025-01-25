class Queue(list):
    def __init__(self, max_size):
        self.max_size = max_size
    
    def push(self, value):
        self.append(value)
        if (len(self) > self.max_size):
            self.pop(0)