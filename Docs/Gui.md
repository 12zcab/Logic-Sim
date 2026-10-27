# GUI Documentation (WIP Document)


### Main Modules

- [Toolbar](#Toolbar)

- [Loader](#Loader)

- [Node Engine](#Node-Engine)

- [Attribute Panel](#Attribute-Panel)

- [main.py](#mainpy)


So every GUI panel is modularized into different library that can be called and return a Tkinter Frame Object.

The Whole Application is based on basic Tkinter (no TTK iirc)


---


## Toolbar

So the it is used to display Buttons that is resizable and contains both text or pyIcons(A python file dedicated for rendering in Tkinter Canvas).

## Loader 

Erm I am still thinking if I should just move it into the main.py but anyways this is a module that help handle Json file as App and Module configurations

## Node Engine

This Script is about maybe 70-80% Written by Ai cuz I think I have spent too many hours on this GUI Node Editor. However, the object structure and the algorithm is designed by me.

This engine handles complex topology Net Connection between Pins and allow highly customized Node and Pin Rendering and modification. Event Listeners are supported to maximize the degree of freedom using this library.

## Attribute Panel

This is a panel with Category and Attribute Row so that Attributes can be collapsed and it also handles specific Type Inputs and also support event listeners.

## Main.py

This script Initilizes everything and load every modules to create a GUI application that connect GUI Interface with Core logic Engine,mapping user GUI interaction to Logic Connections and updates for simulation.