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
        self.IM = IM
        self.ST = ST 
        self.Path = PATH 

    def CreateImports(self):
        try:
            self.Import = importlib.import_module(self.IM) 
        except ModuleNotFoundError: 
            TypeError("File is not found")  
            return

        self.Spec =  importlib.util.spec_from_file_location(self.ST, self.Path)
        self.Script = importlib.util.module_from_spec(self.Spec)

        TargetGlobal = sys.modules[self.IM].__dict__

        if hasattr(self.Import, "__all__"):
            Items = self.Import.__all__
        else:
            Items = [k for k in dir(self.Import) if not k.startswith("_")]
            
        for item in Items:
            TargetGlobal[item] = getattr(self.Import, item)
       
 
    def DeleteImports(): 
        pass 

class Conditions:
    def __init__(self): 
        pass  

    def CreateCon():
        pass

    def DeleteCon():
        pass 
 
        