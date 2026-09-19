from core.library.BetterDict import *
class Component:
    def __init__(self, Name, IOArray, updateFunction):
        self.Name = Name
        self.isObserver = False
        self.IO = BetterDict(IOArray) if isinstance(IOArray, dict) else BetterDict({io.Name: io for io in IOArray})
        self.updateFunction = updateFunction
    def update(self):
        self.updateFunction(self)
    def commitChange(self):
        for io in self.IO.values():
            io._Value = io.futureValue
            io.futureValue = False
    def getNet(self):
        NetArray = []
        for io in self.IO.values():
            NetArray.append(io.Net) if (io.Net not in NetArray) and not (io.Net == None) else None
        return NetArray




class IO:
    def __init__(self, Name):
        self.Name = Name
        self._Value = False
        self.futureValue = False  
        self.Net = None
    
    @property
    def Value(self):
        return self._Value

    @Value.setter
    def Value(self, Value):
        self.futureValue = Value
    def set(self, Value):
            self.futureValue = Value
    
    def __rshift__(self, other):
        if isinstance(other,IO):
            self.connect(other)
            return other
        if isinstance(other,Net):
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
            self.Net = None
    def connect(self, subject):
        if self.Net and subject.Net:
            if self.Net != subject.Net:
                self.Net.mergeNets(subject.Net)
        elif self.Net:
            subject.connectNet(self.Net)
        elif subject.Net:
            self.connectNet(subject.Net)
        else:
            new_net = Net()
            self.connectNet(new_net)
            subject.connectNet(new_net)

    def disconnect(self, subject):
        if not self.Net:
            return
        if len(self.Net.IO) > 2:
            self.disconnectNet()
        elif len(self.Net.IO) <= 2:
            net_to_destroy = self.Net
            self.disconnectNet()
            subject.disconnectNet()
            destroyNet(net_to_destroy)


class Net:
    def __init__(self, Name=None):  # Fixed: name defaults to None
        self.IO = []
        self.Name = Name if Name else f"Net_{id(self)}"
    def add(self, io):
        if io not in self.IO:
            self.IO.append(io)
    def remove(self, io):
        if io in self.IO:
            self.IO.remove(io)
    def update(self):
        if any(io.futureValue for io in self.IO):
            for io in self.IO:
                io.futureValue = True
    def prepareDelete(self):
        for io in self.IO:
            io.Net = None
        self.IO.clear()
    def mergeNets(self, subject):
        for io in list(subject.IO):
            self.add(io)
            io.Net = self
        destroyNet(subject)

def destroyNet(Net):
    if Net:
        Net.prepareDelete()
        del Net

class SimBox:
    def __init__(self, Objects, Nets=[]):
        self.Objects = Objects
        self.Nets = Nets
    def commitChange(self):
        for Obj in self.Objects:
            Obj.commitChange()
    def update(self):
        pending = []
        for obj in self.Objects:
            if obj.isObserver:
                pending.append(obj)
                continue
            obj.update()
        for net in self.Nets:
            net.update()
        self.commitChange()
        for pendingObj in pending:
            pendingObj.update()
    def expandNet(self):
        for obj in self.Objects:
            for net in obj.getNet():
                self.Nets.append(net) if (net not in self.Nets) and not (net == None) else None
    def addObject(self,obj):
        self.Objects.append(obj)
        
class Bus(Component):
    def __init__(self, Name, Width):
        IOArray = []
        for i in range(Width):
            IOArray.append(IO(self.getIOName(i)))
        super().__init__(Name, IOArray, None)
        self.Width = Width
    def getNet(self):
        NetArray = []
        for io in self.IO.values():
            NetArray.append(io.Net) if (io.Net not in NetArray) and not (io.Net == None) else None
        return NetArray
    def getIOName(self,Index):
        return self.Name + "_" + str(Index)

class Module(Component):
    def __init__(self, Name, ModuleIO, InnerBlock):
        # can do Module("Module",[Block.IO.A >> IO("Pin")],[Block])
        super().__init__(Name, ModuleIO, None)
        self.child = BetterDict(InnerBlock) if isinstance(InnerBlock, dict) else BetterDict({block.Name: block for block in InnerBlock})
    def getNet(self):
        NetArray = []
        for io in self.IO.values():
            NetArray.append(io.Net) if (io.Net not in NetArray) and not (io.Net == None) else None
        for block in self.child.values():
            NetArray.extend(block.getNet())
        return NetArray
    def commitChange(self):
        for Obj in self.child.values():
            Obj.commitChange()
        for io in self.IO.values():
            io._Value = io.futureValue
            io.futureValue = False
    def update(self):
        for block in self.child.values():
            block.update()