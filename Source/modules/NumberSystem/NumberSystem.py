from core.module.object import *
from modules.LogicGate import *

class Number:
    def __init__(self, SimBox : SimBox):
        self.SimBox = SimBox
        self.Objects = SimBox.Components

    def InitLogic(self, Objects, Logic : list[dict, dict], Changes : list[dict, dict]):
        for Object in self.Objects:
            if getattr(Objects, Object.name):
               Object.Logic = Logic
               Object.Change = Changes
        
    def Activate(self, Objects):
        for Object in Objects:
            if not Object in self.Objects:
               return
        
            for Pin, New in Object.Logic:
               if self.Objects.IOs[Pin]:
                  setattr(self.Logic, Pin, getattr(New, Pin))

            for Pin, Con in Object.Change:
                if Con[getattr(Object.IOs[Pin])]:
                    setattr(Pin, Object, Con[getattr(Object.IOs[Pin])])

    def Change(self, Object, List : str, Value : dict):
        if not Object in self.Objects:
            return
        if not hasattr(Object, List):
            return  

        for Key, Value in Value:
            if not getattr(List, Key):
                List.append({Key : Value})
            else:
                setattr(List, Key, Value)

class Bool:
    def __init__(self, SimBox : SimBox):
        self.SimBox = SimBox
        self.Objects = SimBox.Objects

    def initLogic(self, Objects, Logic : list):
        for Object in self.Objects:
            if getattr(Objects, Object.name):
               Object.BoolLogic = Logic

    def Activate(self, Objects):
        for Object in self.Objects:
            if getattr(Objects, Object.name) and Object.BoolLogic:
                for IOs, Gate in Object.BoolLogic:
                    if not isinstance(IOs, list):
                        IOs = [IOs]
                    for IO in IOs:
                        if not Object.Net[IO]:
                            print("IO is not completed")
                            continue 

                    Gate