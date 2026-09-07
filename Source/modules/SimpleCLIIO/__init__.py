from core.object import *
import keyboard

def keyboard_button(name, key):
    IODict = {"Out": CircuitIO("Output")}
    return CircuitObject(name,IODict,lambda self: self.IOs["Out"].Output(keyboard.is_pressed(key)))
def print_output(name, out):
    IODict = {"In": CircuitIO("Input")}
    return CircuitObject(name,IODict,lambda self: print(f"{out}") if self.IOs["In"].GetInput() else None)