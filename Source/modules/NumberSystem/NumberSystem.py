from core.module.object import *

class System:
    def __init__(self, SimBox : SimBox):
        self.SimBox = SimBox
        self.Objects = SimBox.Components

    def InitLogic(self, Logic : list[dict, dict], Changes : list[dict, dict]):
        for Object in self.Objects:
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
