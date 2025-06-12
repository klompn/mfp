
class Grain:
    def __init__(self, window, max_grain):
        self.window = window
        self.queue = []
        self.grain = 0
        self.pos = {}
        self.max_grain = max_grain
        self.max_hit = False

    def push(self, item: (int, int)):
        if self.max_hit:
            return self.max_grain

        (t, p) = item
        self.queue.append(item)
        if p in self.pos:
            self.pos[p] += 1
        else:
            self.pos[p] = 1
        while len(self.queue) > 0:
            (t1, p1) = self.queue[0]
            if t - t1 > self.window or self.max_grain < len(self.pos):
                self.queue = self.queue[1:]
                self.pos[p1] -= 1
                if self.pos[p1] == 0:
                    self.pos.pop(p1)
            else:
                break
        # shrink
        if float(len(self.queue)) / float(len(self.pos)) > 3.0:
            new_queue = []
            for (t, p) in self.queue:
                if self.pos[p] == 1:
                    new_queue.append((t,p))
                else:
                    self.pos[p] -= 1
            self.queue = new_queue
        if len(self.pos) >= self.max_grain:
            self.max_hit = True
            del self.queue
            del self.pos
            return self.max_grain
        return len(self.pos)


