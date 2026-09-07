from core.object import *

def and_logic(self):
    # set input
    a = self.IOs["A"].GetInput()
    b = self.IOs["B"].GetInput()
    # set ouput
    self.IOs["OUT"].Output(a and b)

def or_logic(self):
    a = self.IOs["A"].GetInput()
    b = self.IOs["B"].GetInput()
    self.IOs["OUT"].Output(a or b)

def not_logic(self):
    a = self.IOs["A"].GetInput()
    self.IOs["OUT"].Output(not a)



def ANDGate(name):
    return CircuitObject(name, {"A": CircuitIO("A"), "B": CircuitIO("B"), "OUT": CircuitIO("OUT")}, and_logic)
def ORGate(name):
    return CircuitObject(name, {"A": CircuitIO("A"), "B": CircuitIO("B"), "OUT": CircuitIO("OUT")}, or_logic)
def NOTGate(name):
    return CircuitObject(name, {"A": CircuitIO("A"), "OUT": CircuitIO("OUT")}, not_logic)