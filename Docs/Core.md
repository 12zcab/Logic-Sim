# Core Documentation

## Enum
### Strength
Erh yah Strength Enum :D
### Logic
Erh yah Logic State Enum :D
Changed to 4 State one recently

## BetterDict
BetterDictionary is a Small (Yah REALLY SMALL) module that let u do Dictionary.Key instead of Dictionary[Key] :D (isnt it quite useful ?)
```
__BetterDict__["Key"] = "Value"
# can also be written as
__BetterDict_.Key = "Value"
```

## Chronos
Chronos is the god of time in Greece Mythology.Similarly, chronos.py is a module that helps arrange time sequence of events within this Logic Simulator.
### Event
erm yah I made a class named Event instead of passing arguments in a tuple : |
i probly will change that later.?
### Kairos
The class Kairos manages a sequence of event,featuring schedule,hasCurrentEvent,getNextEvent,advanceToNext, total of 4 functions
#### schedule
Schedule an IO update for planned future execution by appending it to the queue.
```
__Kairos__.schedule(component.IO.A, Logic.ONE, Strength.STRONG, Delay=0)
```
Delay: delay 0 means append to the same tick but in next delta tick for instant update otherwise Delay means how many tick you want the event to update.
#### hasCurrentEvent
Check if there are any pending event in this tick (Return a Boolean Value.)
#### getNextEvent
Pop and obtain the next event in the current time.
#### advanceToNext
Directly advance the current time to next time tick that have pended event.

## Object
Object is the most important core module in LogicSim.
It contains class definition of: IO,Net,Component,Module,Simbox.
### IO
IO Object store values and connected one share the same Net.
An update for 1 IO Object will affect other IO Object through the common Net.
### Net
Net is the object responsible for passing IO driving signal to other IO in the same Network.
### Component
Component consists of an update function and IO pins.
When IO pins of the component is updated, it call the update function to update state if IO pins.
(One Known Issue is that right now self-updating components are not handled correctly... :|)
### Module
Module is also a component, but it's purpose is for containing other components.
a Module contains IO pins and blocks.
Blocks are individual components that build the module.
The update function of the module will update all the children blocks.
### Simbox
A Simbox manage Objects(Components and Modules).
It have a internal Scheduler(Kairos Object).
#### expandNet
Search for all the Nets under Simbox's Object list.
#### stepDeltaLoop
Welp, execute 1 Deltaloop :D