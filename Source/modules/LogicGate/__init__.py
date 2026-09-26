from core import *


NOT_LUT = {
    Logic.ZERO: Logic.ONE,
    Logic.ONE:  Logic.ZERO,
    Logic.X:    Logic.X,
    Logic.Z:    Logic.X
}
AND_LUT = {
    (Logic.ZERO, Logic.ZERO): Logic.ZERO, (Logic.ZERO, Logic.ONE):  Logic.ZERO,
    (Logic.ZERO, Logic.X):    Logic.ZERO, (Logic.ZERO, Logic.Z):    Logic.ZERO,
    (Logic.ONE,  Logic.ZERO): Logic.ZERO, (Logic.X,    Logic.ZERO): Logic.ZERO,
    (Logic.Z,    Logic.ZERO): Logic.ZERO,
    (Logic.ONE,  Logic.ONE):  Logic.ONE,
    (Logic.ONE,  Logic.X):    Logic.X,    (Logic.ONE,  Logic.Z):    Logic.X,
    (Logic.X,    Logic.ONE):  Logic.X,    (Logic.Z,    Logic.ONE):  Logic.X,
    (Logic.X,    Logic.X):    Logic.X,    (Logic.X,    Logic.Z):    Logic.X,
    (Logic.Z,    Logic.X):    Logic.X,    (Logic.Z,    Logic.Z):    Logic.X,
}
OR_LUT = {
    (Logic.ONE,  Logic.ONE):  Logic.ONE,  (Logic.ONE,  Logic.ZERO): Logic.ONE,
    (Logic.ONE,  Logic.X):    Logic.ONE,  (Logic.ONE,  Logic.Z):    Logic.ONE,
    (Logic.ZERO, Logic.ONE):  Logic.ONE,  (Logic.X,    Logic.ONE):  Logic.ONE,
    (Logic.Z,    Logic.ONE):  Logic.ONE,
    (Logic.ZERO, Logic.ZERO): Logic.ZERO,
    (Logic.ZERO, Logic.X):    Logic.X,    (Logic.ZERO, Logic.Z):    Logic.X,
    (Logic.X,    Logic.ZERO): Logic.X,    (Logic.Z,    Logic.ZERO): Logic.X,
    (Logic.X,    Logic.X):    Logic.X,    (Logic.X,    Logic.Z):    Logic.X,
    (Logic.Z,    Logic.X):    Logic.X,    (Logic.Z,    Logic.Z):    Logic.X,
}
XOR_LUT = {
    (Logic.ZERO, Logic.ZERO): Logic.ZERO,
    (Logic.ZERO, Logic.ONE):  Logic.ONE,
    (Logic.ONE,  Logic.ZERO): Logic.ONE,
    (Logic.ONE,  Logic.ONE):  Logic.ZERO,
    (Logic.ZERO, Logic.X):    Logic.X,    (Logic.ZERO, Logic.Z):    Logic.X,
    (Logic.ONE,  Logic.X):    Logic.X,    (Logic.ONE,  Logic.Z):    Logic.X,
    (Logic.X,    Logic.ZERO): Logic.X,    (Logic.Z,    Logic.ZERO): Logic.X,
    (Logic.X,    Logic.ONE):  Logic.X,    (Logic.Z,    Logic.ONE):  Logic.X,
    (Logic.X,    Logic.X):    Logic.X,    (Logic.X,    Logic.Z):    Logic.X,
    (Logic.Z,    Logic.X):    Logic.X,    (Logic.Z,    Logic.Z):    Logic.X,
}

class NotGate(Component):
    def __init__(self, Name):
        super().__init__(
            Name, 
            [IO("A"), IO("Y")], 
            lambda self: setattr(self.IO.Y, "Value", NOT_LUT.get(self.IO.A.Value, Logic.X))
        )

class Buffer(Component):
    def __init__(self, Name):
        super().__init__(
            Name, 
            [IO("A"), IO("Y")], 
            lambda self: setattr(self.IO.Y, "Value", self.IO.A.Value) # Buffer maps 1:1 directly
        )

class AndGate(Component):
    def __init__(self, Name):
        super().__init__(
            Name, 
            [IO("A"), IO("B"), IO("Y")], 
            lambda self: setattr(self.IO.Y, "Value", AND_LUT.get((self.IO.A.Value, self.IO.B.Value), Logic.X))
        )

class OrGate(Component):
    def __init__(self, Name):
        super().__init__(
            Name, 
            [IO("A"), IO("B"), IO("Y")], 
            lambda self: setattr(self.IO.Y, "Value", OR_LUT.get((self.IO.A.Value, self.IO.B.Value), Logic.X))
        )

class XorGate(Component):
    def __init__(self, Name):
        super().__init__(
            Name, 
            [IO("A"), IO("B"), IO("Y")], 
            lambda self: setattr(self.IO.Y, "Value", XOR_LUT.get((self.IO.A.Value, self.IO.B.Value), Logic.X))
        )


class NandGate(Component):
    def __init__(self, Name):
        super().__init__(
            Name, 
            [IO("A"), IO("B"), IO("Y")], 
            lambda self: setattr(self.IO.Y, "Value", NOT_LUT.get(AND_LUT.get((self.IO.A.Value, self.IO.B.Value), Logic.X), Logic.X))
        )

class NorGate(Component):
    def __init__(self, Name):
        super().__init__(
            Name, 
            [IO("A"), IO("B"), IO("Y")], 
            lambda self: setattr(self.IO.Y, "Value", NOT_LUT.get(OR_LUT.get((self.IO.A.Value, self.IO.B.Value), Logic.X), Logic.X))
        )

class XnorGate(Component):
    def __init__(self, Name):
        super().__init__(
            Name, 
            [IO("A"), IO("B"), IO("Y")], 
            lambda self: setattr(self.IO.Y, "Value", NOT_LUT.get(XOR_LUT.get((self.IO.A.Value, self.IO.B.Value), Logic.X), Logic.X))
        )
