from core import *
from modules.Legacy.LogicGate import *

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
    def export_custom_data(self):
        return {"delay": self.delay}
    def import_custom_data(self, custom_data: dict, globals_dict: dict = None):
        self.delay = custom_data.get("delay", 1)
        self.update()

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
    def export_custom_data(self):
        return {"delay": self.delay}
    def import_custom_data(self, custom_data: dict, globals_dict: dict = None):
        self.delay = custom_data.get("delay", 1)
        self.update()
    
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
    def export_custom_data(self):
        return {"delay": self.delay}
    def import_custom_data(self, custom_data: dict, globals_dict: dict = None):
        self.delay = custom_data.get("delay", 1)
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
        if self.lastupdate is None or self.lastupdate > now:
            self.lastupdate = now
            return
        interval = 500_000_000 // self.Frequency
        if (now - self.lastupdate) >= interval:
            self.lastupdate += interval
            if (time.perf_counter_ns() - self.lastupdate) >= interval:
                self.lastupdate = time.perf_counter_ns()
            self.state = not self.state
            self.IO.Y.Value = Logic.ONE if self.state else Logic.ZERO
    def export_custom_data(self):
        return {"Frequency": self.Frequency}
    def import_custom_data(self, custom_data: dict, globals_dict: dict = None):
        self.Frequency = custom_data.get("Frequency", 1)
        self.update()