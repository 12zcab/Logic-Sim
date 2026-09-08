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
        "A": CircuitIO(f"{name}_A"),
        "B": CircuitIO(f"{name}_B"),
        "SUM": CircuitIO(f"{name}_SUM"),
        "CARRY": CircuitIO(f"{name}_CARRY")
    }, half_adder_logic)
