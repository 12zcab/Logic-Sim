import os
from tkinter import Tk, PanedWindow, VERTICAL, RAISED, BOTH
from node.nodeEngine import *
from toolbar.toolbar import *
from connector import *

class LogicSimApp:
    def __init__(self, root):
        self.root = root
        self.root.title("LogicSim GUI")
        self.root.geometry("900x700")
        
        self.all_jsons = {}
        self.constructor_to_container = {}
        self.setup_ui()
        self.load_all()

    def setup_ui(self):
        self.paned_window = PanedWindow(
            self.root,
            orient=VERTICAL,
            sashwidth=6,
            sashrelief=RAISED,
            bg="#2D2D2D"
        )
        self.paned_window.pack(fill=BOTH, expand=True)

        self.toolbar = ToolBar(master=self.paned_window)
        self.sub_toolbar = ToolBar(master=self.paned_window)
        self.node_editor = NodeEditor(master=self.paned_window)

        self.paned_window.add(self.toolbar, minsize=40, height=80)
        self.paned_window.add(self.sub_toolbar, minsize=40, height=80)
        self.paned_window.add(self.node_editor, minsize=200)
    def load_all(self):
        self.load_modules()
        for modName in list(reversed(self.all_jsons)):
            self.switch_module(modName)
    def load_modules(self):
        module_jsons = guiJsonPaths()
        
        for module_path in module_jsons:
            json_obj = loadJson(module_path)
            module_name = json_obj.get("name")
            
            self.all_jsons[module_name] = json_obj
            self.all_jsons[module_name]["__path__"] = module_path
            
            bt = self.toolbar.add_button(module_name)
            bt.config(command=lambda name=module_name: self.switch_module(name))

    def switch_module(self, module_name):
        self.sub_toolbar.clear_buttons()
        
        module_data = self.all_jsons[module_name]
        component_names = getComponents(module_data)
        components_obj = module_data.get("components", {})
        module_dir = os.path.dirname(module_data["__path__"])
        
        for component_name in component_names:
            pyicon_path, loadingObj, loadingContainer = self.get_component_data(
                module_dir, components_obj, component_name
            )
            bt = self.sub_toolbar.add_button(component_name, pyicon_path)
            bt.config(command=loadingContainer)
            
        self.sub_toolbar.force_update()

    def get_component_data(self, module_dir, components_obj, component_name):
        component_def = getComponentDefinition(components_obj, component_name)
        pyicon_path = None
        
        icon_data = component_def.get("children", {}).get("pyIcon", {})
        if icon_data.get("path"):
            pyicon_path = os.path.join(module_dir, icon_data.get("path"))
        loadingObjfunc = lambda name=component_name, defn=component_def, dir_path=module_dir: loadObject(name, defn, self.node_editor, dir_path)
        loadingContainerfunc = lambda name=component_name, defn=component_def, dir_path=module_dir: loadContainer(name, defn, self.node_editor, dir_path)
        self.constructor_to_container[globals()[component_def["constructor"]].__name__] = loadingContainerfunc
        return pyicon_path, loadingObjfunc, loadingContainerfunc

if __name__ == "__main__":
    root = Tk()
    app = LogicSimApp(root)
    createVerilogObjAndContainer(app.node_editor,"register.v")
    root.mainloop()