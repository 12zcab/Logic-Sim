from core import *
import time
class Switch(Component):
    def __init__(self, Name):
        super().__init__(Name, [IO("Y")], self.update)
        self.state = False
    def update(self):
        self.IO.Y.Value = Logic.ONE if self.state else Logic.ZERO
    def onclick(self,rx,ry):
        self.state = not self.state
        self.update()
    def export_custom_data(self):
        return {"state": self.state}
    def import_custom_data(self, custom_data: dict, globals_dict: dict = None):
        self.state = custom_data.get("state", False)
        self.update()
        
class Constant(Component):
    def __init__(self, Name):
        super().__init__(Name, [IO("Y")], self.update)
        self.state = False
    def update(self):
        self.IO.Y.Value = Logic.ONE if self.state else Logic.ZERO
    @property
    def power(self):
        return self.state
    @power.setter
    def power(self,newval):
        self.state = newval
        self.update()
    def export_custom_data(self):
        return {"state": self.state}
    def import_custom_data(self, custom_data: dict, globals_dict: dict = None):
        self.state = custom_data.get("state", True)
        self.update()



class VisualAnalyzer(Component):
    def __init__(self, Name):
        super().__init__(Name, [IO("A")], self.update)
        self.keepTicks = 300
        self.graph = []
    def update(self):
        pass
    def perdeltatick(self):
        value = 1 if self.IO.A.Value == Logic.ONE else 0
        self.graph.append(value)
        while len(self.graph) > self.keepTicks:
            self.graph.pop(0)
    def export_custom_data(self):
        return {"keepTicks": self.keepTicks}
    def import_custom_data(self, custom_data: dict, globals_dict: dict = None):
        self.keepTicks = custom_data.get("keepTicks", True)
        self.update()