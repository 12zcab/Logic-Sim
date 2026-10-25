# Core Modules
## LogicGate

Very Very Simple LogicGate module with LUT (Look Up Table) based on 4 Signal Strength Standard and total 9 state (Same as Verilog Standard).

It consists of 10 Type of Components right now:

1. Buffer
2. Not Gate
3. And Gate
4. Or Gate
5. Not-And Gate
6. Not-Or Gate
7. Or-Not Gate (Inverted B Input Or Gate) (Same as Yosys Standard)
8. Three Input Not-And Gate (for FlipFlops)
9. Exclusive-Or Gate
10. Exclusive-Not-Or Gate

All of them supports GUI mode right now.

## FlipFlop

A FlipFlop module that serves for the Verilog Module (quite important component :D) and also demonstrate how you can write modules!

1. BasicDFF
2. PP0_DFF
3. PP0_DFF_behave
4. TFF

BasicDFF is just the simplist D-Type FlipFlop in the world.

the PP0 one is the DDF_PP0 in Yosys Standard for Verilog import.

the PP0_behave one works same as PP0 but no longer maintained (it was written before module obejct exists iirc :||)

TFF Means Toggle Flip Flop (it Toggles every Clock Rise Edge)

## Verilog
### Not Implemented Into GUI Mode Yet
it contains a Parser module and currently it only have one function (parse Verilog File into a module)

## GUI Components and Display
1. Lamp
2. Switch
3. Pulse Generator 
4. Logic Analyzer
5. Seven Segment Display

they are for GUI Interactions
More components will be added in the future :D

## Memory
1. ROM

ROM is a GUI Based Component that take Address Bus as input and output the value through Data Bus
Currently It can only be modified in GUI Mode so it does not support CLI mode but you can modify the ROM.table attribute in CLI mode though...