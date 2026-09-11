
import json
import os

class Store:
    def __init__(self, tableName, filename, **kwargs):
        self.data = kwargs
        self.Filename = filename
        self.tableName = tableName


    def DataStore(self):
        self.File = Loader.FileSearcher(self.Filename)
        if self.File == False:
            ConditionHandle.FileNotFound(self.File, self.tableName)

        



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

    def TableSearcher(File, Table):
        try:
            if File.get(Table):
                return File.get(Table)
        except not File.get(Table):
            return False



    def ValueSearcher(Table, Keys):

        TotalData = {}

        try:
            for key1, value1 in Table:
                for key2, _ in Keys:
                    if key1 == key2:
                        TotalData[key2] = value1
                    else
                        

        except





    

        




 

class Retreiver: 
    def __init__(self, table, key, filename):
        self.table = table
        self.key = key
        self.filename = filename

    def WorkFlower(self):
        return
    


    

    def DataRetrieve(self):
        return


    
        
    



