# This acts as an importer mid scripts or provide a greater organization of imported items
# The ram version of the target script will be imported items from the script that get sent to RAM (Main WorkSpace)
# Ad : it can reduce huge amount of code and save working memory ( even dy of pyth ?!?!)
# this also save the modified version of the script and easy to reverse or more changes in one single (RAM VERSION ONLY)
# Notes: i dont know what to add now, but this script can self call to add things too

# Description about how the code, so first, only one "object" is in the hand of the communciator while containing other created "objects", 
# this make things easy to reuse. Like processor for same script, import yet different purpose each time

import sys, pkgutil, builtins
import types

def Initize():
    pass

class Center():
    def __init__(self, Import, Receiver=None, Modification=None):
        self.Mod = Modification
        if Receiver is __path__:
            self.Script = Loader.RetreievFromPath(Receiver)
        else:
            self.Script = Loader.RetreiveScript(Receiver)

        if Import is __path__:
            self.Import = Loader.RetreievFromPath(Import)
        else:
            self.Import = Loader.RetreiveScript(Import)

        self.Handler = Handler()
        
class Loader():
    
    @staticmethod
    def RetreiveScript(Target):
        FoundModule = []
        for Tar in Target:
            try:
                Found = sys.modules[Tar]
            except ModuleNotFoundError:
                Found = sys.modules[types.ModuleType(Tar)]

            FoundModule.append(Found) 

    def RetreievFromPath(Path):
        FoundModule = []
        for package, modname, _ in pkgutil.iter_importers(Path):
            FullModName = f"{package}.{modname}"
            try:
                Mod = sys.modules[FullModName]
            except ModuleNotFoundError:
                Mod =  sys.modules[types.ModuleType(FullModName)]            
            FoundModule.append(Mod)
        return Loader.RetreiveScript(FoundModule)

    def SearchingTarget(Import, Target=None):
        FoundItems = []
        for Im in Import:
            if Target: 
                for Tar in Target:
                    if Im.name == Tar:
                        FoundItems.append(Im)
            else:
                FoundItems.append(Im)
            
        return FoundItems


class Handler():

    def __init__(self, Import=None, Receiver=None):
        self.AllImport = Import
        self.Receiver = Receiver
        
    # Different Target for the same  
    def Connect(self, Yesno, Target=None):
        FoundImport = Loader.SearchingTarget(self.AllImport, Target)
        for Receiver in self.Receiver:
            for Import in FoundImport:
                if not hasattr(Receiver, f"{Import}"):
                    setattr(Receiver, f"{Import}", Import)
                elif not Yesno:
                    if hasattr(Receiver, f"{Import}"):
                        delattr(Receiver, f"{Import}")
                        



        


            





        
                
    

