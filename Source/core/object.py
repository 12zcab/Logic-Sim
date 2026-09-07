# Object -> IO,Update Function -> RunTick Function to trigger the Update and also update
# IO -> Connected to Net -> if self value is True, then pull the all net IO In to true   have IN and OUT function for Update.
# Net -> Every Update will clear it first until any ppl pull it up
# Net have: 1. Add IO 2.Remove IO 3. Clear all IO.In Value 4.Write 1 to all other IO.In Value if one.out is True (Net.update)
import gc
class CircuitObject:
    def __init__(self, name, IOs, update_func):
        self.name = name
        self.IOs = IOs
        self.update_func = update_func
        
class CircuitIO:
    def __init__(self, name):
        self.name = name
        self.ValIn = False
        self.ValOut = False
        self.connected_net = None
    def Input(self):
        return self.ValIn
    def Output(self,value):
        self.ValOut = value
    def ConnectToNet(self, net):
        self.connected_net = net
        net.AddIO(self)
    def DisconnectFromNet(self):
        if self.connected_net:
            self.connected_net.RemoveIO(self)
            self.connected_net = None
    def ConnectToIO(self, other_io):
        if self.connected_net and other_io.connected_net:
            self.connected_net.MergeNets(other_io.connected_net)
        elif self.connected_net:
            other_io.ConnectToNet(self.connected_net)
        elif other_io.connected_net:
            self.ConnectToNet(other_io.connected_net)
        else:
            new_net = Net()
            self.ConnectToNet(new_net)
            other_io.ConnectToNet(new_net)
    def DisconnectFromIO(self, other_io):
        if len(self.connected_net.ios) > 2:
            self.DisconnectFromNet()
        elif len(self.connected_net.ios) == 2:
            other_io.DisconnectFromNet()
            self.DisconnectFromNet()
            

class Net:
    def __init__(self,name):
        self.ios = []
        self.name = name if name else f"Net_{id(self)}"
    def AddIO(self, io):
        if io not in self.ios:
            self.ios.append(io)
    def RemoveIO(self, io):
        if io in self.ios:
            self.ios.remove(io)
    def Clear(self):
        for io in self.ios:
            io.ValIn = False
    def Update(self):
        self.Clear()
        for io in self.ios:
            if io.ValOut:
                for io2 in self.ios:
                    io2.ValIn = True
                    
def Destroy(sth):
    del sth
    gc.collect()