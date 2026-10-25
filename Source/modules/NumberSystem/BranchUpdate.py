from core.module.object import *
from modules.Data import *
import random
# A calculation of result outside of normal true/false
# Besides Strength cancel each other, this may also include a new combination

SystemTable = []

class CombineIO:
    # this is for designing a combination results
    def __init__(self):
        self.Condition = {}
        self.Changes = {}
    
    # This is for normal one
    def InitCon(self, Component : Component , Conditions, Changes):
        for Object, Value in Conditions:
            if not Component.IO[Object]:
                print("Pin does not exist") 
            self.Condition[IO] = Value

        for InObject, ChangeInfo in Changes:  
            for DeObject, Value in ChangeInfo:
                self.Changes[DeObject] = Value

        return self.Condition and self.Changes 

    def UpdateCon(self, Table, Changes):
        Table = CombineIO.__dict__.items(Table)  
        if not Table:
            return print(f"{Table} does not exist in the system")
        for Var, Change in Changes:
            if Table[Var]: 
                Table[Var] = Change  

    def Execute(self, States):   
        # Ignore the strength 
        NewState = {}
        for InObject, Value in States:
            if Value == self.Condition[InObject]:
                for DeObject, Value in self.Changes[InObject]:  
                    NewState[DeObject] = Value

        return NewState
  
class NumberSystem:
    # Different State combined with strength or factor decided by user tranform as number in a range also decided by user
    # Differnt Number of the range representation can be decided by user for effects
    # the number result can be re-combined for CombineIO  

    # "Object" = {"1-12", [Var = {[4-12], "True" = "4-6", "False" = ""}

    def __init__(self, Object : object.__class__.__self__, CombineIO : CombineIO):
        SystemTable.append(self)
        self.CombineIO = CombineIO
        self.Object = Object
        self.Logics = {}

    def InitLogic(self, Logic : dict):
        for Var, Info in Logic:  
            if Var == "NumberSystem":
                self.Logics[Var] = Info
                continue
            if getattr(self.Object, Var):
               self.Logics[Var] = Info

    def UpdateLogic(self, Table , Info):
        Table = NumberSystem.__dict__.items(Table)
        if Table == None:  
            return print("Table is incorrect")  
        for Var, Value in Info:  
            Table[Var] = Value  
   
    def Execute(self, States):
        ExeLog = {"Old" : States}
        NewValue = {}
        for Var, Value in States:  
            Range = [] 
            for Value in self.Logics[Var][str(Value)]:
                if "-" in Value:
                    Range1, Range2 = map(int, str.split(Value, "-"))
                    Range.append(random.randint(Range1, Range2))    
                else:
                    Range.append(Value)  

                NewValue[Var] = random.choice(Range)  
          
        NewState = self.CombineIO.Execute(NewValue)

        if self.CombineIO.Execute(NewValue):
            ExeLog["New"] = NewState  
   
# Still try to figure out

# If statement = false , premise = true and conclusion = false

# if person is a sun, premise = true, true, premise = false, false