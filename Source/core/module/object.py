from .enum import *
from .BetterDict import *
from .chronos import *
from bidict import bidict


def export_value(val):
    if val is None or isinstance(val, (bool, int, float, str)):
        return val
    if hasattr(val, "export") and callable(getattr(val, "export")):
        return val.export()
    if isinstance(val, BetterDict):
        return {"__type__": "BetterDict", "data": {k: export_value(v) for k, v in val.items()}}
    if isinstance(val, bidict):
        return {"__type__": "bidict", "data": {k: export_value(v) for k, v in val.items()}}
    if isinstance(val, dict):
        return {"__type__": "dict", "data": {str(k): export_value(v) for k, v in val.items()}}
    if isinstance(val, (list, tuple)):
        return [export_value(x) for x in val]
    if isinstance(val, set):
        return {"__type__": "set", "data": [export_value(x) for x in val]}
    return str(val)


def import_value(val):
    if isinstance(val, dict):
        t = val.get("__type__")
        if t == "BetterDict":
            bd = BetterDict()
            for k, v in val.get("data", {}).items():
                bd[k] = import_value(v)
            return bd
        elif t == "bidict":
            bd = bidict()
            for k, v in val.get("data", {}).items():
                bd[k] = import_value(v)
            return bd
        elif t == "dict":
            return {k: import_value(v) for k, v in val.get("data", {}).items()}
        elif t == "set":
            return set(import_value(x) for x in val.get("data", []))
        return {k: import_value(v) for k, v in val.items()}
    elif isinstance(val, list):
        return [import_value(x) for x in val]
    return val


class IO:
    def __init__(self, Name, parentComponent=None):
        self.Name = Name
        self.parent = parentComponent
        self.driveVal = getattr(Logic, "ZERO", "0")
        self.driveStr = getattr(Strength, "PULL", 1)
        self._Value = getattr(Logic, "ZERO", "0")
        
        default_net = Net(Name=f"Internal_{Name}")
        default_net.add(self)
        self._module_net = default_net

    def export(self) -> dict:
        net_identifier = None
        if hasattr(self, "_module_net") and self._module_net:
            net_identifier = str(id(self._module_net.root))
        elif self.Net:
            net_identifier = str(id(self.Net))
            
        return {
            "__class__": "IO",
            "Name": self.Name,
            "driveVal": export_value(self.driveVal),
            "driveStr": export_value(self.driveStr),
            "_Value": export_value(self._Value),
            "is_driver": getattr(self, "is_driver", False),
            "net_id": net_identifier
        }

    @classmethod
    def import_data(cls, data: dict) -> 'IO':
        io = cls(data["Name"])
        io.driveVal = import_value(data.get("driveVal", getattr(Logic, "ZERO", "0")))
        io.driveStr = import_value(data.get("driveStr", getattr(Strength, "PULL", 1)))
        io._Value = import_value(data.get("_Value", getattr(Logic, "ZERO", "0")))
        if "is_driver" in data:
            io.is_driver = data["is_driver"]
        if "net_id" in data:
            setattr(io, "_imported_net_id", data["net_id"])
        return io

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
    def Value(self, val, strength=getattr(Strength, "STRONG", 2), Delay=1):
        self.setPower(val, strength, Delay)

    def setPower(self, val, strength=getattr(Strength, "STRONG", 2), Delay=1):  
        sim = self.simBox
        if sim and hasattr(sim, "scheduler"):
            sim.scheduler.schedule(self, val, strength, Delay)
        else:
            if self.driveVal != val or self.driveStr != strength:
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
        if hasattr(self, '_module_net') and self._module_net:
            curr_net = self._module_net
            while curr_net and curr_net.merged_into:
                parent = curr_net.merged_into
                if parent.merged_into is None:
                    for io in list(curr_net._IO):
                        if io in parent._IO:
                            parent._IO.remove(io)
                    curr_net.merged_into = None
                    break
                curr_net = parent
        elif self.Net:
            self.Net.remove(self)

        if not hasattr(self, "is_driver") or not self.is_driver:
            self.driveStr = getattr(Strength, "HIGHZ", 0)
            self.driveVal = getattr(Logic, "X", "X")
            self._Value = getattr(Logic, "ZERO", "0")


