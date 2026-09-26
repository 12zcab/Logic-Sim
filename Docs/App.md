# App Documentation
## cli.py
Cli.py is a work-in-progress user interface (before we finish the GUI one).
User can directly use simple command to design and simulate logic components!

It features a variable vault in order to protect global variables from being edited.

### Commands
```
1.Create Variable(Object)
create varName PythonRepresentation
The result of the PythonRepresentation will be stored into varName that you can directly use as global variable later.
2.run Speed [Tick]
Speed is must provided but Tick is optional.
Leave the [Tick] blank for infinite loop
run 0   #use max speed to simulate and run infinitely
run 0.01 10   #use maximum 100 Tick Per Second to simulate and only execute 10 ticks.
3.PythonRepresentaion
PythonRepresentation  (Print Result) direct execute
Yah you can directly execute PythonRepresentation but things like "if" and "=" are not allowed as i used eval() instead of exec() :|
with this you can do something like
component.IO.A.Value.setPower(somethingsomething :|)
or componentA.IO.A >> componentB.IO.B

You can use Ctrl-C to escape from infinite loop!
```

yah i think this is already enough for a temporary documentation