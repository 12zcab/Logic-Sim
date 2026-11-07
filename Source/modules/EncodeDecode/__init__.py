from core import *

class Encoder(Component):
    def __init__(self,Name):
        super().__init__(Name,[IO("0"),IO("1"),IO("2"),IO("3"),IO("4"),IO("5"),IO("6"),IO("7"),IO("OUT")], self.update)
    def update(self):
        value = 0
        for i in range(8):
            value += 2 ** i if self.IO[str(i)].Value == Logic.ONE else 0 
        self.IO.OUT.Value = value
        
class Decoder(Component):
    def __init__(self,Name):
        super().__init__(Name,[IO("0"),IO("1"),IO("2"),IO("3"),IO("4"),IO("5"),IO("6"),IO("7"),IO("IN")], self.update)
    def update(self):
        value = self.IO.IN.Value
        if isinstance(value, int):
            for i in range(8).__reversed__():
                if value >= 2 ** i:
                    value -= 2**i
                    self.IO[str(i)].Value = Logic.ONE
                else:
                    self.IO[str(i)].Value = Logic.ZERO
        else:
            for i in range(8).__reversed__():
                self.IO[str(i)].Value = Logic.X