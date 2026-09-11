from core.object import *

def and_logic(self):
    a = self.IO["A"].Value
    b = self.IO["B"].Value
    self.IO["OUT"].Value = a and b

def nand_logic(self):
    a = self.IO["A"].Value
    b = self.IO["B"].Value
    self.IO["OUT"].Value = not(a and b)

def or_logic(self):
    a = self.IO["A"].Value
    b = self.IO["B"].Value
    self.IO["OUT"].Value = a or b

def nor_logic(self):
    a = self.IO["A"].Value
    b = self.IO["B"].Value
    self.IO["OUT"].Value = not(a or b)

def xor_logic(self):
    a = self.IO["A"].Value
    b = self.IO["B"].Value
    self.IO["OUT"].Value = a ^ b

def not_logic(self):
    a = self.IO["A"].Value
    self.IO["OUT"].Value = not a

def half_adder_logic(self):
    a = self.IO["A"].Value
    b = self.IO["B"].Value
    self.IO["SUM"].Value = a ^ b
    self.IO["CARRY"].Value = a and b

def full_adder_logic(self):
    a = self.IO["A"].Value
    b = self.IO["B"].Value
    c = self.IO["C"].Value
    self.IO["SUM"].Value = a ^ b ^ c
    self.IO["CARRY"].Value = (a and b) or (b and c) or (c and a)

def mux21_logic(self):
    i0 = self.IO["I0"].Value
    i1 = self.IO["I1"].Value
    s = self.IO["S"].Value
    self.IO["OUT"].Value = i1 if s else i0

def demux12_logic(self):
    in_val = self.IO["IN"].Value
    s = self.IO["S"].Value
    self.IO["Y0"].Value = in_val if not s else False
    self.IO["Y1"].Value = in_val if s else False

def decoder24_logic(self):
    a0 = self.IO["A0"].Value
    a1 = self.IO["A1"].Value
    en = self.IO["EN"].Value
    
    self.IO["Y0"].Value = en and (not a1) and (not a0)
    self.IO["Y1"].Value = en and (not a1) and a0
    self.IO["Y2"].Value = en and a1 and (not a0)
    self.IO["Y3"].Value = en and a1 and a0

def sr_latch_logic(self):
    if not hasattr(self, "state"):
        self.state = False
    s = self.IO["S"].Value
    r = self.IO["R"].Value
    if r:
        self.state = s
    self.IO["Q"].Value = self.state
    self.IO["QN"].Value = not self.state


def ANDGate(Name):
    return Component(Name, {"A": IO("A"), "B": IO("B"), "OUT": IO("OUT")}, and_logic)
def NANDGate(Name):
    return Component(Name, {"A": IO("A"), "B": IO("B"), "OUT": IO("OUT")}, nand_logic)
def ORGate(Name):
    return Component(Name, {"A": IO("A"), "B": IO("B"), "OUT": IO("OUT")}, or_logic)
def NORGate(Name):
    return Component(Name, {"A": IO("A"), "B": IO("B"), "OUT": IO("OUT")}, nor_logic)
def XORGate(Name):
    return Component(Name, {"A": IO("A"), "B": IO("B"), "OUT": IO("OUT")}, xor_logic)
def NOTGate(Name):
    return Component(Name, {"A": IO("A"), "OUT": IO("OUT")}, not_logic)
def half_adder(Name):
    return Component(Name,{
        "A": IO("A"),
        "B": IO("B"),
        "SUM": IO("SUM"),
        "CARRY": IO("CARRY")
    }, half_adder_logic)
def full_adder(Name):
    return Component(Name,{
        "A": IO("A"),
        "B": IO("B"),
        "C": IO("C"),
        "SUM": IO("SUM"),
        "CARRY": IO("CARRY")
    }, full_adder_logic)
def mux21(Name):
    return Component(Name,{
        "I0": IO("I0"),
        "I1": IO("I1"),
        "S": IO("S"),
        "OUT": IO("OUT")
    }, mux21_logic)
def demux21(Name):
    return Component(Name,{
        "IN": IO("IN"),
        "S": IO("S"),
        "Y0": IO("Y0"),
        "Y1": IO("Y1")
    }, demux12_logic)
def sr_latch(Name):
    return Component(Name,{
            "S": IO("S"),
            "R": IO("R"),
            "Q": IO("Q"),
            "QN": IO("QN")
        }, sr_latch_logic)
def decoder24(Name):
    return Component(Name,{
        "A0": IO("A0"),
        "A1": IO("A1"),
        "EN": IO("EN"),
        "Y0": IO("Y0"),
        "Y1": IO("Y1"),
        "Y2": IO("Y2"),
        "Y3": IO("Y3")
    }, decoder24_logic)
