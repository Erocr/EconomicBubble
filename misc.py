class Queue:
    def __init__(self, max_size):
        self._queue = []
        self.max_size = max_size
    
    def push(self, value):
        self._queue.append(value)
        if (len(self._queue) > self.max_size):
            self._queue.pop(0)