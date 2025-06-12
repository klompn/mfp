
class SlidingWindow:
    def __init__(self, windows, max_item):
        self.windows = windows
        self.len = len(self.windows)
        self.index = [0] * self.len
        self.queue = []
        self.max_item = max_item

    def push(self, t: int):
        for i in range(self.len):
            while self.index[i] < len(self.queue) and t - self.queue[self.index[i]] > self.windows[i]:
                self.index[i] += 1
        self.queue.append(t)
        if len(self.queue) - self.index[0] + 1 > self.max_item:
            self.index[0] = len(self.queue) - self.max_item
        self.queue = self.queue[self.index[0]:]
        result = [0] * self.len
        for i in range(self.len - 1, -1, -1):
            if self.index[i] < self.index[0]:
                self.index[i] = 0
            else:
                self.index[i] -= self.index[0]
            result[i] = len(self.queue) - self.index[i]
        return result


