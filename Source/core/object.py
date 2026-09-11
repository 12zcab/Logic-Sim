# Object -> IO,Update Function -> RunTick Function to trigger the Update and also update
# IO -> Connected to Net -> if self value is True, then pull the all net IO In to true   have IN and OUT function for Update.
# Net -> Every Update will clear it first until any ppl pull it up
# Net have: 1. Add IO 2.Remove IO 3. Clear all IO.In Value 4.Write 1 to all other IO.In Value if one.out is True (Net.update)

import gc

class Component:
    def __init__(self, Name, IOArray, updateFunction):
        self.Name = Name
        self.IOArray = IOArray
        self.updateFunction = updateFunction
    def update(self):
        self.updateFunction(self)

class IO:
    def __init__(self, Name):
        self.Name = Name
        self.ValueOld = False
        self.Value = False
        self.Net = None
    def getValue(self):
        return self.Value
    def setValue(self, Value):
        self.Value = Value
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
            subject.Net(self.Net)
        elif subject.Net:
            self.connectNet(subject.Net)
        else:
            new_net = Net()
            self.connectNet(new_net)
            subject.connectNet(new_net)

    def disconnect(self, subject):
        if not self.Net:
            return
        if len(self.Net.IOArray) > 2:
            self.disconnectNet()
        elif len(self.Net.IOArray) <= 2:
            net_to_destroy = self.Net
            self.disconnectNet()
            subject.disconnectNet()
            destroyNet(net_to_destroy)


class Net:
    def __init__(self, Name=None):  # Fixed: name defaults to None
        self.IOArray = []
        self.Name = Name if Name else f"Net_{id(self)}"
    def add(self, io):
        if io not in self.IOArray:
            self.IOArray.append(io)
    def remove(self, io):
        if io in self.IOArray:
            self.IOArray.remove(io)
    def clear(self):
        for io in self.IOArray:
            io.ValueOld = io.Value
            io.Value = False
    def update(self):
        self.Clear()
        if any(io.ValueOld for io in self.IOArray):
            for io in self.IOArray:
                io.Value = True
    def prepareDelete(self):
        for io in self.IOArray:
            io.Net = None
        self.IOArray.clear()
    def mergeNets(self, subject):
        for io in list(subject.IOArray):
            self.add(io)
            io.Net = self
        destroyNet(subject)

def destroyNet(Net):
    if Net:
        Net.prepareDelete()
        del Net
        gc.collect()

class SimBox:
    def __init__(self, Objects, Nets=[]):
        self.Objects = Objects
        self.Nets = Nets
    def update(self):
        for obj in self.Objects:
            obj.update_func()
        for net in self.Nets:
            net.Update()
    def expandNet(self):
        for obj in self.Objects:
            for k,v in obj.IOArray.items():
                self.Nets.append(v.connected_net) if (v.connected_net not in self.Nets) and not(v.connected_net == None) else None
    def addObject(self,obj):
        self.Objects.append(obj)