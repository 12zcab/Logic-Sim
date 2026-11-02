class System:
    def __init__(self, Objects):
        self.Objects = Objects

    def InitLogic(self, Logic : list[dict, dict], Changes : list[dict, dict]):
        for Object in self.Objects:
            Object.Logic = Logic
            Object.Change = Changes
            Object.Activate = self.Activate

    def Activate(self):
        

            