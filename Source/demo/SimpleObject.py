from core.object import *

def generator_logic(self):
    self.IO["OUT"].Value = True

def inverter_logic(self):
    self.IO["OUT"].Value = (not self.IO["IN"].Value)

gen = Component("Gen", {"OUT": IO("OUT")}, generator_logic)
inv = Component("Inv", {"IN": IO("IN"), "OUT": IO("OUT")}, inverter_logic)

gen.IO["OUT"].connect(inv.IO["IN"])

net1 = gen.IO["OUT"].Net

sim = SimBox([gen, inv],[net1])

sim.update()
sim.update()
print(f"Generator OUT: {gen.IO['OUT'].Value}")
print(f"Inverter IN:   {inv.IO['IN'].Value}")
print(f"Inverter OUT:  {inv.IO['OUT'].Value}")