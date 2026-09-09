from core.object import *

def and_logic(self):
    # set input
    a = self.IOs["A"].GetInput()
    b = self.IOs["B"].GetInput()
    # set ouput
    self.IOs["OUT"].Output(a and b)

def nand_logic(self):
    a = self.IOs["A"].GetInput()
    b = self.IOs["B"].GetInput()
    self.IOs["OUT"].Output(not(a and b))

def or_logic(self):
    a = self.IOs["A"].GetInput()
    b = self.IOs["B"].GetInput()
    self.IOs["OUT"].Output(a or b)

def nor_logic(self):
    a = self.IOs["A"].GetInput()
    b = self.IOs["B"].GetInput()
    self.IOs["OUT"].Output(not(a or b))

def xor_logic(self):
    a = self.IOs["A"].GetInput()
    b = self.IOs["B"].GetInput()
    self.IOs["OUT"].Output(a ^ b)

def not_logic(self):
    a = self.IOs["A"].GetInput()
    self.IOs["OUT"].Output(not a)

def half_adder_logic(self):
    a = self.IOs["A"].GetInput()
    b = self.IOs["B"].GetInput()
    self.IOs["SUM"].Output(a ^ b)      # XOR
    self.IOs["CARRY"].Output(a and b)   # AND

def full_adder_logic(self):
    a = self.IOs["A"].GetInput()
    b = self.IOs["B"].GetInput()
    c = self.IOs["C"].GetInput()
    self.IOs["SUM"].Output(a ^ b ^ c)   #S = A ⊕ B ⊕ C
    self.IOs["CARRY"].Output((a and b) or (b and c) or (c and a))   #Carry = AB + BC + AC

def mux21_logic(self):
    i0 = self.IOs["I0"].GetInput()
    i1 = self.IOs["I1"].GetInput()
    s = self.IOs["S"].GetInput()
    # Out = (NOT S AND D0) OR (S AND D1)
    self.IOs["OUT"].Output(i1 if s else i0)

def demux12_logic(self):
    in_val = self.IOs["IN"].GetInput()
    s = self.IOs["S"].GetInput()
    self.IOs["Y0"].Output(in_val if not s else False)
    self.IOs["Y1"].Output(in_val if s else False)

def decoder24_logic(self):
    a0 = self.IOs["A0"].GetInput()
    a1 = self.IOs["A1"].GetInput()
    en = self.IOs["EN"].GetInput()
    
    self.IOs["Y0"].Output(en and (not a1) and (not a0))
    self.IOs["Y1"].Output(en and (not a1) and a0)
    self.IOs["Y2"].Output(en and a1 and (not a0))
    self.IOs["Y3"].Output(en and a1 and a0)

def sr_latch_logic(self):
    # initial
    if not hasattr(self, "state"):
        self.state = False
    s = self.IOs["S"].GetInput()
    r = self.IOs["R"].GetInput()
    if r:
        self.state = s
        
    self.IOs["Q"].Output(self.state)
    self.IOs["QN"].Output(not self.state)


def ANDGate(name):
    return CircuitObject(name, {"A": CircuitIO("A"), "B": CircuitIO("B"), "OUT": CircuitIO("OUT")}, and_logic)
def NANDGate(name):
    return CircuitObject(name, {"A": CircuitIO("A"), "B": CircuitIO("B"), "OUT": CircuitIO("OUT")}, nand_logic)
def ORGate(name):
    return CircuitObject(name, {"A": CircuitIO("A"), "B": CircuitIO("B"), "OUT": CircuitIO("OUT")}, or_logic)
def NORGate(name):
    return CircuitObject(name, {"A": CircuitIO("A"), "B": CircuitIO("B"), "OUT": CircuitIO("OUT")}, nor_logic)
def XORGate(name):
    return CircuitObject(name, {"A": CircuitIO("A"), "B": CircuitIO("B"), "OUT": CircuitIO("OUT")}, xor_logic)
def NOTGate(name):
    return CircuitObject(name, {"A": CircuitIO("A"), "OUT": CircuitIO("OUT")}, not_logic)
def half_adder(name):
    return CircuitObject(name,{
        "A": CircuitIO("A"),
        "B": CircuitIO("B"),
        "SUM": CircuitIO("SUM"),
        "CARRY": CircuitIO("CARRY")
    }, half_adder_logic)
def full_adder(name):
    return CircuitObject(name,{
        "A": CircuitIO("A"),
        "B": CircuitIO("B"),
        "C": CircuitIO("C"),
        "SUM": CircuitIO("SUM"),
        "CARRY": CircuitIO("CARRY")
    }, full_adder_logic)
def mux21(name):
    return CircuitObject(name,{
        "I0": CircuitIO("I0"),
        "I1": CircuitIO("I1"),
        "S": CircuitIO("S"),
        "OUT": CircuitIO("OUT")
    }, mux21_logic)
def demux21(name):
    return CircuitObject(name,{
        "IN": CircuitIO("IN"),
        "S": CircuitIO("S"),
        "Y0": CircuitIO("Y0"),
        "Y1": CircuitIO("Y1")
    }, demux12_logic)
def sr_latch(name):
    return CircuitObject(name,{
            "S": CircuitIO("S"),
            "R": CircuitIO("R"),
            "Q": CircuitIO("Q"),
            "QN": CircuitIO("QN")
        }, sr_latch_logic)
def decoder24(name):
    return CircuitObject(name,{
        "A0": CircuitIO("A0"),
        "A1": CircuitIO("A1"),
        "EN": CircuitIO("EN"),
        "Y0": CircuitIO("Y0"),
        "Y1": CircuitIO("Y1"),
        "Y2": CircuitIO("Y2"),
        "Y3": CircuitIO("Y3")
    }, decoder24_logic)
