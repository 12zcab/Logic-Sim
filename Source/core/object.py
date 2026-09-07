# Object -> IO,Update Function -> RunTick Function to trigger the Update and also update
# IO -> Connected to Net -> if self value is True, then pull the all net IO In to true   have IN and OUT function for Update.
# Net -> Every Update will clear it first until any ppl pull it up
# Net have: 1. Add IO 2.Remove IO 3. Clear all IO.In Value 4.Write 1 to all other IO.In Value if one.out is True (Net.update)

import gc

class CircuitObject:
    def __init__(self, name, IOs, update_func):
        self.name = name
        self.IOs = IOs  # Dictionary: {"PinName": CircuitIO}
        self.update_func = update_func


class CircuitIO:
    def __init__(self, name):
        self.name = name
        self.ValIn = False
        self.ValOut = False
        self.connected_net = None

    def GetInput(self):
        return self.ValIn

    def Output(self, value):
        self.ValOut = value

    def ConnectToNet(self, net):
        if self.connected_net:
            self.DisconnectFromNet()
        self.connected_net = net
        net.AddIO(self)

    def DisconnectFromNet(self):
        if self.connected_net:
            self.connected_net.RemoveIO(self)
            self.connected_net = None

    def ConnectToIO(self, other_io):
        if self.connected_net and other_io.connected_net:
            if self.connected_net != other_io.connected_net:
                self.connected_net.MergeNets(other_io.connected_net)
        elif self.connected_net:
            other_io.ConnectToNet(self.connected_net)
        elif other_io.connected_net:
            self.ConnectToNet(other_io.connected_net)
        else:
            new_net = Net()  # Works now due to default name=None
            self.ConnectToNet(new_net)
            other_io.ConnectToNet(new_net)

    def DisconnectFromIO(self, other_io):
        # Simplified disconnect per your requirements
        if not self.connected_net:
            return

        if len(self.connected_net.ios) > 2:
            self.DisconnectFromNet()
        elif len(self.connected_net.ios) <= 2:
            net_to_destroy = self.connected_net
            self.DisconnectFromNet()
            other_io.DisconnectFromNet()
            DestroyNet(net_to_destroy)


class Net:
    def __init__(self, name=None):  # Fixed: name defaults to None
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
        if any(io.ValOut for io in self.ios):
            for io in self.ios:
                io.ValIn = True

    def PrepareDelete(self):
        for io in self.ios:
            io.connected_net = None
        self.ios.clear()

    def MergeNets(self, other_net):
        for io in list(other_net.ios):
            self.AddIO(io)
            io.connected_net = self
        DestroyNet(other_net)


def DestroyNet(net_obj):
    if net_obj:
        net_obj.PrepareDelete()
        del net_obj
        gc.collect()


class SimBox:
    def __init__(self, Objects, Nets):
        self.Objects = Objects
        self.Nets = Nets

    def update(self):
        # Step 1: Objects evaluate inputs and set outputs
        for obj in self.Objects:
            obj.update_func(obj.IOs)

        # Step 2: Nets propagate signals across connected pins
        for net in self.Nets:
            net.Update()