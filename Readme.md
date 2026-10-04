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
#### Made By 12zcab and Walker
#### Credit: MoonMinor for Pre3 week helping

# What is Logic-Sim?
Logic-Sim is a easy to use logic simulator written with pure python aiming for high modularization and Simple-to-use.

# How to try it?
Please download the whole Github Repo as Zip or clone it and execute the bootstrap.exe with internal_libs folder and Source folder together at the same time
If you want to try Verilog Import than you can use the register.v (Verilog tests are all done with this specific file,we will test if other verilog works too later)
For more Details of how to use Cli interface, please read Docs/Cli.md and Docs/App.md THANKYYOUUU

# Functions Implemented Now:
- Core
    - module
        - BetterDict  convenient dictionary library
        - chronos  event engine
        - enum  err just some value enums
        - object  Logic Objects
    - '__init__'.py  Importer and some testing stuff
- Gui  WIP a GUI Editor :DDDD
- modules
    - DataLogger  Basic DataLogger Module
    - FlipFlop  Basic FlipFlop Components made with LogicGate module
    - LogicGate  Basic LogicGate Module
    - SimpleCLIIO Basic Command Line Interface Input Output Module
    - Verilog Basic Verilog Component Import (YES YOU DID NOT SAW IT WRONG IT NOW HV VERILOG SUPPORTTTT)
    - '__init__'.py  Importer :D

- cli.py the basic command line interface!
- app.py currently empty, but later will for init.ing the app
- cleanpycache.py a small script to clean all the caches before we upload stuff XD
- register.v a small verilog thing for verilog test!

- target.md  a note written in day 1 :O
- bootstrap.py a loader for the exe file so that the exe can directly execute the code
- improvements.md a record of brainstorm with Ai that contains some suggestions for us to try implement later
- Readme.md  WELP U R READING ME RN
- build.bat erm yah the script i use to build the project
- bootstrap.exe  pyinstaller compiled directly executable exe! 