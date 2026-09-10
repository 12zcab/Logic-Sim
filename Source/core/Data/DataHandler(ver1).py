
import json
import os

class Store:
    def __init__(self, tableName, **kwargs):
        self.data = kwargs
        self.tableName = tableName

    def DataProcessing(self):
        try:
            with open(self.filename, "r") as file:
                self.File = json.load(file)
                try:
                    if self.table == self.File.get(self.tableName):
                        print("Found")
                except self.table == False:
                    self.table = {}

        except FileNotFoundError or json.JSONDecodeError:
            self.File = open(self.filename, "x").close()
            self.table = {}

    def DataStore(self):
        for key, values in self.data.items():
            self.table[key] = values


        with open(self.filename, "w") as file:
            json.dump(self.File, file, indent=4)




class Retreiver: 
    def __init__(self, table, key):
        self.table = table
        self.key = key

    def RetreiveProcessing(self):
        self.file = 

    


    def DataRetrieve(self):


    
        
    



