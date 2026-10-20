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
Please download and unzip the latest Release and execute the bootstrap.exe with internal_libs folder and Source folder together at the same time

# How can I modify this project?
## Setup Environment:
You can use setupDev.bat in project Source to install the directory so that modules can be correctly  imported
## Build:
To build it,just delete the internal_lib and build_cache and execute build.bat

# Functions Implemented Now:
- Core
    - module
        - BetterDict  convenient dictionary library
        - chronos  event engine
        - enum  err just some value enums
        - object  Logic Objects
    - '__init__'.py  Importer and some testing stuff
- Gui
    - node  an Ai(Mostly) generate Node Based Editor Engine
    - simulation WIP  (Probly will soon be moved to main.py)
    - toolbar  (a Simple Tkinter Button Toolbar that is scalable)
    - main.py  Main GUI Program with Tkinter
- modules
    - DataLogger  Basic DataLogger Module
    - FlipFlop  Basic FlipFlop Components made with LogicGate module
    - LogicGate  Basic LogicGate Module
    - SimpleCLIIO Basic Command Line Interface Input Output Module
    - Verilog  Basic Verilog Component Import (YES YOU DID NOT SAW IT WRONG IT NOW HV VERILOG SUPPORTTTT)
    - '__init__'.py  Importer :D

More About Modules:

Modules basically consist of 3 parts:

1.```__init__.py``` and other python files with object definition

2.GUI.json with definition for the node editor render.

3.pyIcon files: a kinda special python executable script that describe rendering process of Tkinter Canvas

- cli.py the basic command line interface for debugging (mostly)
- app.py currently almost empty, but later will for init.ing the app
- cleanpycache.py a small script to clean all the caches before we upload stuff XD
- register.v a small verilog thing for verilog test!

- target.md  a note written in day 1 :O
- bootstrap.py a loader for the exe file so that the exe can directly execute the code
- improvements.md a record of brainstorm with Ai that contains some suggestions for us to try implement later
- Readme.md  WELP U R READING ME RN -_-
- build.bat erm yah the script i use to build the project
- bootstrap.exe  pyinstaller compiled directly executable exe! 
- requirements.txt  for pip install
- setupDev.bat  setting up developing environment you need for editing this project and build it yourself