from core import *

class NotGate(Component):
    def __init__(self, Name):
        super().__init__(Name, [IO("A"), IO("OUT")], lambda self: setattr(self.IO.OUT, "Value", not self.IO.A.Value))

class Buffer(Component):
    def __init__(self, Name):
        super().__init__(Name, [IO("A"), IO("OUT")], lambda self: setattr(self.IO.OUT, "Value", self.IO.A.Value))

class AndGate(Component):
    def __init__(self, Name):
        super().__init__(Name, [IO("A"), IO("B"), IO("OUT")], lambda self: setattr(self.IO.OUT, "Value", self.IO.A.Value and self.IO.B.Value))

class OrGate(Component):
    def __init__(self, Name):
        super().__init__(Name, [IO("A"), IO("B"), IO("OUT")], lambda self: setattr(self.IO.OUT, "Value", self.IO.A.Value or self.IO.B.Value))

class XorGate(Component):
    def __init__(self, Name):
        super().__init__(Name, [IO("A"), IO("B"), IO("OUT")], lambda self: setattr(self.IO.OUT, "Value", self.IO.A.Value ^ self.IO.B.Value))

class NandGate(Component):
    def __init__(self, Name):
        super().__init__(Name, [IO("A"), IO("B"), IO("OUT")], lambda self: setattr(self.IO.OUT, "Value", not (self.IO.A.Value and self.IO.B.Value)))

class NorGate(Component):
    def __init__(self, Name):
        super().__init__(Name, [IO("A"), IO("B"), IO("OUT")], lambda self: setattr(self.IO.OUT, "Value", not (self.IO.A.Value or self.IO.B.Value)))

class XnorGate(Component):
    def __init__(self, Name):
        super().__init__(Name, [IO("A"), IO("B"), IO("OUT")], lambda self: setattr(self.IO.OUT, "Value", not (self.IO.A.Value ^ self.IO.B.Value)))
        
class MUX(Component):
    def __init__(self, Name):
        super().__init__(Name, [IO("A"), IO("B"), IO("S"), IO("OUT")], lambda self: setattr(self.IO.OUT, "Value", (self.IO.A.Value and (not self.IO.S.Value) or (self.IO.B.Value and self.IO.S.Value))))

