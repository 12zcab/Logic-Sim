from core import *
from modules.LogicGate import *

class RiseEdge(Module):
    def __init__(self, Name):
        A = IO("A")
        Y = IO("Y")
        ModuleIO = [A, Y]
        Not = NotGate("Not")
        Buf = Buffer("Buffer")
        And = AndGate("And")
        Blocks    = [Not, And,Buf]
        super().__init__(Name, ModuleIO, Blocks)
        A >> Not.IO.A >> And.IO.A
        Not.IO.Y >> Buf.IO.A
        Buf.IO.Y >> And.IO.B
        And.IO.Y >> Y
    @property
    def delay(self):
        return self.child["Buffer"].delay
    @delay.setter
    def delay(self,value):
        self.child["Buffer"].delay = value

class FallEdge(Module):
    def __init__(self, Name):
        A = IO("A")
        Y = IO("Y")
        ModuleIO = [A, Y]
        Not = NotGate("Not")
        Buf = Buffer("Buffer")
        Nor = NorGate("Nor")
        Blocks    = [Not, Nor,Buf]
        super().__init__(Name, ModuleIO, Blocks)
        A >> Not.IO.A >> Nor.IO.A
        Not.IO.Y >> Buf.IO.A
        Buf.IO.Y >> Nor.IO.B
        Nor.IO.Y >> Y
    @property
    def delay(self):
        return self.child["Buffer"].delay
    @delay.setter
    def delay(self,value):
        self.child["Buffer"].delay = value
    
class Edge(Module):
    def __init__(self, Name):
        A = IO("A")
        Y = IO("Y")
        ModuleIO = [A, Y]
        Not = NotGate("Not")
        Buf = Buffer("Buffer")
        Xor = XnorGate("Xor")
        Blocks    = [Not, Xor,Buf]
        super().__init__(Name, ModuleIO, Blocks)
        A >> Not.IO.A >> Xor.IO.A
        Not.IO.Y >> Buf.IO.A
        Buf.IO.Y >> Xor.IO.B
        Xor.IO.Y >> Y
    @property
    def delay(self):
        return self.child["Buffer"].delay
    @delay.setter
    def delay(self,value):
        self.child["Buffer"].delay = value
    

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