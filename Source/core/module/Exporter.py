from modules.Data.DataHandler import *
from module.object import *
import json

Class = []

class Exporter:
    # Export per SimBox
    def __init__(self, SimBox : SimBox, File, Name : str, Other):
        self.SimBox = SimBox
        self.Other = Other
        self.Name = Name
        self.JSon = File
        self.Handler = Handler()
        self.Backet = {}

    def Catch(self, Targets, Loop=None):
        # When Targets = "All", the functions will enter self-loop mode
        if Targets == "All":
            for Object in self.SimBox.__dict__:
                if getattr(Object, __dict__):
                    # If the Object still contains things if will self loop
                    self.Backet[getattr(Object, __name__)] = self.Catch(Object, True)
                else:
                    self.Backet[getattr(Object, __name__)] = Object
            return
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
        # Outside of the "All", self loop can be used outside of it however the function of path by path is lost
        if Loop:
            for Object in Targets.__dict__:
                if getattr(Object, __dict__):
                    self.Backet[getattr(Object, __name__)] = self.Catch(Object, True)  
                else:  
                    self.Backet[getattr(Object, __name__)] = Object

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
                        if not getattr(self.SimBox, Key):
                          print(f"{Key} : No Found, creating {Key}")

                        setattr(self.SimBox, Key, Value)
                          

        if Table == "All":
            PriObj = getattr(self.SimBox, globals()[next(iter(Table))])
            for Object in Table:  
                if getattr(self.SimBox.__dict__, Object):
                   setattr(PriObj, getattr(Object, __name__), self.Import(Object, True))
                else:
                   setattr(PriObj, Object.__name__, Object)
  
            return PriObj

        if Loop == True:
            for Object in Table:
                PriObj = getattr(self.SimBox, globals()[next(iter(Table))])
                if getattr(self.SimBox.__dict__, Object):
                   setattr(PriObj, getattr(Object, __name__), self.Import(Object, True))
                else:
                   setattr(PriObj, Object.__name__, Object)