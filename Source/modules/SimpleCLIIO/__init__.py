from core import *
import keyboard


def keyboard_button(Name, key):
    io_out = IO("OUT")
    io_loop = IO("LOOP")
    IODict = {"OUT": io_out, "LOOP": io_loop}
    def track(self):
        val = Logic.ONE if keyboard.is_pressed(self.Key) else Logic.ZERO
        self.IO["OUT"].setPower(val, strength=Strength.STRONG, Delay=0)
        current_loop = self.IO["LOOP"].Value
        next_loop = Logic.ZERO if current_loop == Logic.ONE else Logic.ONE
        self.IO["LOOP"].setPower(next_loop, strength=Strength.STRONG, Delay=1)
    obj = Component(Name, IODict, track)
    obj.Key = key
    obj.IO["LOOP"] >> obj.IO["LOOP"]
    return obj

def print_output(Name, out):
    IODict = {"IN": IO("IN")}
    comp = Component(Name,IODict,lambda self: print(f"{out}") if self.IO["IN"].Value else None)
    return comp