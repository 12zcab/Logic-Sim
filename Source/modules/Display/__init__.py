from core import *

class SevenSegment(Component):
    def __init__(self,Name):
        super().__init__(Name, [IO("A"),IO("B"),IO("C"),IO("D"),IO("E"),IO("F"),IO("G"),IO("DP")], self.update)
        self.ActivateLevel = True
        self.A = False
        self.B = False
        self.C = False
        self.D = False
        self.E = False
        self.F = False
        self.G = False
        self.DP = False
    def update(self):
        self.A = True if self.IO.A.Value == (Logic.ONE if self.ActivateLevel else Logic.ZERO) else False
        self.B = True if self.IO.B.Value == (Logic.ONE if self.ActivateLevel else Logic.ZERO) else False
        self.C = True if self.IO.C.Value == (Logic.ONE if self.ActivateLevel else Logic.ZERO) else False
        self.D = True if self.IO.D.Value == (Logic.ONE if self.ActivateLevel else Logic.ZERO) else False
        self.E = True if self.IO.E.Value == (Logic.ONE if self.ActivateLevel else Logic.ZERO) else False
        self.F = True if self.IO.F.Value == (Logic.ONE if self.ActivateLevel else Logic.ZERO) else False
        self.G = True if self.IO.G.Value == (Logic.ONE if self.ActivateLevel else Logic.ZERO) else False
        self.DP = True if self.IO.DP.Value == (Logic.ONE if self.ActivateLevel else Logic.ZERO) else False
        
class Lamp(Component):
    def __init__(self, Name):
        super().__init__(Name, [IO("A")], self.update)
        self.state = False
    def update(self):
        self.state = (self.IO.A.Value == Logic.ONE)
