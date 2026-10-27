# Logic-Sim

```text
.____                 .__         _________.__         
|    |    ____   ____ |__| ____  /   _____/|__| _____  
|    |   /  _ \ / ___\|  |/ __ \ \_____  \ |  |/     \ 
|    |__(  <_> ) /_/  >  \  ___/ /        \|  |  Y Y  \
|_______ \____/\___  /|__|\___  >_______  /|__|__|_|  /
        \/    /_____/         \/        \/          \/ 
```


## An Easy to use Logic Simulation Software
### Made By 12zcab and Walker
### Credit
#### 3rd prep-week Contributor : MoonMinor
#### Day-1-Believer : @astrokoala23 for giving this project the first star

# What is Logic-Sim?
Logic-Sim is a easy to use logic simulator written with pure python aiming for high modularization and Simple-to-use.

# How to try it?
Please download and unzip the latest Release and execute the bootstrap.exe with internal_libs folder and Source folder together at the same time

# Screenshots

Erm sorry i hv not yet prepared

# Documentation

[Docs Readme](Docs/README.md)

[Tutorial(Not Yet Finished)](Docs/Tutorial/BasicLogicStuff.md)


# How can I modify this project?
## Setup Environment
You can use setupDev.bat in project Source to install the directory so that modules can be correctly  imported
## Build
To build it,just delete the internal_lib and build_cache and execute build.bat

# Brief File Structure
- Core
    - module
        - BetterDict
        - chronos
        - enum
        - object
    - '__init__'.py
- Gui
    - node
    - loader
    - toolbar
    - attribute panel
    - main.py
- modules
    - DataLogger
    - FlipFlop
    - Display
    - LogicGate
    - SimpleCLIIO (CLI only)
    - Memory
    - Verilog (CLI Only)
    - guiComponents
    - '__init__'.py

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
- README.md  WELP U R READING ME RN -_-
- build.bat erm yah the script i use to build the project
- bootstrap.exe  pyinstaller compiled directly executable exe! 
- requirements.txt  for pip install
- setupDev.bat  setting up developing environment you need for editing this project and build it yourself

- index.html docsify webpage
[Webpage](https://12zcab.github.io/Logic-Sim/)
- _sidebar.md docsify sidebar config