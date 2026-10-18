from .enum import *
from .BetterDict import *
from .chronos import *


class IO:
    def __init__(self, Name, parentComponent=None):
        self.Name = Name
        self.parent = parentComponent
        self.driveVal = Logic.X
        self.driveStr = Strength.HIGHZ
        self._Value = Logic.X
        
        default_net = Net(Name=f"Internal_{Name}")
        default_net.add(self)
        self._module_net = default_net

    def get_full_name(self):
        owner_name = self.parent.Name if self.parent else "Unowned"
        return f"{owner_name}:{self.Name}"

    @property
    def Net(self):
        if hasattr(self, '_module_net') and self._module_net:
            return self._module_net.root
        return None

    @property
    def simBox(self):
        if self.parent:
            return self.parent.simBox 
        return None

    @property
    def Value(self): 
        return self._Value

    @Value.setter
    def Value(self, val, strength=Strength.STRONG, Delay=1):
        self.setPower(val, strength, Delay)

    def setPower(self, val, strength=Strength.STRONG, Delay=1):
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

    def connect(self, subject):
        if not isinstance(subject, IO):
            raise TypeError(f"Cannot connect IO to {type(subject)}")
        if self is subject:
            return
        if self.Net != subject.Net:
            self.Net.mergeNets(subject.Net)

    def connectNet(self, net, force=False):
        if net is None:
            return
        target_net = net.root
        mod_root = self._module_net.root if hasattr(self, '_module_net') and self._module_net else self.Net
        if mod_root and mod_root != target_net:
            target_net.mergeNets(mod_root)
        else:
            target_net.add(self)

    def disconnectNet(self):
        """Cleanly unbind from the external net and restore default internal state."""
        # Unlink from merged net
        if hasattr(self, '_module_net') and self._module_net:
            base_net = self._module_net
            if base_net.merged_into:
                parent_gui = base_net.merged_into.root
                for io in list(base_net._IO):
                    if io in parent_gui._IO:
                        parent_gui._IO.remove(io)
                base_net.merged_into = None
            else:
                if self.Net:
                    self.Net.remove(self)

        # Reset driving strength back to High-Z if this isn't an active driver
        if not hasattr(self, "is_driver") or not self.is_driver:
            self.driveStr = Strength.HIGHZ
            self.driveVal = Logic.X
            self._Value = Logic.ZERO


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
        while target.merged_into is not None:
            target = target.merged_into
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
            
        maxStr = max((io.driveStr for io in ios), default=Strength.HIGHZ)
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
        for io in list(root_other._IO):
            if io not in root_self._IO:
                root_self._IO.append(io)
        root_other.merged_into = root_self


class Component:
    def __init__(self, Name, IOArray, updateFunction=None):
        self.Name = Name
        self.parent = None
        self.IO = BetterDict(IOArray) if isinstance(IOArray, dict) else BetterDict({io.Name: io for io in IOArray})
        self.updateFunction = updateFunction
        for io in self.IO.values():
            io.parent = self
        self._freeze_internal_nets()

    def _freeze_internal_nets(self):
        for io in self.IO.values():
            io._module_net = io.Net.root

    @property
    def simBox(self):
        if hasattr(self.parent, "simBox"):
            return self.parent.simBox
        return self.parent

    def update(self):
        if self.updateFunction:
            self.updateFunction(self)
    def forceUpdate(self):
        self.update()
    def getNet(self):
        NetArray = []
        for io in self.IO.values():
            if io.Net is not None and io.Net.root not in NetArray:
                NetArray.append(io.Net.root)
        return NetArray


class Module(Component):
    def __init__(self, Name, ModuleIO, InnerBlock):
        super().__init__(Name, ModuleIO, None)
        self.child = BetterDict(InnerBlock) if isinstance(InnerBlock, dict) else BetterDict({block.Name: block for block in InnerBlock})
        for block in self.child.values():
            block.parent = self
        self._freeze_internal_nets()

    def _freeze_internal_nets(self):
        super()._freeze_internal_nets()
        if hasattr(self, "child"):
            for block in self.child.values():
                if hasattr(block, "_freeze_internal_nets"):
                    block._freeze_internal_nets()

    def getNet(self):
        NetArray = []
        for io in self.IO.values():
            if io.Net is not None and io.Net.root not in NetArray:
                NetArray.append(io.Net.root)
        for block in self.child.values():
            for net in block.getNet():
                if net is not None and net.root not in NetArray:
                    NetArray.append(net.root)
        return NetArray

    def update(self):
        pass
    def forceUpdate(self):
        if hasattr(self, "child"):
            for child in self.child.values():
                if hasattr(child, "forceUpdate"):
                    child.forceUpdate()
                elif hasattr(child, "update"):
                    child.update()

class SimBox:
    def __init__(self, Objects, MAX_DELTA_CYCLES=50):
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

    def removeObject(self, obj):
        if obj in self.Objects:
            self.Objects.remove(obj)

    def expandNet(self):
        flat_objects = []
        flat_nets = []
        visited_nets = set()

        def flatten(comp, parent_node):
            if comp.parent is None or comp.parent == self:
                comp.parent = parent_node

            if comp not in flat_objects:
                flat_objects.append(comp)

            for net in comp.getNet():
                if net is not None:
                    root_net = net.root
                    if root_net not in visited_nets:
                        visited_nets.add(root_net)
                        flat_nets.append(root_net)

            if hasattr(comp, "child"):
                for child_obj in comp.child.values():
                    flatten(child_obj, parent_node=comp)

        top_level = [o for o in list(self.Objects) if o.parent is None or o.parent == self]
        for obj in top_level:
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
            if hasattr(obj, "update"):
                obj.update()
        self.stepDeltaLoop()

    def stepDeltaLoop(self):
        for obj in self.Objects:
            if hasattr(obj, "perdeltatick"):
                obj.perdeltatick()
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
                    affectedNets.add(evt.targetIO.Net.root)
            for net in affectedNets:
                if net.resolve():
                    for io in net.IO:
                        if io.parent and not isinstance(io.parent, Module):
                            affectedComponent.add(io.parent)
            for comp in affectedComponent:
                if hasattr(comp, "update"):
                    comp.update()