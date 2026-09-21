from .enum import *
from .BetterDict import *
from .chronos import *

class IO:
    def __init__(self, Name, parentComponent=None):
        self.Name = Name
        self.parent = parentComponent
        self.Net = None
        self.driveVal = Logic.X
        self.driveStr = Strength.HIGHZ
        self.Value = Logic.X
        default_net = Net()
        default_net.add(self)

    def setPower(self, val, strength=Strength.STRONG, Delay=0, SimBox=None):
        if SimBox and hasattr(SimBox, "scheduler"):
            SimBox.scheduler.schedule(self, val, strength, Delay)
        else:
            self.driveVal = val
            self.driveStr = strength
            if self.Net:
                self.Net.resolve()

    def __rshift__(self, other):
        if isinstance(other, IO):
            self.connect(other)
            return other
        if isinstance(other, Net):
            self.connectNet(other)
            return None
        raise TypeError(f"Cannot connect IO to {type(other)}")
    def connectNet(self, net):
        if self.Net:
            self.disconnectNet()
        self.Net = net
        net.add(self)
    def disconnectNet(self):
        if self.Net:
            self.Net.remove(self)
            newNet = Net()
            self.Net = newNet
            newNet.add(self)
    def connect(self, subject):
        if self.Net and subject.Net:
            if self.Net != subject.Net:
                self.Net.mergeNets(subject.Net)
        elif self.Net:
            subject.connectNet(self.Net)
        elif subject.Net:
            self.connectNet(subject.Net)
        else:
            newNet = Net()
            self.connectNet(newNet)
            subject.connectNet(newNet)
class Net:
    def __init__(self, Name=None):
        self.IO = []
        self.Name = Name if Name else f"Net_{id(self)}"
        self._Value = Logic.Z
        self._Strength = Strength.HIGHZ
    def add(self, io):
        if io not in self.IO:
            self.IO.append(io)
            io.Net = self
    def remove(self, io):
        if io in self.IO:
            self.IO.remove(io)
    def resolve(self):
        if not self.IO:
            self._Value = Logic.Z
            self._Strength = Strength.HIGHZ
            return False
        maxStr = max(io.driveStr for io in self.IO)
        if maxStr == Strength.HIGHZ:
            newVal = Logic.Z
        else:
            maxDriver = [io.driveVal for io in self.IO if io.driveStr == maxStr]
            firstVal = maxDriver[0]
            newVal = firstVal if all(v == firstVal for v in maxDriver) else Logic.X
        valChanged = (self._Value != newVal)
        self._Value = newVal
        self._Strength = maxStr
        for io in self.IO:
            io.Value = newVal
        return valChanged
    def prepareDelete(self):
        for io in list(self.IO):
            io.Net = None
        self.IO.clear()
    def mergeNets(self, subject):
        if subject == self:
            return
        for io in list(subject.IO):
            self.add(io)
            io.Net = self
        subject.IO.clear()
        destroyNet(subject)
def destroyNet(net):
    if net:
        net.prepareDelete()
class Component:
    def __init__(self, Name, IOArray, updateFunction):
        self.Name = Name
        self.IO = BetterDict(IOArray) if isinstance(IOArray, dict) else BetterDict({io.Name: io for io in IOArray})
        self.updateFunction = updateFunction
        for io in self.IO.values():
            io.parent = self
    def update(self, SimBox=None):
        if self.updateFunction:
            self.updateFunction(self, SimBox)
    def getNet(self):
        NetArray = []
        for io in self.IO.values():
            if io.Net is not None and io.Net not in NetArray:
                NetArray.append(io.Net)
        return NetArray

class SimBox:
    def __init__(self, Objects,MAX_DELTA_CYCLES = 30):
        self.Objects = Objects
        self.Nets = []
        self.scheduler = Kairos()
        self.MAX_DELTA_CYCLES = MAX_DELTA_CYCLES
    def addObject(self,obj):
        self.Objects.append(obj)
    def expandNet(self):
        newNets = []
        for obj in self.Objects:
            for net in obj.getNet():
                if net is not None and net not in newNets:
                    newNets.append(net)
        self.Nets = newNets
    def init(self, mode="random"):
        self.expandNet()
        for net in self.Nets:
            initVal = Logic.ZERO
            net._Value = initVal
            for io in net.IO:
                io.Value = initVal
        for obj in self.Objects:
            obj.update(SimBox=self)
    def stepDeltaLoop(self):
        while self.scheduler.hasCurrentEvent():
            next_delta = min(self.scheduler.queue[self.scheduler.currentTime].keys())
            if next_delta > self.MAX_DELTA_CYCLES:
                print(f"[WARNING] Delta Cycle exceeded limit!")
                self.scheduler.queue[self.scheduler.currentTime].clear()
                break
            events = self.scheduler.getNextEvent()
            affectedNets = set()
            for evt in events:
                evt.targetIO.driveVal = evt.Val
                evt.targetIO.driveStr = evt.Strength
                if evt.targetIO.Net:
                    affectedNets.add(evt.targetIO.Net)
            affectedComponent = set()
            for net in affectedNets:
                if net.resolve():
                    for io in net.IO:
                        if io.parent:
                            affectedComponent.add(io.parent)
            for comp in affectedComponent:
                comp.update(SimBox=self)