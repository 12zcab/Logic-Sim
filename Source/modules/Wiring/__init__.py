from core import *

class Encoder(Component):
    def __init__(self,Name):
        super().__init__(Name,[IO("0"),IO("1"),IO("2"),IO("3"),IO("4"),IO("5"),IO("6"),IO("7"),IO("OUT")], self.update)
        self._width = 8
    @property
    def width(self):
        return self._width
    @width.setter
    def width(self,newwidth):
        if newwidth == self._width:
            return
        if newwidth > self._width:
            for _ in range(newwidth - self._width):
                name = str(len(self.IO.keys()) - 1)
                self.addIO(name)
                if self.guiNode:
                    self.guiNode.add_pin(name,-1,int(name))
        if newwidth < self._width:
            for _ in range(self._width - newwidth):
                name = str(len(self.IO.keys()) - 2)
                self.delIO(name)
                if self.guiNode:
                    self.guiNode.del_pin(name)
        self._width = newwidth
        self.guiNode.height = newwidth
        out = next((p for p in self.guiNode.pins if p.name == "OUT"), None)
        out.rel_y = newwidth/2
    def update(self):
        value = 0
        for i in range(self.width):
            value += 2 ** i if self.IO[str(i)].Value == Logic.ONE else 0 
        self.IO.OUT.Value = value
    def export_custom_data(self):
        return {
            "_width": self._width
        }
    def import_custom_data(self, custom_data: dict, globals_dict: dict = None):
        self.width = custom_data.get("_width", 8)
        self.update()
class Decoder(Component):
    def __init__(self,Name):
        super().__init__(Name,[IO("0"),IO("1"),IO("2"),IO("3"),IO("4"),IO("5"),IO("6"),IO("7"),IO("IN")], self.update)
        self._width = 8
    @property
    def width(self):
        return self._width
    @width.setter
    def width(self,newwidth):
        if newwidth == self._width:
            return
        if newwidth > self._width:
            for _ in range(newwidth - self._width):
                name = str(len(self.IO.keys()) - 1)
                self.addIO(name)
                if self.guiNode:
                    self.guiNode.add_pin(name,1,int(name))
        if newwidth < self._width:
            for _ in range(self._width - newwidth):
                name = str(len(self.IO.keys()) - 2)
                self.delIO(name)
                if self.guiNode:
                    self.guiNode.del_pin(name)
        self._width = newwidth
        self.guiNode.height = newwidth
        inpin = next((p for p in self.guiNode.pins if p.name == "IN"), None)
        inpin.rel_y = newwidth/2
    def update(self):
        value = self.IO.IN.Value
        if isinstance(value, int):
            for i in range(self.width).__reversed__():
                if value >= 2 ** i:
                    value -= 2**i
                    self.IO[str(i)].Value = Logic.ONE
                else:
                    self.IO[str(i)].Value = Logic.ZERO
        else:
            for i in range(self.width).__reversed__():
                self.IO[str(i)].Value = Logic.X
    
    def export_custom_data(self):
        return {
            "_width": self._width
        }
    def import_custom_data(self, custom_data: dict, globals_dict: dict = None):
        self.width = custom_data.get("_width", 8)
        self.update()



class Arrange(Component):
    def __init__(self, Name):
        super().__init__(Name, [IO(str(i)) for i in range(8)], self.update)
        self._width = 8

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, newwidth):
        if newwidth == self._width or newwidth < 1:
            return
        if newwidth > self._width:
            for i in range(self._width, newwidth):
                name = str(i)
                self.addIO(name)
                if self.guiNode:
                    self.guiNode.add_pin(name, 0.5, i + 0.5)
        elif newwidth < self._width:
            for i in range(self._width - 1, newwidth - 1, -1):
                name = str(i)
                self.delIO(name)
                if self.guiNode:
                    self.guiNode.del_pin(name)
        self._width = newwidth
        if self.guiNode:
            self.guiNode.height = newwidth

    def update(self):
        pass

    def export_custom_data(self):
        return {"_width": self._width}

    def import_custom_data(self, custom_data: dict, globals_dict: dict = None):
        self.width = custom_data.get("_width", 8)