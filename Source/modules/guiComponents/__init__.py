from core import *
import time
class Switch(Component):
    def __init__(self, Name):
        super().__init__(Name, [IO("Y")], self.update)
        self.state = False
    def update(self):
        self.IO.Y.Value = Logic.ONE if self.state else Logic.ZERO
    def onclick(self):
        self.state = not self.state
        self.update()
        
class Lamp(Component):
    def __init__(self, Name):
        super().__init__(Name, [IO("A")], self.update)
        self.state = False
    def update(self):
        self.state = (self.IO.A.Value == Logic.ONE)


class OneHertz(Component):
    def __init__(self, Name):
        super().__init__(Name, [IO("Y")], self.update)
        self.state = False
        self.lastupdate = None
        self.IO.Y.Value = Logic.ZERO
    def update(self):
        pass
    def perdeltatick(self):
        now = time.perf_counter_ns()
        if self.lastupdate is None:
            self.lastupdate = now
            return
        TOGGLE_INTERVAL_NS = 500_000_000
        if (now - self.lastupdate) >= TOGGLE_INTERVAL_NS:
            self.lastupdate += TOGGLE_INTERVAL_NS
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