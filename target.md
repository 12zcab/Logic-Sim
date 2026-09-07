# Logic Sim Project
Want I want to do:
1.Cli Interface
2.Exportable
3.GUI Interface
4.Drag and Drop Node Connection
5.Modularized n Extendable
6.Simple Logic Gates
7.Memories


Python
  maybe + a little bit HTML

Directory Tree:
Root
->modules
  ->ModFolder
    ->asset
    ->info.json   Stores Module Information  like Parts Assets etc  
      info tells the app how to mount different folders and files and also store basic informations such like mod name and mod ver etc.
->core
  ->library
  corefunctions
  E.G. LogicUpdate.py
       CLI.py
  ->object.py
->app.py


GUI count as mod..?   yes..?



Latch

-> Gates -> Mod
-> Button Input -> Mod Basic IO
-> Signal Output -> Mod Basic IO
CLI Interface connect stuff and disconnect stuff and start simulation stuff   -> CLI.py
Simulate -> Update by Logic Tic -> LogicUpdate.py
LogicUpdate Need to grep Informations of Objects -> Object.py
Object.py need to handle:
1. Connection
2. Update Code

