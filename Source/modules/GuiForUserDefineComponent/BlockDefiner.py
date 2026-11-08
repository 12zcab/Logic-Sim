from core.module.object import *

class SpecialGate:
    def __init__(self, name, InSlot : list, OutSlot : list):
        self.Name = name
        self.In = InSlot
        self.Out = OutSlot
        self.Funcs = []
        self.Module = Component(self.Name, {self.In, self.Out}, self.Func)

    def ConnectLogic(self):
        if not self.Funcs:  
            return
        self.Module.updateFunction = self.Funcs

    def BuildLogic(self, Logic : list):
        if Logic[0] == "Increase":
            def Increase(Input):
                return Input + Logic[1]
            return self.Func == Increase
        elif Logic[0] == "Decrease":
            def Decrease(Input):
                return Input - Logic[1]
            return self.Func == Decrease
        elif Logic[0] == "Turning":
            def Turning(Input):
                if hasattr(Logic["Conditions"], Input):
                    return Logic["Conditions"]
                return self.Func == Turning

    def StoreComponentInfo(self):
        Nets = self.Module.getNet()
        Funcs = []
        for Func in self.Funcs:
            Funcs.append(Func.__name__)

        return {"Name" : self.Name, "Nets" : Nets, "Funcs" : Funcs}