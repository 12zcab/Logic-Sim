# This acts as an importer mid scripts or provide a greater organization of imported items
# The ram version of the target script will be imported items from the script that get sent to RAM (Main WorkSpace)
# Ad : it can reduce huge amount of code and save working memory ( even dy of pyth ?!?!)
# this also save the modified version of the script and easy to reverse or more changes in one single (RAM VERSION ONLY)
# Notes: i dont know what to add now, but this script can self call to add things too

# Description about how the code, so first, only one "object" is in the hand of the communciator while containing other created "objects", 
# this make things easy to reuse. Like processor for same script, import yet different purpose each time

import pkgutil, importlib,  ast
import types

def Initize():
    pass

class Center():
    def __init__(self, Import, Receiver):
        if Receiver is __path__:
            self.Script = Loader.RetreievFromPath(Receiver)
        else:
            self.Script = Loader.RetreiveScript(Receiver)

        if Import is __path__:
            self.Import = Loader.RetreievFromPath(Import)
        else:
            self.Import = Loader.RetreiveScript(Import)

        self.Handler = Handler(self.Import, self.Script)
        
class Loader():
    
    @staticmethod 
    def RetreiveScript(Target):
        FoundModule = [] 
        for Tar in Target:
            Found = importlib.import_module(Tar)
            if not Found ==  None:
               FoundModule.append(Found) 

        return FoundModule
    
    @staticmethod 
    def RetreievFromPath(TargetPath, Prefix=None):
        Target = []
        Path = [TargetPath] if isinstance(TargetPath, str) else TargetPath

        for _, ModName, _ in pkgutil.iter_modules(Path):
            FullName = f"{Prefix}{ModName}" if not Prefix == None else ModName

            Target.append(FullName)

        Loader.RetreiveScript(Target)

    @staticmethod 
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



class Modifier:
    @staticmethod

    def Applied(ModInfo):
        ModInfo   

    def Delete():
        pass


class Handler():

    def __init__(self, Import, Receiver):
        self.AllImport = Import
        self.Receiver = Receiver
         
    # Different Target for the same  
    def TargetImport(self, Target):
        self.FoundImport = Loader.SearchingTarget(self.AllImport, Target)

    def Connection(self, Yesno, Target=None):
        self.FoundImport = Loader.SearchingTarget(self.AllImport, Target)
        for Receiver in self.Receiver: 
            for Import in self.FoundImport:
                if not hasattr(Receiver, f"{Import}"):  
                    setattr(Receiver, f"{Import}", Import)
                elif not Yesno:
                    if hasattr(Receiver, f"{Import}"):
                        delattr(Receiver, f"{Import}")
       
 
    def Modification(self, YesNo, TargetPart):
        for Im in self.FoundImport:
            for Tar, ModNeeded in TargetPart:
                if Tar == Im.name:
                    for Request in ModNeeded:
                        for ModName, ModInfo in self.Modification: 
                            if Request == ModName:
                                Modifier.Applied(ModInfo, Im)