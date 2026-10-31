from modules.Data.DataHandler import *
from module.object import *
import json
import importlib

Class = []

class Exporter:
    # Export per SimBox
    def __init__(self, SimBox : SimBox, File, Name : str):
        self.SimBox = SimBox
        self.Name = Name
        self.JSon = File
        self.Handler = Handler()
        self.Backet = {}

    def Catch(self, Targets, Loop=None):
        # When Targets = "All", the functions will enter self-loop mode
        if Targets == "All" or Loop == None:
    
            for Object in self.SimBox.__dict__:
                if getattr(Object, __dict__):
                    # If the Object still contains things if will self loop
                    self.Backet[getattr(Object, __name__)] = self.Catch(Object, True)
                else:
                    if isinstance(Object, callable):
                        self.Backet[getattr(Object, "__qualname__")] = f"{Object.__module__}{Object.__qualname__}"
                    else:
                       self.Backet[getattr(Object, __name__)] = Object 
            return
        
        # Outside of the "All", self loop can be used outside of it however the function of path by path is lost
        if Loop:  
            for Object in Targets.__dict__:
                if getattr(Object, __dict__):  
                    self.Backet[getattr(Object, __name__)] = self.Catch(Object, True)  
                else:      
                    if isinstance(Object, callable):
                        self.Backet[getattr(Object, "__qualname__")] = f"{Object.__module__}.{Object.__qualname__}"
                    else:
                       self.Backet[getattr(Object, __name__)] = Object
        # Normal usage and including path by path function
        if not Loop == True:
            Found = 0
            Final = True
            for Target in Targets:  
                if Found == 0:
                    Found = getattr(SimBox.__dict__, Target)
                else:  
                    Found = getattr(Found, Target)
                if Found == None:
                    Final = False
              
                if not Final:
                    return print(f"Target can not be found, final reach is {Found}")

  
    def Store(self):  
        self.Handler.Backet = self.Backet
        if self.Handler.Store(self.JSon):
            self.Backet = {}

class Importer: 
    def __init__(self, FileName : json, TableName, SimBox):  
        self.File = FileName  
        self.SimBox = SimBox
        self.Table = TableName  

    def Import(self, Table, Loop = None):
        if isinstance(Table, dict) and Loop == None:
            for Key, Value in Table:
                Found = 0
                Final = True  
                for Path in Key:
                    if isinstance(Path, __dict__): 
                       Path = str(Path.__name__)
                    Found = getattr(self.SimBox.__dict__, Path)
                    if not Found:
                       Final = False  
                       return
                    
                if not Final:
                   return print(f"Object can only be traced back to {Found}")
                else:
                    for Key, Value in Value:
                        if not getattr(Found, Key):
                          print(f"{Key} : No Found, creating {Key}")

                        setattr(Found, Key, Value)
                            

        if Table == "All" or Loop == True:
            PriObj = getattr(self.SimBox, globals()[next(iter(Table))])

            for Key, Object in Table:
                if getattr(self.SimBox.__dict__, Object):
                   setattr(PriObj, Key, self.Import(Object, True))
                else:
                    if "." in Key:
                        Parts = Key.split(".")
                        for i in range(len(Parts), 0, -1):
                            ModulePath = ".".join(Parts[:i])
                            try:
                               module = importlib.import_module(ModulePath)
                               remain = Parts[i:]
                            except ModuleNotFoundError:
                               return

                            Found = False
                            for Part in remain:
                                if not Found:
                                    Found = getattr(module, Part)
                                    continue

                                Found = getattr(Found, Part)

                            Object = Found
                                   
                    setattr(PriObj, Key, Object)

            if Table == "All":
               return PriObj