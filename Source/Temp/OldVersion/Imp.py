# This acts as an importer mid scripts or provide a greater organization of imported items
# The ram version of the target script will be imported items from the script that get sent to target
# Ad : it can reduce huge amount of code and save working memory
# this also save the modified version of the script and easy to reverse or more changes in one single 
# Notes: i dont know what to add now, but this script can self call to add things too

import ast, sys

class Communciator:
    def __init__(self, ST, IM):
        self.Loader = Loader(IM, ST) 
        self.Import = self.Loader.GetImport()
        self.TargetScript = self.Loader.GetScript()

    def Completion(self, Target=None):
        if not self.Loader or not self.Import:
            return print("Data is not enough for further execution")
        
        self.Importer = Importer(self.TargetScript, self.Import, Target)
        return self.Importer.Compile()

    def Deletion(self, Target=None):
        self.NameSpace = sys.modules[self.ST].__dict__
        for name in Target:
            self.NameSpace[name]
            print (f"{self.NameSpace[name]}" " has been deleted") 

 
class Loader:
    def __init__(self, IM, ST):
        self.TargetImport = IM 
        self.TargetScript = ST  

    def GetImport(self):
        try:
            with open(self.TargetImport, "r") as file:
                self.Import = file.read()
        except (ModuleNotFoundError, FileNotFoundError): 
            TypeError("File is not found")  
            self.Import = False
        return ast.parse(self.Import) 

    def GetScript(self): 
        try:
            self.TargetRam = sys.modules[self.TargetScript]
        except ModuleNotFoundError: 
            self.TargetRam = False 
            raise TypeError("Module is not found in RAM")
               
    
class Importer:
    def __init__(self, TargetScript, ImportTree, WantedItems):
        self.TargetScript = TargetScript
        self.ImportTree = ImportTree
        self.WantedItems = WantedItems
 
    def Compile(self):
        self.SelectedItems = []
        for Item in self.ImportTree.body:
            if isinstance(Item, ast.FunctionDef) or isinstance(Item, ast.ClassDef):
                for Name in self.WantedItems:
                    if Name == Item.name:
                        self.SelectedItems.append(Item)
                        

        NewcodeInfo = ast.Module(body=self.SelectedItems, type_ignores=[])
        Newcode = compile(NewcodeInfo, filename="<ast>", mode="exec")

        exec(Newcode, self.TargetScript.__dict__)  
  
        return self.TargetScript