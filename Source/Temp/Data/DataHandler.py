import json
from Data import *


class TableHandle(dict):
    
    def __getattr__(self, Name):
        if Name in self:
            return self[Name]
        raise AttributeError(f"'BetterDict' object has no attribute '{Name}'")
    
    def __setattr__(self,Name,Value):
        self[Name] = [Value]

    def __delattr__(self,Name):
        if Name in self:
            del self[Name]
        else:
            raise AttributeError(f"'BetterDict' object has no attribute '{Name}'")
                

class Loader:
    def gettable(f, t):
        Assets = Loader.getfile(f)
        Handler = TableHandle(Assets)
        return Handler[t]
    
    def getfile(file):
        return json.load(file) if json.JSONDecodeError or FileNotFoundError else False

        
class FileHandle:
    def export(file, data):
        if not Loader.getfile(file):
            pass
             
class DataHandle:

    def __init__(self, file, table, data):
        self.data = data 
        self.file = Loader.getfile(file)
        self.table = Loader.gettable(self.file, table)

    def getstore(self):
        if not self.table: raise AttributeError("Table is not found")
        for key, value in self.data:  
            self.table[key] = value 
        json.dump(self.table, self.file)       

    def getRetreive(self):
        self.RetrievedData = {}
        if not self.table: return self.RetrievedData
        for name in self.data:
            value = self.table[name]
            self.RetrievedData[name] = value if value == None else self.RetrievedData[name] = None

        return self.RetrievedData                 



    
        
    



