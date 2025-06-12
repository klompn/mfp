
from .pattern import QuadraPattern, TuplePattern, TriplePattern, ValuePattern

class RowGrain(ValuePattern):
    def __init__(self):
        self.flag = [None] * 5
        self.t = [2, 4, 8, 16, 32]

class RowSpan(ValuePattern):
    def __init__(self):
        self.flag = [None] * 4
        self.t = [8, 32, 128, 512]

class RowCombo(TuplePattern):
    def __init__(self):
        self.flag = []
        self.t = []
        for x in [2, 4, 8, 16, 32]:
            for r in [8, 32, 128, 512]:
                self.flag.append(None)
                self.t.append((x, r))

class ColumnGrain(ValuePattern):
    def __init__(self):
        self.flag = [None] * 6
        self.t = [2, 4, 8, 16, 32, 64]

class ColumnSpan(ValuePattern):
    def __init__(self):
        self.flag = [None] * 5
        self.t = [8, 64, 512, 4096, 32768]

class ColumnCombo(TuplePattern):
    def __init__(self):
        self.flag = []
        self.t = []
        for x in [2, 4, 8, 16, 32, 64]:
            for r in [8, 64, 512, 4096, 32768]:
                self.flag.append(None)
                self.t.append((x, r))

class BankGrain(TuplePattern):
    def __init__(self):
        self.flag = []
        self.t = []
        for x in [2, 4, 8, 16, 32]:
            for r in [2, 4, 8, 16, 32, 64]:
                self.flag.append(None)
                self.t.append((x, r))

class BankSpan(TuplePattern):
    def __init__(self):
        self.flag = []
        self.t = []
        for x in [8, 32, 128, 512]:
            for r in [8, 64, 512, 4096, 32768]:
                self.flag.append(None)
                self.t.append((x, r))

class BankCombo(QuadraPattern):
    def __init__(self):
        self.flag = []
        self.t = []
        for x in [2, 4, 8, 16, 32]:
            for u in [8, 32, 128, 512]:
                for y in [2, 4, 8, 16, 32, 64]:
                    for v in [8, 64, 512, 4096, 32768]:
                        self.flag.append(None)
                        self.t.append((x, u, y, v))