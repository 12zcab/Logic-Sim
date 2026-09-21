from core.library.BetterDict import BetterDict


class Component:
    def __init__(self, Name, IOArray, updateFunction):
        self.Name = Name
        self.isObserver = False
        self.IO = BetterDict(IOArray) if isinstance(IOArray, dict) else BetterDict({io.Name: io for io in IOArray})
        self.updateFunction = updateFunction

    def update(self):
        if self.updateFunction:
            self.updateFunction(self)

    def getNet(self):
        NetArray = []
        for io in self.IO.values():
            if io.Net is not None and io.Net not in NetArray:
                NetArray.append(io.Net)
        return NetArray


class IO:
    def __init__(self, Name):
        self.Name = Name
        self.Net = Net()
        self.Net.add(self)

    @property
    def Value(self):
        return self.Net._Value if self.Net else False

    @Value.setter
    def Value(self, val):
        if self.Net:
            self.Net.futureValue.append(val)

    def set(self, val):
        self.Value = val

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
            self.Net = Net()
            self.Net.add(self)  # Ensure new fallback net contains self

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
        if not self.Net or self.Net != subject.Net:
            return
        target_net = self.Net
        if len(target_net.IO) > 2:
            self.disconnectNet()
        else:
            self.disconnectNet()
            subject.disconnectNet()
            destroyNet(target_net)


class Net:
    def __init__(self, Name=None):
        self.IO = []
        self.Name = Name if Name else f"Net_{id(self)}"
        self._Value = False
        self.futureValue = []

    def add(self, io):
        if io not in self.IO:
            self.IO.append(io)

    def remove(self, io):
        if io in self.IO:
            self.IO.remove(io)

    def update(self):
        self._Value = False
        if True in self.futureValue:
            self._Value = True
        self.futureValue = []

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
        subject.IO.clear()  # CLEAR subject.IO before destruction to protect io.Net assignments
        destroyNet(subject)


def destroyNet(net):
    if net:
        net.prepareDelete()


class SimBox:
    def __init__(self, Objects, Nets=None):
        self.Objects = Objects
        self.Nets = Nets if Nets is not None else []

    def update(self):
        pending = []
        for obj in self.Objects:
            if getattr(obj, "isObserver", False):
                pending.append(obj)
                continue
            obj.update()
        for net in self.Nets:
            net.update()
        for pendingObj in pending:
            pendingObj.update()

    def expandNet(self):
        new_nets = []
        for obj in self.Objects:
            for net in obj.getNet():
                if net is not None and net not in new_nets:
                    new_nets.append(net)
        self.Nets = new_nets

    def addObject(self, obj):
        self.Objects.append(obj)


class Bus(Component):
    def __init__(self, Name, Width):
        IOArray = [IO(self.getIOName(i)) for i in range(Width)]
        super().__init__(Name, IOArray, None)
        self.Width = Width

    def getIOName(self, Index):
        return f"{self.Name}_{Index}"


class Module(Component):
    def __init__(self, Name, ModuleIO, InnerBlock):
        super().__init__(Name, ModuleIO, None)
        self.child = BetterDict(InnerBlock) if isinstance(InnerBlock, dict) else BetterDict({block.Name: block for block in InnerBlock})

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
        for block in self.child.values():
            block.update()