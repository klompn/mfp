
class MonotonicQueue:
    def __init__(self, window, less):
        self.window = window
        self.less = less
        self.queue = []

    def push(self, item: (int, int)):
        (t, p) = item
        while len(self.queue) > 0:
            (t1, p1) = self.queue[0]
            if t - t1 > self.window:
                self.queue = self.queue[1:]
            else:
                break
        while len(self.queue) > 0:
            (t1, p1) = self.queue[-1]
            if self.less(p, p1):
                self.queue.pop()
            else:
                break
        self.queue.append(item)
        if len(self.queue) == 0:
            return 0
        else:
            (t, p) = self.queue[0]
            return p
