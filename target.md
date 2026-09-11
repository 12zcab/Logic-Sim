Pulse Cli Out Observer

Perfectly stored all the project data in 1 object and also keep global variables safe
So when export project we can just simply make that object a json file
Also same when import
We probly need more detail feature before we do the GUI
Firstly is function description per function
It tells user how to use the function and also help generate layout for calling the func in GUI mode

12zcab — 19:13
Yah
Will have a module.json pointing to every function in the module python code
And what argument to input too
It helps implementing the help command in CLI
Like we can help object. afunction
And then return a great info.
Also it can help dynamically generate a proper layout for gui function without needing to hard code it.
Like what field must be filled in and its type ( Text box,check box etc.
I think the overall project file will contain a :  components.json for components and nets
node.json for GUI node status
project.circuitsim - actually a json but contains project details and settings like default update speed etc.
Wow so much thing to improve

