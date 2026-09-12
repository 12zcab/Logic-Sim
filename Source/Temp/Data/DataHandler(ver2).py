import json
import os

class Store:
    def __init__(self, tableName, filename, **kwargs):
        self.data = kwargs
        self.Filename = filename
        self.tableName = tableName

    def DataStore(self):
        self.File = Loader.FileSearcher(self.Filename)
        if not self.File:
            ConditionHandle.FileNotFound(self.File)
        self.data = json.load(self.File)

        self.Table = Loader.TableSearcher(self.data, self.tableName)
        if not self.Table:
            ConditionHandle.TableNotFound(self.Table)

        for key, value in self.data.items():
            self.Table[key] = value

        json.dump(self.Table, self.File, indent=4)

        
class ConditionHandle:

    def Checking(self):
        return
        
    def FileNotFound(self):
        return

    def TableNotFound(self):
        return

    def VarNotFound(self):
        pass
        


class Loader:

    def FileSearcher(Filename):
        try:
            with open(Filename, "x") as file:
                return file

        except FileNotFoundError or json.JSONDecodeError:
            return False
        

    def TableSearcher(Data, TableName):
        try:
            if Data.get(TableName):
                return Data.get(TableName)
        except not Data.get(TableName):
            return False


    def ValueSearcher(Table, Keys):
        TotalData = {}
        try:
            for key1, value1 in Table:
                for key2, _ in Keys:
                    if key1 == key2:
                        TotalData[key2] = value1
                        Success = True
                    else:
                        Success = False
        except not Success:
            return False

 

class Retreiver: 
    def __init__(self, tableName, key, filename):
        self.tableName = tableName
        self.keys = key
        self.filename = filename 

    def DataRetrieve(self):

        self.RetrievedData = {}

        self.File = Loader.FileSearcher(self.filename)
        if not self.File:
            ConditionHandle.FileNotFound
        self.Data = json.load(self.File)

        self.Table = Loader.TableSearcher(self.Data, self.tableName)
        if not self.Table:
            ConditionHandle.TableNotFound()

        for key1, value in self.Table:
            for key2, _ in self.keys:
                if key1 == key2:
                    self.RetrievedData[key1] = value
                else:
                    self.Report = ConditionHandle.VarNotFound()

        return self.RetrievedData
                    
                
                    






    
        
    



