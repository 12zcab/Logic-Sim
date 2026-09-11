from core.object import *
import keyboard
def keyboardTrack(self):
    self.IO["Out"].Value = keyboard.is_pressed(self.Key)
def keyboard_button(Name, key):
    IODict = {"Out": IO("Output")}
    obj = Component(Name,IODict,keyboardTrack)
    obj.Key = key
    return obj
def print_output(Name, out):
    IODict = {"In": IO("Input")}
    return Component(Name,IODict,lambda self: print(f"{out}") if self.IO["In"].Value else None)