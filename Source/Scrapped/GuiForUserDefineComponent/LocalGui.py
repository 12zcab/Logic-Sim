import tkinter as tk
import Source.Scrapped.GuiForUserDefineComponent.ScriptDefiner as ScriptDefiner
import Source.Scrapped.GuiForUserDefineComponent.BlockDefiner as BlockDefiner
from gui.node.nodeEngine import *


# Use a comfirm or save to execute the beblow
# Maybe a different list for gate or transforming component into gate which is not acceptable traditinally lol

class BlocksGui:
    def __init__(self):
        pass

    def CreateGui(self, GraphInfo): 
        self.PinNumber = GraphInfo["Pins"].size()
        self.Logics = GraphInfo["Logics"]
        BlockDefiner.a 
   
    def CopyChosen(self):  
        pass 

    def DeleteChosen(self):   
        pass    

    def Create():    
        pass    

    def DeleteCreated():   
        pass 
    
class ScriptGui:    
  
    def __init__(self): 
        pass   
   
    def CreateGui(self):   
        pass
  
    def SendContent(self):
        pass