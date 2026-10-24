from core import *
import math

class ROM(Component):
    def __init__(self,Name):
        super().__init__(Name, [IO("A0"),IO("A1"),IO("A2"),IO("A3"),IO("D0"),IO("D1"),IO("D2"),IO("D3"),IO("D4"),IO("D5"),IO("D6"),IO("D7")], self.update)
        self.table = [[Logic.ZERO for _ in range(8)] for _ in range(16)]
        self.selected = 0
    def update(self):
        self.selected = 0
        if self.IO.A0.Value == Logic.ONE:
            self.selected += 1
        if self.IO.A1.Value == Logic.ONE:
            self.selected += 2
        if self.IO.A2.Value == Logic.ONE:
            self.selected += 4
        if self.IO.A3.Value == Logic.ONE:
            self.selected += 8
        for i in range(8):
            self.IO["D" + str(i)].Value = self.table[self.selected][i]
    def onclick(self,rx,ry):
        x = math.floor(rx) - 1
        y = math.floor(ry) - 1
        if (x>=0)and(x<=15)and(y>=0)and(y<=7):
            if self.table[x][y] == Logic.ONE:
                self.table[x][y] = Logic.ZERO
            else:
                self.table[x][y] = Logic.ONE
        self.update()