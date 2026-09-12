import json
import os

class Store:
    def __init__(self, tableName, filename, data):
        self.data = data
        self.Filename = filename
        self.tableName = tableName

    def DataStore(self):

        self.File = Loader.FileSearcher(self.Filename)

        if not self.File:
            self.File = ConditionHandle.FileNotFound(self.File)
        self.Loaded= json.load(self.File)

        if not Loader.TableSearcher(self.Loaded, self.tableName):
            self.Table = ConditionHandle.TableNotFound(self.Table)
        self.Table.update(self.data)

        if ConditionHandle.Checking(self.Table, self.Data):
            json.dump(self.Table, self.File, indent=4)
        else:
            return print("Data unsuccessful")

        
class ConditionHandle:
    def Checking(Ori, DataForChecking):

        for key1, value1 in Ori:
                for key2, value2 in DataForChecking:
                    if key1 == key2:
                        if not value1 == value2:
                            return False
                        else:
                            return True
        
    def FileNotFound(Filename, type):
        if type == "Store":
            return os.makedirs(os.path.join("Temp"/"Data", Filename), exist_ok=True) 

        if type == "Retrieve":
            for i in range(5):
                File = Loader.FileSearcher(Filename)
                if not File:
                    return False
                else:
                    return File + print("Error Solved")
       
    def TableNotFound(File, TableName, type):
        if type == "Store":
            return {}

    def VarNotFound(TableName, type): 
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
        for key1, value1 in Table:
            for key2, _ in Keys:
                if key1 == key2:
                    return value1
                else:
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
            if not ConditionHandle.FileNotFound():
                return print("Data Retrieve Failed")
        self.Data = json.load(self.File)

        self.Table = Loader.TableSearcher(self.Data, self.tableName)
        if not self.Table:
            if not ConditionHandle.TableNotFound():
                return print("Data Retrieve Failed")

        for key1, value in self.Table:
            for key2, _ in self.keys:
                if key1 == key2:
                    self.RetrievedData[key1] = value
                else:
                    self.Report = ConditionHandle.VarNotFound()

        return self.RetrievedData
                    