# This acts as an importer mid scripts or provide a greater organization of imported items
# The ram version of the target script will be imported items from the script that get sent to RAM (Main WorkSpace)
# Ad : it can reduce huge amount of code and save working memory ( even dy of pyth ?!?!)
# this also save the modified version of the script and easy to reverse or more changes in one single (RAM VERSION ONLY)
# Notes: i dont know what to add now, but this script can self call to add things too

# Description about how the code, so first, only one "object" is in the hand of the communciator while containing other created "objects", 
# this make things easy to reuse. Like processor for same script, import yet different purpose each time

import ast, sys
from Temp import Importer


class ObjectInit():
    def __init__(self, RAMScript, ImportFile, conditions=None):
        self.Script = Loader.LoadScript(RAMScript)
        self.Import = Loader.LoadImport(ImportFile)
        self.conditions = conditions 
    def Override(self, Required):
        pass
        

class Loader():
    @staticmethod
    def GetScript(TargetScript):
        try:
            return sys.modules[TargetScript]
        except FileNotFoundError or ModuleNotFoundError:
            print("Module/Script not found in RAM")
            return None 

    def GetImport(TargetImport):
        try:
            with open(TargetImport, "r") as file:
                return file
        except FileNotFoundError:
            print("Import not found")
            return None 

    def LoadImporter(self):
        pass


class Processor(): 
    def __init__(self, ImportRam, ScriptRam, conditions):
        self.ImportRam = ImportRam
        self.ScriptRam = ScriptRam
        self.conditions = conditions

    def CreateConditions(self):
        pass
        