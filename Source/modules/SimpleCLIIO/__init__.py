from core import *
import keyboard
def keyboardTrack(self):
    self.IO["OUT"].Value = keyboard.is_pressed(self.Key)
def keyboard_button(Name, key):
    IODict = {"OUT": IO("OUT")}
    obj = Component(Name,IODict,keyboardTrack)
    obj.Key = key
    return obj
def print_output(Name, out):
    IODict = {"IN": IO("IN")}
    return Component(Name,IODict,lambda self: print(f"{out}") if self.IO["IN"].Value else None)