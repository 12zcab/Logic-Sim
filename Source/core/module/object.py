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

    def connectNet(self, net,force=False):
        if force:
            self.Net = net
            net.add(self)
            return
        if net is None:
            return
        if self.Net == net:
            if self not in net.IO:
                net.add(self)
            return

        if self.Net:
            # Merge the incoming net into the pin's existing net hierarchy
            self.Net.mergeNets(net)
        else:
            self.Net = net
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
    def __init__(self, Name=None, value=Logic.Z):
        self._IO = []
        self._Name = Name
        self._Value = value
        self._Strength = Strength.HIGHZ
        self.merged_into = None

    @property
    def root(self):
        target = self
        visited = []
        while target.merged_into is not None:
            visited.append(target)
            target = target.merged_into
        for node in visited:
            node.merged_into = target
        return target
    @property
    def Name(self):
        root_net = self.root
        if root_net._Name:
            return root_net._Name
        return f"Net_{id(root_net)}"
    @Name.setter
    def Name(self, val):
        self.root._Name = val
    @property
    def IO(self):
        return self.root._IO
    @IO.setter
    def IO(self, val):
        self.root._IO = val
    @property
    def Value(self):
        return self.root._Value
    @Value.setter
    def Value(self, val):
        self.root._Value = val
    @property
    def Strength(self):
        return self.root._Strength
    @Strength.setter
    def Strength(self, val):
        self.root._Strength = val
    def add(self, io):
        root_net = self.root
        if io not in root_net._IO:
            root_net._IO.append(io)
        io.Net = root_net
    def remove(self, io):
        root_net = self.root
        if io in root_net._IO:
            root_net._IO.remove(io)
    def resolve(self):
        root_net = self.root
        ios = root_net._IO
        if not ios:
            valChanged = (root_net._Value != Logic.Z or root_net._Strength != Strength.HIGHZ)
            root_net._Value = Logic.Z
            root_net._Strength = Strength.HIGHZ
            return valChanged
            
        maxStr = max(io.driveStr for io in ios)
        if maxStr == Strength.HIGHZ:
            newVal = root_net._Value if root_net._Value != Logic.Z else Logic.ZERO
            newStr = Strength.HIGHZ
        else:
            firstVal = None
            newVal = None
            for io in ios:
                if io.driveStr == maxStr:
                    if firstVal is None:
                        firstVal = io.driveVal
                    elif io.driveVal != firstVal:
                        newVal = Logic.X
                        break
            if newVal is None:
                newVal = firstVal
            newStr = maxStr

        valChanged = (root_net._Value != newVal or root_net._Strength != newStr)
        root_net._Value = newVal
        root_net._Strength = newStr
        for io in ios:
            io._Value = newVal

        return valChanged
        root_net = self.root
        ios = root_net._IO
        if not ios:
            valChanged = (root_net._Value != Logic.Z or root_net._Strength != Strength.HIGHZ)
            root_net._Value = Logic.Z
            root_net._Strength = Strength.HIGHZ
            return valChanged
        maxStr = max(io.driveStr for io in ios)
        if maxStr == Strength.HIGHZ:
            newVal = Logic.Z
        else:
            firstVal = None
            newVal = None
            for io in ios:
                if io.driveStr == maxStr:
                    if firstVal is None:
                        firstVal = io.driveVal
                    elif io.driveVal != firstVal:
                        newVal = Logic.X
                        break
            if newVal is None:
                newVal = firstVal
        valChanged = (root_net._Value != newVal or root_net._Strength != maxStr)
        root_net._Value = newVal
        root_net._Strength = maxStr
        for io in ios:
            io._Value = newVal

        return valChanged
    def prepareDelete(self):
        root_net = self.root
        for io in list(root_net._IO):
            io.Net = None
        root_net._IO.clear()
    def mergeNets(self, other):
        if other is None:
            return
        root_self = self.root
        root_other = other.root
        if root_self is root_other:
            return
        if not root_self._Name and root_other._Name:
            root_self._Name = root_other._Name
        for io in root_other._IO:
            io.Net = root_self
            if io not in root_self._IO:
                root_self._IO.append(io)
        root_other._IO = []
        root_other.merged_into = root_self

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
    def __init__(self, Objects, MAX_DELTA_CYCLES=50):
        self.Objects = []
        self.Nets = []
        self.scheduler = Kairos()
        self.MAX_DELTA_CYCLES = MAX_DELTA_CYCLES
        for obj in Objects:
            self.addObject(obj)
    def addObject(self, obj):
        print("SimBox Added Obj:")
        print(obj)
        obj.parent = self
        if obj not in self.Objects:
            self.Objects.append(obj)
    def removeObject(self, obj):
        if obj in self.Objects:
            self.Objects.remove(obj)
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