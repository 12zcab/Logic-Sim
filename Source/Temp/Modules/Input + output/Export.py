from core.object import *
from modules import *
from Data import DataHandler
import os
import json


 
class Exporter:
    def __init__(self, items, filename):
        self.items = items
        self.filename = filename
 
    def ExportSimbox(self, ExportSimbox):
        SimBoxData = {
            "Conponets" : [],
            "Nets" : []
        }

        for object in ExportSimbox.Objects:
            objectData = {
                "objectname" : object.name,
                "IOs" : {pinData : ioData for pinData, ioData in object.IOs.item()},
            }
            SimBoxData["Conponets"].append(objectData)

        for net in ExportSimbox.Nets:
            netData = {
                "Connected" : net.connected_net
            }
            SimBoxData["Nets"].append(netData)

        
        DataHandler.Store("ExportedSimBox", "ExportedData.JSON", ExportSimbox)
        

    



        
        
        
            

        




        
        

        

 
 
  

 
        
    