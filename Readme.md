# Logic-Sim
<pre>
.____                 .__         _________.__         
|    |    ____   ____ |__| ____  /   _____/|__| _____  
|    |   /  _ \ / ___\|  |/ ___\ \_____  \ |  |/     \ 
|    |__(  <_> ) /_/  >  \  \___ /        \|  |  Y Y  \
|_______ \____/\___  /|__|\___  >_______  /|__|__|_|  /
        \/    /_____/         \/        \/          \/ 
</pre>
### An Easy to use Logic Simulation Software
#### Made By 12zcab,MoonMinor and Walker

# What is Logic-Sim?
Logic-Sim is a easy to use logic simulator written with pure python aiming for high modularization and Simple-to-use.

# Functions Implemented Now:
- Core
    - cli.py
    - object.py
- Demo
    - demoSimpleObject.py  Testing Object Functions
    - testCliIO.py  Testing CliIO Module
- modules
    - DataLogger  Basic DataLogger Module
    - LogicGate  Basic LogicGate Module
    - SimpleCLIIO Basic Command Line Interface Input Output Module
- app.py currently empty, but later will for init.ing the app
- target.md  a note written in day 1 :O

# Example:
### DataLogger and LogicGates in CLI Mode
```
create And ANDGate("AND")
create Or ORGate("OR")
create Xor XORGate("XOR")
create a keyboard_button("ABT","a")
create b keyboard_button("BBT","b")
create log Logger("logger",["A","B","AND","OR","XOR"],[a.IO.Out,b.IO.Out,And.IO.OUT,Or.IO.OUT,Xor.IO.OUT])
a.IO.Out >> And.IO.A >> Or.IO.A >> Xor.IO.A
b.IO.Out >> And.IO.B >> Or.IO.B >> Xor.IO.B
run 0.05
```
### Not Gate Pulse Signal,Error Handle.
```
asd
create notgate NOTGate("Not")
create logger Logger("logger",["SignalIn","SignalOut"],[notgate.IO.A,notgate.IO.OUT])
notgate.IO.A >> notgate.IO.B
notgate.IO.A >> notgate.IO.OUT
run 0.01 5
```
Output:
```
>asd
Eval Error in [asd]: 
name 'asd' is not defined
None
>create notgate NOTGate("Not")
>create logger Logger("logger",["SignalIn","SignalOut"],[notgate.IO.A,notgate.IO.OUT])
>notgate.IO.A >> notgate.IO.B
Eval Error in [varVault["notgate"].IO.A >> varVault["notgate"].IO.B]: 
'BetterDict' object has no attribute 'B'
None
>notgate.IO.A >> notgate.IO.OUT
<core.object.IO object at 0x0000015C47B30E10>
>run 0.01 5
+------------+-------------+
| SignalIn   | SignalOut   |
+============+=============+
| True       | True        |
+------------+-------------+
+------------+-------------+
| SignalIn   | SignalOut   |
+============+=============+
| False      | False       |
+------------+-------------+
+------------+-------------+
| SignalIn   | SignalOut   |
+============+=============+
| True       | True        |
+------------+-------------+
+------------+-------------+
| SignalIn   | SignalOut   |
+============+=============+
| False      | False       |
+------------+-------------+
+------------+-------------+
| SignalIn   | SignalOut   |
+============+=============+
| True       | True        |
+------------+-------------+
>
```
Though it may seem not correct as Not Gate's Input and Output is the same,but it actually reflects the truth status of a logic gate.With output and input shorted,its output and input MUST BE THE SAME,so the Not Gate is experiencing a process delay between ticks
So this actually simulate the real-world situation
