from core.object import *

def and_logic(self):
    # set input
    a = self.IOs["A"].GetInput()
    b = self.IOs["B"].GetInput()
    # set ouput
    self.IOs["OUT"].Output(a and b)
    return CircuitObject("AND_Gate", {"A": CircuitIO("A"), "B": CircuitIO("B"), "OUT": CircuitIO("OUT")}, and_logic)