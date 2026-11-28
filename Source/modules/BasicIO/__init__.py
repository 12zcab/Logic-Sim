from core import *
import time


class WidthableSwitch(Component):
    def __init__(self, Name):
        super().__init__(Name, [IO("Y0")], self.update)
        self.state = [False]
        self._width = 1

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, newwidth):
        if newwidth == self._width or newwidth < 1:
            return
        if newwidth > self._width:
            for _ in range(newwidth - self._width):
                idx = len(self.IO.keys())
                name = "Y" + str(idx)
                self.addIO(name)
                self.state.append(False)
                if self.guiNode:
                    self.guiNode.add_pin(name, 1, idx)
        elif newwidth < self._width:
            for _ in range(self._width - newwidth):
                idx = len(self.IO.keys()) - 1
                name = "Y" + str(idx)
                self.delIO(name)
                self.state.pop()
                if self.guiNode:
                    self.guiNode.del_pin(name)
        self._width = newwidth
        if self.guiNode:
            self.guiNode.height = newwidth
        self.update()

    def update(self):
        for i in range(self._width):
            self.IO["Y" + str(i)].Value = Logic.ONE if self.state[i] else Logic.ZERO

    def onclick(self, rx, ry):
        # Map relative y-coordinate to the corresponding bit index
        idx = int(ry)
        if 0 <= idx < self._width:
            self.state[idx] = not self.state[idx]
            self.update()

    def export_custom_data(self):
        return {"state": self.state, "_width": self._width}

    def import_custom_data(self, custom_data: dict, globals_dict: dict = None):
        self.width = custom_data.get("_width", 1)
        saved_state = custom_data.get("state", [False] * self._width)
        if isinstance(saved_state, bool):
            self.state = [saved_state] + [False] * (self._width - 1)
        else:
            self.state = (saved_state + [False] * self._width)[:self._width]
        self.update()


class WidthableLamp(Component):
    def __init__(self, Name):
        super().__init__(Name, [IO("A0")], self.update)
        self.state = [Logic.ZERO]
        self._width = 1
        self.colour = "#38bdf8"
        self.showNumber = True

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, newwidth):
        if newwidth == self._width or newwidth < 1:
            return
        if newwidth > self._width:
            for _ in range(newwidth - self._width):
                idx = len(self.IO.keys())
                name = "A" + str(idx)
                self.addIO(name)
                self.state.append(Logic.ZERO)
                if self.guiNode:
                    self.guiNode.add_pin(name, 1, idx)
        elif newwidth < self._width:
            for _ in range(self._width - newwidth):
                idx = len(self.IO.keys()) - 1
                name = "A" + str(idx)
                self.delIO(name)
                self.state.pop()
                if self.guiNode:
                    self.guiNode.del_pin(name)
        self._width = newwidth
        if self.guiNode:
            self.guiNode.height = newwidth
        self.update()

    def update(self):
        for i in range(self._width):
            self.state[i] = self.IO["A" + str(i)].Value

    def export_custom_data(self):
        return {
            "colour": self.colour,
            "showNumber": self.showNumber,
            "_width": self._width
        }

    def import_custom_data(self, custom_data: dict, globals_dict: dict = None):
        self.colour = custom_data.get("colour", "#38bdf8")
        self.showNumber = custom_data.get("showNumber", True)
        self.width = custom_data.get("_width", 1)
        self.update()