class Net:
    def __init__(self, Name=None, value=getattr(Logic, "Z", "Z")):
        self._IO = []
        self._Name = Name
        self._Value = value
        self._Strength = getattr(Strength, "HIGHZ", 0)
        self.merged_into = None

    def export(self) -> dict:
        return {
            "__class__": "Net",
            "Name": self.Name,
            "Value": export_value(self.Value),
            "Strength": export_value(self.Strength)
        }

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
        default_highz = getattr(Strength, "HIGHZ", 0)
        default_z = getattr(Logic, "Z", "Z")
        default_zero = getattr(Logic, "ZERO", "0")
        default_x = getattr(Logic, "X", "X")

        if not ios:
            valChanged = (root_net._Value != default_z or root_net._Strength != default_highz)
            root_net._Strength = default_highz
            return valChanged
            
        maxStr = max((io.driveStr for io in ios), default=default_highz)
        if maxStr == default_highz:
            newVal = root_net._Value if root_net._Value != default_z else default_zero
            newStr = default_highz
        else:
            firstVal = None
            newVal = None
            for io in ios:
                if io.driveStr == maxStr:
                    if firstVal is None:
                        firstVal = io.driveVal
                    elif io.driveVal != firstVal:  
                        newVal = default_x
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
    def __init__(self, Name, IOArray=None, updateFunction=None):
        self.Name = Name
        self.parent = None
        self.guiNode = None
        IOArray = IOArray or {}
        self.IO = BetterDict(IOArray) if isinstance(IOArray, dict) else BetterDict({io.Name: io for io in IOArray})
        self.updateFunction = updateFunction
        for io in self.IO.values():
            io.parent = self
        self._freeze_internal_nets()

    def export(self) -> dict:
        """Base export for all Component subclasses (exports class name, Name, IOs, guiNode, and custom_data)."""
        node_obj = getattr(self, "guiNode", None)
        data = {
            "__class__": self.__class__.__name__,
            "Name": self.Name,
            "IO": {k: io.export() for k, io in self.IO.items()} if hasattr(self, "IO") and self.IO else {},
            "guiNode": node_obj.export() if node_obj and hasattr(node_obj, "export") else None,
        }
        custom_data = self.export_custom_data()
        if custom_data:
            data["custom_data"] = custom_data
        return data

    def export_custom_data(self) -> dict:
        """Override in specialized subclasses to export custom attributes."""
        return {}

    def import_custom_data(self, custom_data: dict, globals_dict: dict = None):
        """Override in specialized subclasses to import custom attributes."""
        pass

    def _freeze_internal_nets(self):
        for io in self.IO.values():
            if io.Net:
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
    def __init__(self, Name, ModuleIO=None, InnerBlock=None):
        super().__init__(Name, ModuleIO or {}, None)
        self.child = BetterDict(InnerBlock) if isinstance(InnerBlock, dict) else BetterDict({b.Name: b for b in InnerBlock or {}})
        for block in self.child.values():
            block.parent = self
        self._freeze_internal_nets()

    def export_custom_data(self) -> dict:
        """Exports essential internal child component hierarchy recursively."""
        return {
            "child": {k: child_obj.export() for k, child_obj in self.child.items()} if hasattr(self, "child") and self.child else {}
        }

    def import_custom_data(self, custom_data: dict, globals_dict: dict = None):
        if "child" in custom_data:
            from .save import Importer
            importer = Importer("", "", None, globals_dict=globals_dict)
            children = BetterDict()
            for c_name, c_data in custom_data["child"].items():
                child_comp = importer.InstantiateObject(c_data)
                child_comp.parent = self
                children[c_name] = child_comp
            self.child = children

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
        """Propagate logic evaluation to child blocks."""
        if hasattr(self, "child"):
            for child in self.child.values():
                if hasattr(child, "update"):
                    child.update()

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
            net.resolve()
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
    def clear(self):
        self.Objects.clear()
        self.Nets.clear()
        self.scheduler = Kairos()