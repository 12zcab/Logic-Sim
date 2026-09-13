# in here, this will act as import file register or checker
# Or as a general refrence to the data inside of the core script

# Gui based user

import os
import importlib
from Temp.Data import DataHandler

VerScripts = {}
VerAssets = {}


class Checker:        
    def __init__(self, FileNames, DataWanted):
        self.FileNames = FileNames
        self.Datawanted = DataWanted



        

class DataGetter:
    def TypeDataGather(scripts, DataWanted):
        pass

 
    def COLLECTScripts(FileNames):
        CollectedScript = {}
        for ScriptName in FileNames: 
            Script = 0

            try:
                with open(ScriptName, "w") as file:
                    Script = file
            except FileNotFoundError:
                return False

            Path = os.path.abspath(Script)
            ModuleName = os.path.splitext(os.path.basename(Path))[0]

            Spec = importlib.util.spec_from_file_location(ModuleName, Path)
            Module = importlib.util.module_from_spec(Spec)
            


 
 
            


 