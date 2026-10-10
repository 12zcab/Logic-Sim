from core.object import *
from Data import *
from MutanterFile import Mutanter
from Verilog import *
from LogicGate import *
from SimpleCLIIO import *
from DataLogger import *
from Data import DataHandler

# Collect the state of Component wanted for prediction (all will be better)
# Recommend per SimBox but your choice
class ComponentState(Component):
     def __init__(self, Comp):
          self.ConnectNet = {}
          self.IOValue = {}
          if not Comp.Name == "Logger" or not Comp["Name"] == "Logger":
               print("Need Logger")
               return
          if not isinstance(Comp, Component):
               self.Logger = super.__init__(Comp["Name"], Comp["IOArray"], Comp["UpdateFunctions"])
          else:
               self.Logger = Comp
          
     def UpdateRecord(self, Component):
          ComponentData = self.Logger.update()
          for Io in ComponentData["IOs"]:
               self.IOValue[Io.name] = Io
          for Net in ComponentData["Net"]:
               self.ConnectNet[str(Net)] = Net


     def Retreive(self, Component):
          if not isinstance(Component, ComponentState):
               print("Needed to create A OBJECT FOR COMP")
          Data = {self.ConnectComp, self.IOValue}
          return Data


# SimBoxState
class SimBoxState(SimBox): 

     def __init__(self, Box):
          if not isinstance(Box, SimBox):
               Box = super.__init__(self, Box["Objects"], Box["Nets"])

          # Init the set up of collecting the data of the component in a Simbox
          for Component in Box:
               State = ComponentState(Component)
               if State.UpdateRecord(Component):
                  ComponentData = State.Retreive(Component)
                
               if ComponentData:
                    self.BoxData[Component.name] = ComponentData

          self.ComponentLog = {}
          self.NetLog =  {}
          self.Data = ChangeLog(f"{SimBox} : {self.CurrentNumber}")
          self.CurrentNumber = 1 
        
     def UpdateObjects(self, Box):
         if not isinstance(Box, SimBox):  
            print("Require a simbox")
            return 
              
         for Component in Box["Objects"]:

              ComponentUpdate = ComponentState(Component).UpdateRecord(Component)
              if ComponentUpdate:
                  ComponentData = ComponentState(Component).Retreive(Component)
              self.ComponentLog[Component.name] == ComponentData


     def UpdateNets(self, Box):
         if not isinstance(Box, SimBox): 
            print("Require a simbox")
            return

         for Net in Box["Nets"]:
               self.ObjectLog[Net.name] = Net


class ChangeLog:
     def __init__(self, TableName):
          f"{TableName}" = {}

          self.Handler = DataHandler.Handler()

     def StoreLog(self):
          self.Handler.Store("History.JSON")
  
     def DeleteLog(self):
          self.Log = None
          self = None