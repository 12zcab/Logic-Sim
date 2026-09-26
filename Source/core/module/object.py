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
        self._Value = Logic.X
        default_net = Net()
        default_net.add(self)

    @property
    def simBox(self):
        if self.parent:
            return self.parent.simBox
        return None
    @property
    def Value(self):
        return self._Value
    @Value.setter
    def Value(self,val, strength=Strength.STRONG, Delay=1):
        self.setPower(val, strength, Delay)
    def setPower(self, val, strength=Strength.STRONG, Delay=1):
        """Schedules events automatically on tracked SimBox without passing arguments."""
        sim = self.simBox
        if sim and hasattr(sim, "scheduler"):
            sim.scheduler.schedule(self, val, strength, Delay)
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
        if self.Net == net:
            if net and self not in net.IO:
                net.add(self)
            return
        if self.Net:
            self.Net.remove(self)
        self.Net = net
        if net:
            net.add(self)
    def disconnectNet(self):
        if self.Net:
            self.Net.remove(self)
            newNet = Net()
            self.Net = newNet
            newNet.add(self)
    def connect(self, subject):
        if not isinstance(subject, IO):
            raise TypeError(f"Cannot connect IO to {type(subject)}")
        if self is subject:
            return
        if self.Net is None:
            self.Net = Net()
        if self not in self.Net.IO:
            self.Net.add(self)
        if subject.Net is None:
            subject.Net = Net()
        if subject not in subject.Net.IO:
            subject.Net.add(subject)
        if self.Net != subject.Net:
            target_net = subject.Net
            self.Net.mergeNets(target_net)
            subject.connectNet(self.Net)
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
            io._Value = newVal

        return valChanged

    def prepareDelete(self):
        for io in list(self.IO):
            io.Net = None
        self.IO.clear()
    def mergeNets(self, target_net):
        if target_net is None or target_net == self:
            return
        for io in list(target_net.IO):
            io.Net = self
            if io not in self.IO:
                self.IO.append(io)
        target_net.IO.clear()
        self.resolve()

class Component:
    def __init__(self, Name, IOArray, updateFunction=None):
        self.Name = Name
        self.parent = None
        self.IO = BetterDict(IOArray) if isinstance(IOArray, dict) else BetterDict({io.Name: io for io in IOArray})
        self.updateFunction = updateFunction
        for io in self.IO.values():
            io.parent = self

    @property
    def simBox(self):
        if hasattr(self.parent, "simBox"):
            return self.parent.simBox
        return self.parent
    def update(self):
        if self.updateFunction:
            self.updateFunction(self)
    def getNet(self):
        NetArray = []
        for io in self.IO.values():
            if io.Net is not None and io.Net not in NetArray:
                NetArray.append(io.Net)
        return NetArray

class Module(Component):
    def __init__(self, Name, ModuleIO, InnerBlock):
        super().__init__(Name, ModuleIO, None)
        self.child = BetterDict(InnerBlock) if isinstance(InnerBlock, dict) else BetterDict({block.Name: block for block in InnerBlock})
        
        for block in self.child.values():
            block.parent = self
    def getNet(self):
        NetArray = []
        for io in self.IO.values():
            if io.Net is not None and io.Net not in NetArray:
                NetArray.append(io.Net)
        for block in self.child.values():
            for net in block.getNet():
                if net is not None and net not in NetArray:
                    NetArray.append(net)
        return NetArray
    def update(self):
        pass

class SimBox:
    def __init__(self, Objects, MAX_DELTA_CYCLES=30):
        self.Objects = []
        self.Nets = []
        self.scheduler = Kairos()
        self.MAX_DELTA_CYCLES = MAX_DELTA_CYCLES
        for obj in Objects:
            self.addObject(obj)
    def addObject(self, obj):
        obj.parent = self
        if obj not in self.Objects:
            self.Objects.append(obj)
    def expandNet(self):
        flat_objects = []
        flat_nets = []
        visited_nets = set()
        def flatten(comp, parent_node):
            comp.parent = parent_node
            
            if comp not in flat_objects:
                flat_objects.append(comp)
            for net in comp.getNet():
                if net is not None and net not in visited_nets:
                    visited_nets.add(net)
                    flat_nets.append(net)
            if hasattr(comp, "child"):
                for child_obj in comp.child.values():
                    flatten(child_obj, parent_node=comp)
        for obj in list(self.Objects):
            flatten(obj, parent_node=self)
        self.Objects = flat_objects
        self.Nets = flat_nets
    def init(self, mode="random"):
        self.expandNet()
        for net in self.Nets:
            initVal = Logic.ZERO
            net._Value = initVal
            for io in net.IO:
                io._Value = initVal
        for obj in self.Objects:
            obj.update()
    def stepDeltaLoop(self):
        while self.scheduler.hasCurrentEvent():
            next_delta = min(self.scheduler.queue[self.scheduler.currentTime].keys())
            if next_delta > self.MAX_DELTA_CYCLES:
                print(f"[WARNING] Delta Cycle exceeded limit!")
                self.scheduler.queue[self.scheduler.currentTime].clear()
                break
            events = self.scheduler.getNextEvent()
            affectedComponent = set()
            affectedNets = set()
            for evt in events:
                evt.targetIO.driveVal = evt.Val
                evt.targetIO.driveStr = evt.Strength
                if evt.targetIO.Net:
                    affectedNets.add(evt.targetIO.Net)
            for net in affectedNets:
                if net.resolve():
                    for io in net.IO:
                        if io.parent and not isinstance(io.parent, Module):
                            affectedComponent.add(io.parent)
            for comp in affectedComponent:
                comp.update()