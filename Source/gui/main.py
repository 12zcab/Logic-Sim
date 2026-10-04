from tkinter import *
from node.nodeEngine import *
from toolbar.toolbar import *
from connector import *
root = Tk()
root.title("LogicSim - Node Editor")
root.geometry("900x700")

paned_window = PanedWindow(
    root,
    orient=VERTICAL,
    sashwidth=6,
    sashrelief=RAISED,
    bg="#2D2D2D"
)
paned_window.pack(fill=BOTH, expand=True)

toolbar = ToolBar(master=paned_window)
node_editor = NodeEditor(master=paned_window)

paned_window.add(toolbar, minsize=40, height=80)
paned_window.add(node_editor, minsize=200)

moduleJsons = guiJsonPaths()
for modulePath in moduleJsons:
    jsonObj = loadJson(modulePath)
    componentsObj = jsonObj.get("components", {})
    componentNames = getComponents(jsonObj)
    module_dir = os.path.dirname(modulePath)
    for componentName in componentNames:
        componentDefinition = getComponentDefinition(componentsObj, componentName)
        bt = toolbar.add_button(componentName)
        bt.config(command=lambda name=componentName, defn=componentDefinition, dir_path=module_dir: 
            loadObject(name, defn, node_editor, dir_path)
        )

root.mainloop()