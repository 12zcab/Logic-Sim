from modules.Data.DataHandler import *
from module.object import *

import json


class Exporter:
    # Export per SimBox
    def __init__(self, SimBox : SimBox, File, Name : str, Other):
        self.SimBox = SimBox
        self.Other = Other
        self.Name = Name
        self.JSon = File
        self.Handler = Handler()
        self.Backet = {}

    def Catch(self, File : json, Targets, Loop=None):
        # When Targets = "All", the functions will enter self-loop mode
        if Targets == "All":
            for Object in self.SimBox.__dict__:
                if getattr(Object, __dict__):
                    # If the Object still contains things if will self loop
                    self.Backet[getattr(Object, __name__)] = self.Catch(File, Object, True)
                else:
                    self.Backet[getattr(Object, __name__)] = Object
            return
        # Normal usage and including path by path function
        if not Loop:
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
                    print(f"Target can not be found, final reach is {Found}")
        # Outside of the "All", self loop can be used outside of it however the function of path by path is lost
        if Loop:
            for Object in Targets.__dict__:
                if getattr(Object, __dict__):
                    self.Backet[getattr(Object, __name__)] = self.Catch(File, Object, True)
                else:  
                    self.Backet[getattr(Object, __name__)] = Object

    def Store(self):
        self.Handler.Backet = self.Backet
        if self.Handler.Store(self.JSon):
            self.Backet = {}

class Importer:
    def __init__(self, SimBox : SimBox):
        self.SimBox = SimBox

    def Import(self, Data):
        for Keys, Value in Data:
            Found = 0
            Final = True
            for Key in Keys:
                if Found == 0:
                    Found = SimBox.__dict__[Key]
                    continue
                Found = getattr(Found, Key)

                if not Found:
                    print(f"Target can not be found, final reach is {Found}")
                    Final = False
            if Final:
                Found = Value