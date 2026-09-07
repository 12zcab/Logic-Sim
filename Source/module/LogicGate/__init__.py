from core.object import *

def and_gate_logic(ios):
    #read signal
    in_a = ios["a"].GetInput()
    in_b = ios["b"].GetInput()
    #logic rule
    logic = in_a and in_b 
    #write signal
    ios["out"].Output(result)
