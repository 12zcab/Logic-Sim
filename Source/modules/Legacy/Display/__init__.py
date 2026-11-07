from core import *

class SevenSegment(Component):
    def __init__(self,Name):
        super().__init__(Name, [IO("A"),IO("B"),IO("C"),IO("D"),IO("E"),IO("F"),IO("G"),IO("DP")], self.update)
        self.ActivateLevel = True
        self.A = False
        self.B = False
        self.C = False
        self.D = False
        self.E = False
        self.F = False
        self.G = False
        self.DP = False
    def update(self):
        self.A = True if self.IO.A.Value == (Logic.ONE if self.ActivateLevel else Logic.ZERO) else False
        self.B = True if self.IO.B.Value == (Logic.ONE if self.ActivateLevel else Logic.ZERO) else False
        self.C = True if self.IO.C.Value == (Logic.ONE if self.ActivateLevel else Logic.ZERO) else False
        self.D = True if self.IO.D.Value == (Logic.ONE if self.ActivateLevel else Logic.ZERO) else False
        self.E = True if self.IO.E.Value == (Logic.ONE if self.ActivateLevel else Logic.ZERO) else False
        self.F = True if self.IO.F.Value == (Logic.ONE if self.ActivateLevel else Logic.ZERO) else False
        self.G = True if self.IO.G.Value == (Logic.ONE if self.ActivateLevel else Logic.ZERO) else False
        self.DP = True if self.IO.DP.Value == (Logic.ONE if self.ActivateLevel else Logic.ZERO) else False
    def export_custom_data(self):
        return {"ActivateLevel": self.ActivateLevel}
    def import_custom_data(self, custom_data: dict, globals_dict: dict = None):
        self.ActivateLevel = custom_data.get("ActivateLevel", True)
        self.update()
class Lamp(Component):
    def __init__(self, Name):
        super().__init__(Name, [IO("A")], self.update)
        self.state = Logic.ZERO
        self.colour = "#38bdf8"
        self.showNumber = True
    def update(self):
        self.state = self.IO.A.Value
        print(self.state)
    def export_custom_data(self):
        return {"colour": self.ActivateLevel,"showNumber": self.showNumber}
    def import_custom_data(self, custom_data: dict, globals_dict: dict = None):
        self.colour = custom_data.get("colour", "#38bdf8")
        self.showNumber = custom_data.get("showNumber",True)
        self.update()