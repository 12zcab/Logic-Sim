from core.object import *

def generator_logic(self):
    self.IOs["OUT"].Output(True)

def inverter_logic(self):
    self.IOs["OUT"].Output(not self.IOs["IN"].GetInput())

gen = CircuitObject("Gen", {"OUT": CircuitIO("OUT")}, generator_logic)
inv = CircuitObject("Inv", {"IN": CircuitIO("IN"), "OUT": CircuitIO("OUT")}, inverter_logic)

gen.IOs["OUT"].ConnectToIO(inv.IOs["IN"])

net1 = gen.IOs["OUT"].connected_net

sim = SimBox(Objects=[gen, inv], Nets=[net1])

sim.update()
sim.update()
print(f"Generator OUT: {gen.IOs['OUT'].GetInput()}")
print(f"Inverter IN:   {inv.IOs['IN'].GetInput()}")
print(f"Inverter OUT:  {inv.IOs['OUT'].ValOut}")