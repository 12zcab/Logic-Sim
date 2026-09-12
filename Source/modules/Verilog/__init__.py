import os
import sys
from core.object import *

"""VerilogModule -> VerilogBlock/SubModule -> Components for HIGHLY MODULARIZEDDD"""

"""
VerilogModule CPU
  ├── self.IO Reset, Clock, Total_Out
  └── self.Block
        ├── VerilogBlock CU
        │     └── self.Component -> [ANDGate, ORGate, NOTGate...]
        │
        └── VerilogModule RegisterFile
              ├── self.IO Reg_Addr, Reg_Data
              └── self.Block
                    ├── VerilogModule  Reg_Bit0
                    │     ├── self.IO
                    │     └── self.Block -> [AlwaysTimeBlock, AlwaysCombBlock]
                    │
                    └── VerilogModule  Reg_Bit1
                          ...
"""

def updateRecursive(array):
    if not array:
        return
    for obj in array:
        if hasattr(obj, "update"):
            obj.update()

class VerilogModule(Component):
    def __init__(self, Name, PinOutIOs, BlockArray):
        super().__init__(Name, BlockArray, lambda self: updateRecursive(self.Block))
        self.Block = self.IO
        self.IO = PinOutIOs
    def allNet(self):
        arrayNet = []
        for k,v in self.IO.items():
            arrayNet.append(v.Net)
        for h,block in self.Block.items():
            arrayNet = [*arrayNet,*block.allNet()]
        return arrayNet

class VerilogBlock(Component):
    def __init__(self, Name, ComponentArray):
        super().__init__(Name, ComponentArray, lambda self: updateRecursive(self.Component))
        self.Component = self.IO
        del self.IO
    def allNet(self):
        arrayNet = []
        for h,component in self.Component.items():
            for k,v in component.IO.items():
                arrayNet.append(v.Net)
        return arrayNet

