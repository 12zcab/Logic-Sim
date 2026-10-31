from core import *
import time
class Switch(Component):
    def __init__(self, Name):
        super().__init__(Name, [IO("Y")], self.update)
        self.state = False
    def update(self):
        self.IO.Y.Value = Logic.ONE if self.state else Logic.ZERO
    def onclick(self,rx,ry):
        self.state = not self.state
        self.update()
        
class Constant(Component):
    def __init__(self, Name):
        super().__init__(Name, [IO("Y")], self.update)
        self.state = False
    def update(self):
        self.IO.Y.Value = Logic.ONE if self.state else Logic.ZERO
    @property
    def power(self):
        return self.state
    @power.setter
    def power(self,newval):
        self.state = newval
        self.update()


class PulseGenerator(Component):
    def __init__(self, Name):
        super().__init__(Name, [IO("Y")], self.update)
        self.state = False
        self.lastupdate = None
        self.Frequency = 1
        self.IO.Y.Value = Logic.ZERO
    def update(self):
        pass
    def perdeltatick(self):
        now = time.perf_counter_ns()
        if self.lastupdate is None:
            self.lastupdate = now
            return
        if (now - self.lastupdate) >= (500000000 // self.Frequency):
            self.lastupdate += (500000000 // self.Frequency)
            if (time.perf_counter_ns() - self.lastupdate) >= (500000000 // self.Frequency):
                self.lastupdate = None
            self.state = not self.state
            self.IO.Y.Value = Logic.ONE if self.state else Logic.ZERO
            
class VisualAnalyzer(Component):
    def __init__(self, Name):
        super().__init__(Name, [IO("A")], self.update)
        self.keepTicks = 300
        self.graph = []
    def update(self):
        pass
    def perdeltatick(self):
        value = 1 if self.IO.A.Value == Logic.ONE else 0
        self.graph.append(value)
        while len(self.graph) > self.keepTicks:
            self.graph.pop(0)