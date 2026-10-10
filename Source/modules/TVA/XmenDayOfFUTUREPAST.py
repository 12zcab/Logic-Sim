from core.object import *
from Verilog import *
from LogicGate import *
from FlipFlop import *
from Snap import *
from Data.DataHandler import *
 
Handler = DataHandler()


class Mystery:


    @staticmethod
    def SetUpSimBox():
        pass
    
    @staticmethod
    def GetResult(self):
        #Create a simbox locally 
        self.Unbox = None

class History:
    @staticmethod
    def GetResult(Box : SimBox, Number : int):
        Data = Handler.Retreive("History.JSON", f"{Box}{Number}")
        if Data:
            return Data
        else:
            print("Retreive unsuccessful")
