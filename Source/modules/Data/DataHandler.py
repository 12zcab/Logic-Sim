import os
import json
from pathlib import Path

class Loader:

    @staticmethod
    def GetData(FileName, TableName):
        FoundTable = []
        File = Loader.GetFile(FileName)
        Items = json.load(File)

        for item in Items:
            if isinstance(item, dict) or isinstance(item, list):
                if str(item.__name__) == TableName:
                    FoundTable.append(FoundTable)

    @staticmethod
    def GetFile(FileName):
        FilePath = Loader.FindPath(FileName)
        if not os.path.exists(FilePath):
            with open(FilePath, "w") as f:
                File = f

        if File == None:
            with open(FilePath, "r") as f:
              File = f

    @staticmethod
    def FindPath(Name : str):
        FullName = f"{Name}.json"
        for path in Path(".").rglob(FullName):
            if not path.absolute():
                return None
            else:
                return path.absolute()

class Handler:

    def __init__(self):
        self.Backet = []


    def Store(self , Filename: str):
        if not isinstance(self.Backet, list) and not isinstance(self.Backet, dict):
            Table = [self.Backet]
        setattr(Loader.GetFile(Filename), Table)

        
    def Retreive(TableName, Filename : str):
        return Loader.GetData(Filename, TableName)
