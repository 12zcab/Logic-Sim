from core.object import *
from Data import *
from MutanterFile import Mutanter

Handler = Mutanter.Handler()

Handler.Connect({})

     
class State(SimBox):
     def __init__(self):
          self.VerLog = ChangeLog().Log
          self.FFLog = ChangeLog().Log

     def UpdateVerilog():
          pass

     def UpdateFlipFlop():
          pass


class ChangeLog:
     def __init__(self):
          self.Log = {}

     def StoreLog():
          pass

     def DeleteLog():
          pass





          