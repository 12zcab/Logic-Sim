from core.object import *
from modules import *
import os
import json


 
class Exporter:
    def __init__(self, items, filename):
        self.items = items
        self.filename = filename
 
    def ExportObject(self, Simbox):
        SimBoxData = {
            "Conponets" : [],
            "Nets" : []
        }
        
        try:
            with open(self.filename, "x") as file:
                self.file = file
        except FileNotFoundError:
            self.file = os.makedirs(self.filename, exist_ok=True)


        for key1, value1 in (SimBox.Objects):
            SimBoxData["Conponets"][key1] = value1

        for key2, value2 in (SimBox.Nets):
            SimBoxData["Nets"][key2] = value2

        json.dump(SimBoxData, self.file, indent=4)
    



        
        
        
            

        




        
        

        

 
 
  

 
        
    