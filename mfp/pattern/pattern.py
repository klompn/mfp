
class Pattern:
    def result(self):
        return self.flag
    def header(self):
        return list(map(lambda t: '"' + type(self).__name__ + " " + str(t) + '"', self.t))

class ValuePattern(Pattern):
    def check(self, time, value):
        for i in range(len(self.t)):
            if self.flag[i] is None and value >= self.t[i]:
                self.flag[i] = time

class TuplePattern(Pattern):
    def check(self, time, value):
        for i in range(len(self.t)):
            if self.flag[i] is None and value[0] >= self.t[i][0] and value[1] >= self.t[i][1]:
                self.flag[i] = time

class TriplePattern(Pattern):
    def check(self, time, value):
        for i in range(len(self.t)):
            if self.flag[i] is None and value[0] >= self.t[i][0] and value[1] >= self.t[i][1] and value[2] >= self.t[i][2]:
                self.flag[i] = time

class QuadraPattern(Pattern):
    def check(self, time, value):
        for i in range(len(self.t)):
            if self.flag[i] is None and value[0] >= self.t[i][0] and value[1] >= self.t[i][1] and value[2] >= self.t[i][2] and value[3] >= self.t[i][3]:
                self.flag[i] = time