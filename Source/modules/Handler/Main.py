from modules import *
from core.module.object import *
import json


# Current idea, Local custom Gui Handle for component
# Work Flow, WorkSpace > Box > Component, WorkSpace Execute the functions and workflow, Engine return the valurable changes


Default = [
    "Work1",
    "Work2",
    "Work3",
]

class WorkSpace:
    def __init__(self):
        self.BoxList = []

    def BridgeBox(BoxList : list[BoxObject]):
        for Box1 in BoxList:
            for Box2 in BoxList:
                if not Box2.PartnerBox[Box1]:
                    Box2.PartnerBox[Box1]
        # I guess a special line between boxes while the boxes remain seperate
        
    def GhostResult(self, BoxInfo : list, Box2Info : list = None ):
        with open("History.JSON", "r") as Read:
            Data = json.load(Read)
            if Data.BoxInfo[1].BoxInfo[2].BoxInfo[3]:
                return Data.BoxInfo[1].BoxInfo[2]  

class ComponentInputter:
    def __init__(self, Component):
        self.Component = Component
        self.IOArray = self.Component.IO

    def ConnectGui(self, Special=None):
        if not isinstance(Special, list):
            Special = [Special]
        self.GuiSet = []
        for IO in self.Component.IO:
            if not Special[IO.name]:
               self.GuiSet.append(IO.name)

    def ConnnectReaction(self, List=Default):
        for IO in self.GuiSet:
            Connected = self.GuiSet.Connect(IO.UpdateFunction if IO.UpdateFunction else None)
            Component.WorkList = List
            if not Connected:
                print("Bruh IO Gui is bugged")


# Gui Engine Part
class InputReaction:
    def __init__(self, Input, WorkFlow=Default):
        self.Input = Input
        self.WorkFlow = WorkFlow

    def ExecuteWorkFlow(self, Step=None):
        if Step == None:  
            Step = 0
        if Step > self.WorkFlow.size():
            return
        Default[Step]
        Step += 1  
        self.ExecuteWorkFlow(Step)
  
    def TimeWaiting(self):
        pass    
    
        

class BoxObject:
    def __init__(self, SimBox : SimBox):
        self.SimBox = SimBox
        self.Parent = None
        self.Pots = {}

    def ConnectBoxToParent(self, Parent : WorkSpace):
        self.SimBox.Parent = Parent
        self.Parent.BoxList.append(self.SimBox)

    def SetPot(self, PotNumber, Position):
        for i in range(1, PotNumber):
            self.Pots(f"Pot{i}") = Component(f"Pot{i}", ["IO1"], self.ActivatePot())
            self.Pots(f"Pot{i}").On = False
            self.SimBox.addObject(self.Pots(f"Pot{i}"))
  
    def ConnectPot(self, Object : Component):
        for _, Pot in self.Pots:
            for PotIO in Pot.Net.IO:
                if not Object.Net.IO[PotIO.name]:
                    Object.Net.IO[PotIO.name]
        
    def ActivatePot(self, PotNumber):
        for _, Pot in self.Pots:
            if Pot.On == False:
                Pot.On = True