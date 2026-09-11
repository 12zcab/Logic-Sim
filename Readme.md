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
- JohnCena ????? i guess walker added it :|
- target.md  a note written in day 1 :O

# Example:
### DataLogger and LogicGates in CLI Mode
```
Logger Test:
create And ANDGate("AND")
create Or ORGate("OR")
create Xor XORGate("XOR")
create a keyboard_button("ABT","a")
create b keyboard_button("BBT","b")
create log Logger("logger",["A","B","AND","OR","XOR"],[a.IOs["Out"],b.IOs["Out"],And.IOs["OUT"],Or.IOs["OUT"],Xor.IOs["OUT"]])
a.IOs["Out"].ConnectToIO(And.IOs["A"])
a.IOs["Out"].ConnectToIO(Or.IOs["A"])
a.IOs["Out"].ConnectToIO(Xor.IOs["A"])
b.IOs["Out"].ConnectToIO(And.IOs["B"])
b.IOs["Out"].ConnectToIO(Or.IOs["B"])
b.IOs["Out"].ConnectToIO(Xor.IOs["B"])
run 0.05
```