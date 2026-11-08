from core.module.object import *

class SpecialModule:
    def __init__(self, name, InSlot : list, OutSlot : list, updateFunctions : str):
        self.Name = name
        self.In = InSlot
        self.Out = OutSlot
    
    def Build(self):
        self.Module = Component(self.Name, {self.In, self.Out}, ) 

