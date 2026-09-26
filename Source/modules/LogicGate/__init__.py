from core import *

NOT_LUT = {
    Logic.ZERO: Logic.ONE, Logic.ONE: Logic.ZERO,
    Logic.X: Logic.X,       Logic.Z: Logic.X
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

class Buffer(Component):
    def __init__(self, Name):
        super().__init__(Name, [IO("A"), IO("Y")], self.update)
    def update(self):
        self.IO.Y.Value = self.IO.A.Value

class NotGate(Component):
    def __init__(self, Name):
        super().__init__(Name, [IO("A"), IO("Y")], self.update)
    def update(self):
        self.IO.Y.Value = NOT_LUT.get(self.IO.A.Value, Logic.X)

class AndGate(Component):
    def __init__(self, Name):
        super().__init__(Name, [IO("A"), IO("B"), IO("Y")], self.update)
    def update(self):
        self.IO.Y.Value = AND_LUT.get((self.IO.A.Value, self.IO.B.Value), Logic.X)

class OrGate(Component):
    def __init__(self, Name):
        super().__init__(Name, [IO("A"), IO("B"), IO("Y")], self.update)
    def update(self):
        self.IO.Y.Value = OR_LUT.get((self.IO.A.Value, self.IO.B.Value), Logic.X)

class NandGate(Component):
    def __init__(self, Name):
        super().__init__(Name, [IO("A"), IO("B"), IO("Y")], self.update)
    def update(self):
        and_res = AND_LUT.get((self.IO.A.Value, self.IO.B.Value), Logic.X)
        self.IO.Y.Value = NOT_LUT.get(and_res, Logic.X)

class OrNotGate(Component):
    def __init__(self, Name):
        super().__init__(Name, [IO("A"), IO("B"), IO("Y")], self.update)
    def update(self):
        a_val = self.IO.A.Value
        b_val = self.IO.B.Value
        not_b = NOT_LUT.get(b_val, Logic.X)
        self.IO.Y.Value = OR_LUT.get((a_val, not_b), Logic.X)
        
class NandGate3(Component):
    def __init__(self, Name):
        super().__init__(Name, [IO("A"), IO("B"), IO("C"), IO("Y")], self.update)

    def update(self):
        a, b, c = self.IO.A.Value, self.IO.B.Value, self.IO.C.Value
        if a == Logic.ZERO or b == Logic.ZERO or c == Logic.ZERO:
            self.IO.Y.Value = Logic.ONE
            return
        ab_res = AND_LUT.get((a, b), Logic.X)
        abc_res = AND_LUT.get((ab_res, c), Logic.X)
        self.IO.Y.Value = NOT_LUT.get(abc_res, Logic.X)