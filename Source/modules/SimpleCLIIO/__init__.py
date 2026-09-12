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
def keyIn(Name,key,IO2):
    IODict = {"Out": IO("Output")}
    IODict.Out >> IO2
    obj = Component(Name,IODict,keyboardTrack)
    obj.Key = key
    return obj
def charOut(Name,char,IO2):
    IODict = {"In": IO("Input")}
    IODict.In >> IO2
    return Component(Name,IODict,lambda self: print(f"{out}") if self.IO["In"].Value else None)