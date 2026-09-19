# This acts as an importer mid scripts or provide a greater organization of imported items
# Also create the conditions statement u wants for the imported
# Ad : it can reduce huge amount of code and save working memory
import importlib
import importlib.util
import ast
import sys

def SelfDeclare():
    Importer(Importer, all)

class Importer:
    def __init__(self, IM, ST, PATH):
        self.TargetImport = IM
        self.TargetScript = ST 
        self.Path = PATH

    def GetImport(self):
        try:
            self.Import = importlib.import_module(self.TargetImport) 
        except ModuleNotFoundError: 
            TypeError("File is not found")  
            return self.Import == None

    def LoadImport(self):
        if hasattr(self.Import, "__all__"): 
            self.Items = self.Import.__all__
        else:
            self.Items = [k for k in dir(self.Import) if not k.startswith("_")]
        return self.Items

    def LoadScript(self):
        pass
 
class HandleNode:
    def __init__(self, TargetScript, TargetArea):
        self.TargetScript = TargetScript
        self.TargetArea = TargetArea

    def LoadTarget(self):
        

        

class Conditions: 
    def __init__(self, Cons, ST, TG):
        self.Cons = Cons 
        self.TargetScript = ST
        self.Target = TG

        self.TargetGlobal = sys.modules[self.TargetScript].__dict__
    

    def CreateCon():

        if not self.
        pass

    def DeleteCon():
        pass 
 
        