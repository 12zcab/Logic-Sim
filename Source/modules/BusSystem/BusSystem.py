from typing import Dict, Any, List, Union
from core.module.object import *

# Assuming these custom modules exist in your framework workspace
# from core.module.object import *
# from modules.LogicGate import *



class Bus:
    def __init__(self, SimBox : SimBox, name : str):
        self.Name = name
        self.SimBox = SimBox
        with open("Bus.json", "r", encoding=None) as file:
            Read = file.read()
            self.Info = Read

    def Build(self):
        if getattr(self.Info, ) 

        