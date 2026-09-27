import os
import json
from Data import *


class TableHandle(dict):
    
    def __getattr__(self, Name):
        if Name in self:
            return self[Name]
        raise AttributeError(f"'TableHandle' object has no attribute '{Name}'")
    
    def __setattr__(self, Name, Value):
        self[Name] = Value

    def __delattr__(self, Name):
        if Name in self:
            del self[Name]
        else:
            raise AttributeError(f"'TableHandle' object has no attribute '{Name}'")
                 

class Loader:
    @staticmethod
    def gettable(f, t):
        Assets = Loader.getfile(f)
        Handler = TableHandle(Assets)
        
        Table = Handler.get(t)
        if not Table:
            Table = {}
        return Table 
    
    @staticmethod
    def getfile(f):
        if not os.path.exists(f) or os.path.getsize(f) == 0:
            print("New file has been created") 
            with open(f, "w") as file:
                json.dump({}, file)
            return {}
            
        with open(f, "r") as file:
            return json.load(file)

        
class FileHandle:

    @staticmethod
    def export(f, t, d):
        Handler = DataHandle(f, t, d)
        Handler.getstore()


class DataHandle:

    def __init__(self, file, table, data):
        self.filename = file
        self.data = data 
        self.filedata = Loader.getfile(file)
        self.tablename = table
        self.table = Loader.gettable(file, table)

    def getstore(self): 
        if not isinstance(self.data, dict):
            raise TypeError("Data is not a dict")
 
        if self.tablename not in self.filedata:
            self.filedata[self.tablename] = {}
            
        for key, value in self.data.items():  
            self.filedata[self.tablename][key] = value 

        with open(self.filename, "w") as file:
            json.dump(self.filedata, file, indent=4)      

    def getRetreive(self):
        self.RetrievedData = {}
        if not self.table: 
            return self.RetrievedData
            
        for name in self.data:
            value = self.table.get(name)
            self.RetrievedData[name] = value
 
        return self.RetrievedData  



    
        
    



