from mfp.util.monotonic_queue import MonotonicQueue
from mfp.util.grain import Grain

class BasicStat:
    def __init__(self, grain, span, window_span, new_fault):
        self.grain = grain
        self.span = span
        self.window_span = window_span
        self.new_fault = new_fault

class Basic:
    def __init__(self, grain_limit, span_limit: int):
        self.max = None
        self.min = None
        self.window_max = MonotonicQueue(86400, lambda x, y: x >= y)
        self.window_min = MonotonicQueue(86400, lambda x, y: x <= y)
        self.grain = Grain(86400, grain_limit)
        self.fault = False
        self.span_limit = span_limit
        self.span_hit = False

    def observe(self, t: int, v: int):
        fault_before = self.fault
        if self.max is None or self.max < v:
            self.max = v
        if self.min is None or self.min > v:
            self.min = v
        if self.max > self.min:
            self.fault = True
        if self.span_hit:
            window_span = self.span_limit
        else:
            window_max = self.window_max.push((t, v))
            window_min = self.window_min.push((t, v))
            window_span = window_max - window_min + 1
            if window_span >= self.span_limit:
                self.span_hit = True
                del self.window_max
                del self.window_min
        grain = self.grain.push((t, v))
        return BasicStat(grain = grain,
                         span = self.max - self.min + 1,
                         window_span = window_span,
                         new_fault = (not fault_before) and self.fault)