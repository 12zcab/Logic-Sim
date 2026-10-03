# Since the old version is too shit and anti human, i want to create a whole new version. Bruh
# On top of that, the old one is hard to track (The main issue) while having heavy security issue 
# I have searched the better way to make the structure ( Ai + YT video )
# Son, this thing can self destruct


from Temp.Data import DataHandler
import importlib
import pkgutil
import logging
import types
from typing import *


logging.basicConfig(level=logging.INFO)


class Loader:
    @staticmethod
    def LoadModule(TargetName):

        #Return Tables
        FoundItems = []

        for Target in TargetName:
            try:
                Found = importlib.import_module(Target)
                FoundItems.append(Found)
            except ImportError as e:
                print(f"{Target}" " does not exist due to" f"{e}")

        return FoundItems  

    @staticmethod
    def LoadFromPath(TargetPaths , prefix : str = ""):

        # Return Table
        FoundItems = []

        for _, modname, _ in pkgutil.iter_importers(TargetPaths):
            Target = f"{prefix}{modname}"
            try:
               FoundItems.append(importlib.import_module(Target))
            except ImportError as e:
                print(f"{Target}" " does not exist due to" f"{e}")
        return FoundItems
    
    @staticmethod
    def CloneImport(TargetImport):
        # Return table
        Clone = []
        Imports = Loader.LoadModule(TargetImport)
        
        for Import in Imports:
            if Import == None:
                continue

            CloneImport = types.ModuleType(f"{Import}")
            setattr(CloneImport, "__name__", str(f"Copy_{Import}"))

            for key, value in Import.__dict__.items():
               if not key == "__name__" or "__loader__" or "__spec__" or "__file__" or "__cached__":
                   setattr(Import, key, value)

            Clone.append(CloneImport)

        return Clone





class Modifier:
    @staticmethod
    def ApplyAttr(TargetModule, Modinfo : any):
        #one by one
        SuccessChanges = []

        try:
            Import = Loader.LoadModule(TargetModule)
        except ImportError as e:
            print(f"{e}")
            return SuccessChanges == None


        Name = getattr(Import, "__name__")

        for ModPart, Mod in Modinfo:
            if  not isinstance(Mod, str):
                setattr(Import, str(ModPart), Mod)
                logging.info(f"{ModPart} has been replaced")
                SuccessChanges.append(f"{Mod} has been changed")
            elif isinstance(Mod, str):
                try:
                   Compile = compile(Mod)
                   exec(Compile, Import.__dict__)
                   logging.info(f"{ModPart} has been compiled and attached to the {Name}")
                   SuccessChanges.append(Mod)
                except Exception as e:
                    logging.info(f" Bruh {ModPart} is shitted inserted black man disappeared")
            else:
                setattr(Import, ModPart, Mod)

        return SuccessChanges
   

    @staticmethod
    def DeleteAttr(TargetImport,  AttrNames):
        # One by one

        SuccessChanges = []

        try:
            Import = Loader.LoadModule(TargetImport)
        except ImportError as e:
            logging.info(f"{e} this shit has appeared as {TargetImport} is not a thing, try harder son")
  
        for AttrName in AttrNames:
            if getattr(Import, AttrName):
               delattr(Import, AttrName)
               logging.info(f"{AttrName} is deleted")
               SuccessChanges.append(f"{AttrName} is deleted")

        return Import


class Handler:

    print("This is more automatic but u can still use manually if u are cool")
    # Handler store the log of the past things so no worry, easy things u know but this is a fixed way, however since u can change this importer, maybe u can do CoolStuff

    def __init__(self):
        self.DataHandler = DataHandler.Handler()
        self.ConLog = {}
        self.ChangeLog = {}
        self.CloneLog = []
        # History per Handler

    def Connect(self, Info):
        for Target, Imports in Info:
            for Import in Imports:
                Found = Loader.LoadModule(Target)
                if not getattr(Found, Import): 
                    setattr(Found, Import, Loader.LoadModule(Import))
                    if not self.ConLog[f"{Found.__name__}"]:
                        self.ConLog[f"{Found.__name__}"] = [Import.__name__]
                    else:
                        self.ConLog[f"{Found.__name__}"].append(Import.__name__)
                else:
                    print("No need from Connect")
    

    def Disconnect(self, List):
        for Target, Imports in List:
            for Import in Imports:
                Found = Loader.LoadModule(Target)[0]
                if not getattr(Found, Import):
                    delattr(Found, Import)
                    if self.ConLog[f"{Found.__name__}"]:
                        self.ConLog[f"{Found.__name__}"].remove(Import.__name__)
                else: 
                    print("No need from Disconnect")
                
    def ApplyAttr(self, AttrInfos, TargetScripts : dict = None):
        for ModuleName, AttrInfo in AttrInfos:
            if not TargetScripts == None:

                Clone = Loader.CloneImport(ModuleName, f"Clone_{ModuleName}")[0]
                SuccessChanges = Modifier.ApplyAttr(Clone, AttrInfo)

                Handler.LogChanges(self.Handler, self.CloneLog, Clone)
                Handler.LogChanges(self.Handler, self.ChangeLog, Clone, SuccessChanges)

                for Target in TargetScripts:
                    Found = Loader.LoadModule(Target)
                    setattr(Found, Clone.__name__ , Clone)

                    Handler.LogChanges(self.Handler, self.ConLog, Found.__name__, Clone.__name__)   
            else:

                SuccessChanges = Modifier.ApplyAttr(ModuleName, AttrInfo)
            
                Handler.LogChanges(self.Handler, self.ChangeLog, ModuleName, SuccessChanges)
            

    def DeleteAttr(self, AttrInfos):
        for ModuleName, AttrInfo in AttrInfos:
            SuccessChange = Modifier.DeleteAttr(ModuleName, AttrInfo)
            Handler.LogChanges(self.Handler, self.ChangeLog, ModuleName, SuccessChange)
            

    def Revert(self, RevertInfo):
        if not isinstance(RevertInfo, dict):
            Info = {RevertInfo}
        Info = RevertInfo
        for Target, ImportList in Info:
            Target = Loader.LoadModule(Target)
            for ImportName in ImportList:
                CopyName = f"Clone_{ImportName}"
                delattr(Target, CopyName) if getattr(Target, CopyName) else print("Revert is not required")

    def GarbageCollect(self):

        NotAttach = []
        for Clone in self.CloneLog:
            for _, Cons in self.ConLog:
                if not Cons[f"{Clone}"]:
                    NotAttach.append(Clone)

        for Clone in NotAttach:
            del(Clone)

    def LogChanges(self, Table, Value, key=None):

        if isinstance(Table, dict) and key == None:
            return print("Key is required")

        if Value == None:
            return print("Changes may have failed")

        if Table == self.ConLog or self.ChangeLog:
            if not Table[key]:
                Table[key] = [Value]
            else:
                Table[key].append(Value)
                self.DataHandler.Backet(Table)

                if self.ConLog:
                   self.DataHandler.Store("ChangeLog")
                else:
                    self.DataHandler.Store("ConLog")

        if Table == self.CloneLog:
            if not Table[Value]:
                Table.append(Value)
                self.DataHandler.Backet(Table)
                self.DataHandler.Store("CloneLog")


# Data store for logs
 
    