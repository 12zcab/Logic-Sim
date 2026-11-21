from core import *
import time


class Switch(Component):
    def __init__(self, Name):
        super().__init__(Name, [IO("Y0")], self.update)
        self.state = []
        self._width = 1
    @property
    def width(self):
        return self._width
    @width.setter
    def width(self,newwidth):
        if newwidth == _width:
            return
        if newwidth > _width:
            for _ in range(newwidth - _width):
                name = "Y" + str(len(self.IO.keys()))
                self.addIO(name)
                if self.guiNode:
                    self.guiNode.add_pin
        if newwidth < _width:
            for _ in range(_width - newwidth):
                name = "Y" + str(len(self.IO.keys()) - 1)
                self.delIO(name)
        self._width = newwidth
    def update(self):
        self.IO.Y.Value = Logic.ONE if self.state else Logic.ZERO
    def onclick(self,rx,ry):
        self.state = not self.state
        self.update()
    def export_custom_data(self):
        return {"state": self.state,"_width": self._width}
    def import_custom_data(self, custom_data: dict, globals_dict: dict = None):
        self.state = custom_data.get("state", False)
        self.state = custom_data.get("_width", 1)
        self.update()


class Lamp(Component):
    def __init__(self, Name):
        super().__init__(Name, [IO("A")], self.update)
        self.state = Logic.ZERO
        self.colour = "#38bdf8"
        self.showNumber = True
    def update(self):
        self.state = self.IO.A.Value
    def export_custom_data(self):
        return {"colour": self.ActivateLevel,"showNumber": self.showNumber}
    def import_custom_data(self, custom_data: dict, globals_dict: dict = None):
        self.colour = custom_data.get("colour", "#38bdf8")
        self.showNumber = custom_data.get("showNumber",True)
        self.update()