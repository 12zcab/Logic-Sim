from typing import Dict, Any, List, Union
from core.module.object import *

# Assuming these custom modules exist in your framework workspace
# from core.module.object import *
# from modules.LogicGate import *



class Bus:
    def __init__(self, SimBox : SimBox, name : str, Input : int, Output : int):
        self.Name = name
        self.InSlot = Input
        self.OutSlot = Output
        self.SimBox = SimBox
        self.TransformConnection = {}
        self.CombineConnection = {}
        self.SlotConnection = {}

    def Connect(self, InSlot, OutSlot):
        if getattr(self.SlotConnection, str(InSlot)):
            if not getattr(self.SlotConnection, str(InSlot)) == OutSlot:
                [self.SlotConnection[str(InSlot)]].append(OutSlot)
        else:
            self.SlotConnection[str(InSlot)] = OutSlot

    def BuildTransform(self, InSlot, Logic : str):
        if InSlot < self.InSlot:
            return

        if getattr(self.LogicConnection, str(InSlot)):
            return
        else:
            self.LogicConnection[str(InSlot)] = Logic

    def BuildCombination(self, Output, Logic : str):
        if getattr(self.CombineConnection, Output):
            return

        self.CombineConnection[str(Output)] = Logic


    def Combine(self, OutSlot):
        try:
           String = getattr(self.CombineConnection, str(OutSlot))
        except AttributeError:
            return

        return exec(String)

    def Transform(self, InSlot):
        try:
            String = getattr(self.TransformConnection, InSlot)
        except AttributeError:
            return

        return exec(String)  