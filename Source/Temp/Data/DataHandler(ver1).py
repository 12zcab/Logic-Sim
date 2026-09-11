
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

        self.Table = Loader.TableSearcher(self.File, self.tableName)
        if not self.Table:
            ConditionHandle.TableNotFound(self.Table)



        



class ConditionHandle:

    def Checking(self):
        return
        
    def FileNotFound(self):
        return

    def TableNotFound(self):
        return
        


class Loader:    

    def FileSearcher(Filename):
        try:
            with open(Filename, "x") as file:
                return file

        except FileNotFoundError or json.JSONDecodeError:
            return False

    def TableSearcher(File, TableName):
        try:
            if File.get(TableName):
                return File.get(TableName)
        except not File.get(TableName):
            return False



    def ValueSearcher(Table, Keys):
        Success = True
        TotalData = {}


        try:
            for key1, value1 in Table:
                for key2, _ in Keys:
                    if key1 == key2:
                        TotalData[key2] = value1
                    else:
                        Success = False
                        
        except not Success:
            return False

 

class Retreiver: 
    def __init__(self, table, key, filename):
        self.table = table
        self.key = key
        self.filename = filename

    def WorkFlower(self):
        return
    


    

    def DataRetrieve(self):
        return


    
        
    



