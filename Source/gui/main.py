import os
from tkinter import Tk, PanedWindow, VERTICAL, RAISED, BOTH,filedialog
from bidict import bidict

from gui.node.nodeEngine import *
from gui.toolbar.toolbar import *
from gui.loader import *
from gui.attribute.attributePanel import *
from core import *


class LogicSimApp:
    def __init__(self, root):
        self.root = root
        self.root.title("LogicSim GUI")
        self.root.geometry("900x700")
        self.logicToNode = bidict({})
        self.logicNetToNodeNet = bidict({})
        self.constructToDefin = {}
        self.lastSelectedNode = None
        self.all_jsons = {}
        self.setup_ui()
        self.load_all()
        self.root.after(0, self.updateMainApp)
        self.simBox = SimBox([])
        self.simBox.init()
        self._nodeAttributes = {
            "x":{
                "attribute":"x",
                "type":"float"
            },
            "y":{
                "attribute":"y",
                "type":"float"
            },
            "width":{
                "attribute":"width",
                "type":"float"
            },
            "height":{
                "attribute":"height",
                "type":"float"
            },
            "angle":{
                "attribute":"angle",
                "type":"integer"
            }
        }
    def updateMainApp(self):
        self.simBox.stepDeltaLoop()
        self.simBox.scheduler.advanceToNext()
        self.updateNetStates()
        self.node_editor.redraw_all()
        self.root.after(1, self.updateMainApp)

    def updateNetStates(self):
        for sim_net, gui_net in list(self.logicNetToNodeNet.items()):
            val = sim_net.Value
            if val == Logic.ONE:
                gui_net.setColor("#38bdf8")
                gui_net.setAllPinColor("#38bdf8")
            elif val == Logic.X:
                gui_net.setColor("#f8bd38")
                gui_net.setAllPinColor("#f8bd38")
            else:
                gui_net.setColor("#222222")
                gui_net.setAllPinColor("#222222")

    def setup_ui(self):
        self.upperToolbarPaned = PanedWindow(
            self.root,
            orient=VERTICAL,
            sashwidth=6,
            sashrelief=RAISED,
            bg="#2D2D2D"
        )
        self.upperToolbarPaned.pack(fill=BOTH, expand=True)

        self.toolbar = ToolBar(master=self.paned_window)
        self.sub_toolbar = ToolBar(master=self.paned_window)
        self.node_editor = NodeEditor(self.paned_window)

        self.paned_window.add(self.toolbar, minsize=40, height=80)
        self.paned_window.add(self.sub_toolbar, minsize=40, height=80)
        self.paned_window.add(self.node_editor, minsize=200)
        
        self.node_editor.bind_event("net_create", lambda net: self.createNetEvent(net))
        self.node_editor.bind_event("net_destroy", lambda net: self.destroyNetEvent(net))
        self.node_editor.bind_event("connect", lambda net, pin: self.connectPinEvent(net,pin))
        self.node_editor.bind_event("disconnect", lambda net, pin: self.disconnectPinEvent(net,pin))
        self.node_editor.bind_event("node_delete", lambda node: self.deleteLogicObj(node))
        self.node_editor.bind_event("select", lambda obj: self.handle_node_click(obj))
    def handle_node_click(self, obj):
        if isinstance(obj, NodeObject):
            logic_obj = self.logicToNode.inv.get(obj)
            if getattr(logic_obj, "onclick", None):
                logic_obj.onclick()
    def guiPinToLogicPin(self,guiPin):
        return self.logicToNode.inv[guiPin.owner].IO[guiPin.name]
    def createNetEvent(self,net):
        self.logicNetToNodeNet[Net(value=Logic.ZERO)] = net
        self.simBox.expandNet()
    def destroyNetEvent(self,net):
        del self.logicNetToNodeNet.inv[net]
        self.simBox.expandNet()
    def connectPinEvent(self, net, pin):
        logic_io = self.guiPinToLogicPin(pin)
        
        sim_net = self.logicNetToNodeNet.inv.get(net)
        
        logic_io.connectNet(sim_net, force=True)
        
        if logic_io.Net:
            logic_io.Net.resolve()
            
        if logic_io.parent:
            if hasattr(logic_io.parent, "update"):
                logic_io.parent.update()
                
        self.simBox.expandNet()

    def disconnectPinEvent(self, net, pin):
        logic_io = self.guiPinToLogicPin(pin)
        
        logic_io.disconnectNet()
        
        if net and self.logicNetToNodeNet.inv.get(net):
            self.logicNetToNodeNet.inv.get(net).resolve()
            
        if logic_io.Net:
            logic_io.Net.resolve()
        if logic_io.parent and hasattr(logic_io.parent, "update"):
            logic_io.parent.update()
            
        self.simBox.expandNet()
    def addLogic(self,logicObj,nodeObj):
        self.simBox.addObject(logicObj)
        self.logicToNode[logicObj] = nodeObj
    def deleteLogicObj(self,node):
        self.simBox.removeObject(self.logicToNode.inv[node])
        del self.logicToNode.inv[node]
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
            pyicon_path, loadingObj = self.get_component_data(
                module_dir, components_obj, component_name
            )
            bt = self.sub_toolbar.add_button(component_name, pyicon_path)
            bt.config(command=lambda loader=loadingObj: self.spawnFromButton(loader))
        self.sub_toolbar.force_update()
    def spawnFromButton(self,loadingObj):
        returnstuff = loadingObj()
        logicObj = returnstuff[0]
        nodeObj = returnstuff[1]
        self.addLogic(logicObj,nodeObj)

    def get_component_data(self, module_dir, components_obj, component_name):
        component_def = getComponentDefinition(components_obj, component_name)
        pyicon_path = None
        icon_data = component_def.get("children", {}).get("pyIcon", {})
        if icon_data.get("path"):
            pyicon_path = os.path.join(module_dir, icon_data.get("path"))
        loadingObjfunc = lambda name=component_name, defn=component_def, dir_path=module_dir: loadObject(name, defn, self.node_editor, dir_path)
        return pyicon_path, loadingObjfunc
    
if __name__ == "__main__":
    root = Tk()
    app = LogicSimApp(root)
    root.mainloop()