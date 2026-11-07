import os
import time
from tkinter import Tk, PanedWindow, VERTICAL, HORIZONTAL, RAISED, BOTH, filedialog
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
        self.GuiUpdate = 0
        
        self._last_win_w = 900
        self._last_win_h = 700
        self._last_net_values = {}
        self._last_gui_time = time.perf_counter()

        self.setup_ui()
        self.load_all()
        self.root.after(0, self.updateMainApp)
        self.simBox = SimBox([])
        self.simBox.init()
        self._nodeAttributes = {
            "x": {
                "attribute": "x",
                "type": "float"
            },
            "y": {
                "attribute": "y",
                "type": "float"
            },
            "width": {
                "attribute": "width",
                "type": "float"
            },
            "height": {
                "attribute": "height",
                "type": "float"
            },
            "angle": {
                "attribute": "angle",
                "type": "integer"
            }
        }

    def updateMainApp(self):
        self.simBox.stepDeltaLoop()
        self.simBox.scheduler.advanceToNext()

        self.updateNetStates()

        if hasattr(self, "node_editor"):
            self.node_editor.update_dirty_node_graphics()

        self.GuiUpdate += 1
        self.root.after(1, self.updateMainApp)

    def updateNetStates(self):
        color_map = {
            Logic.ONE: "#38bdf8",
            Logic.X: "#f8bd38",
            Logic.ZERO: "#222222",
            Logic.Z: "black"
        }
        for sim_net, gui_net in list(self.logicNetToNodeNet.items()):
            val = sim_net.Value
            if self._last_net_values.get(sim_net) != val:
                self._last_net_values[sim_net] = val
                gui_net.color = color_map.get(val, "#114C06")

    def setup_ui(self):
        self.root.bind("<Configure>", self.on_window_resize)

        self.upperToolbarPaned = PanedWindow(
            self.root,
            orient=VERTICAL,
            sashwidth=6,
            sashrelief=RAISED,
            bg="#2D2D2D"
        )
        self.upperToolbarPaned.pack(fill=BOTH, expand=True)

        self.toolbar = ToolBar(master=self.upperToolbarPaned)
        self.upperToolbarPaned.add(self.toolbar, minsize=40, height=80)
        
        self.lowerToolbarPaned = PanedWindow(
            self.upperToolbarPaned,
            orient=VERTICAL,
            sashwidth=6,
            sashrelief=RAISED,
            bg="#2D2D2D"
        )
        self.upperToolbarPaned.add(self.lowerToolbarPaned, minsize=40, height=80)
        self.upperToolbarPaned.pack(fill=BOTH, expand=True)
        
        self.sub_toolbar = ToolBar(master=self.lowerToolbarPaned)
        self.lowerToolbarPaned.add(self.sub_toolbar, minsize=40, height=80)
        self.lowerMidToolbarPaned = PanedWindow(
            self.lowerToolbarPaned,
            orient=HORIZONTAL,
            sashwidth=6,
            sashrelief=RAISED,
            bg="#2D2D2D"
        )
        self.lowerToolbarPaned.add(self.lowerMidToolbarPaned, minsize=200)
        self.node_editor = NodeEditor(self.lowerMidToolbarPaned)
        self.attributePanel = AttributePanel(self.lowerMidToolbarPaned)
        self.lowerMidToolbarPaned.add(self.node_editor, stretch="always")
        self.lowerMidToolbarPaned.add(self.attributePanel, width=200, stretch="never")
        
        self.node_editor.bind_event("net_create", lambda net: self.createNetEvent(net))
        self.node_editor.bind_event("net_destroy", lambda net: self.destroyNetEvent(net))
        self.node_editor.bind_event("connect", lambda net, pin: self.connectPinEvent(net,pin))
        self.node_editor.bind_event("disconnect", lambda net, pin: self.disconnectPinEvent(net,pin))
        self.node_editor.bind_event("node_delete", lambda node: self.deleteLogicObj(node))
        self.node_editor.bind_event("select", lambda obj, rx, ry: self.handle_node_click(obj, rx, ry))
        self.node_editor.bind_event("node_move", lambda node: self.handle_node_move(node))

    def on_window_resize(self, event):
        if event.widget == self.root:
            curr_w = event.width
            curr_h = event.height
            if abs(self._last_win_w - curr_w) > 5 or abs(self._last_win_h - curr_h) > 5:
                if self._last_win_w > 0 and self._last_win_h > 0 and hasattr(self, "node_editor"):
                    scale = min(curr_w / self._last_win_w, curr_h / self._last_win_h)
                    if scale > 0 and abs(scale - 1.0) > 0.02:
                        self.node_editor.zoom = max(5.0, self.node_editor.zoom * scale)
                        self.node_editor.redraw_all()
                self._last_win_w = curr_w
                self._last_win_h = curr_h

    def handle_node_move(self, node):
        self.updateNodeAttributePanel(self.logicToNode.inv.get(node), node)

    def handle_node_click(self, obj, ax, ay):
        if obj is None:
            self.attributePanel.clearCategories()
            self.lastSelectedNode = None
            return
        if isinstance(obj, NodeObject):
            logic_obj = self.logicToNode.inv.get(obj)
            if logic_obj and getattr(logic_obj, "onclick", None):
                logic_obj.onclick(ax - obj.x, ay - obj.y)
            if not self.lastSelectedNode == obj:
                self.loadAttributePanel(logic_obj, obj)
            else:
                self.updateAttributePanel(logic_obj, obj)
            self.lastSelectedNode = obj

    def loadAttributePanel(self, logicObject, nodeObject):
        self.attributePanel.clearCategories()
        self.attributePanel.setTitle(logicObject.Name)
        if logicObject.__class__.__name__ in self.constructToDefin.keys():
            definition = self.constructToDefin[logicObject.__class__.__name__].get("attributes", None)
            if definition:
                for key in definition.keys():
                    cate = self.attributePanel.addCategory(key)
                    for key2 in definition[key].keys():
                        attr = cate.addAttribute(key2, definition[key][key2]["type"], lambda value, logicObject=logicObject, definition=definition, key=key, key2=key2: self.updateAttribute(logicObject, definition[key][key2], value))
                        attr.setValue(getattr(logicObject, definition[key][key2]["attribute"]), trigger_recall=False)
        self.loadNodeAttributePanel(logicObject, nodeObject)

    def updateAttributePanel(self, logicObject, nodeObject):
        self.attributePanel.setTitle(logicObject.Name)
        if logicObject.__class__.__name__ in self.constructToDefin.keys():
            definition = self.constructToDefin[logicObject.__class__.__name__].get("attributes", None)
            if definition:
                for key in definition.keys():
                    cate = self.attributePanel.categories[key]
                    for key2 in definition[key].keys():
                        attr = cate.attributes[key2]
                        attr.setValue(getattr(logicObject, definition[key][key2]["attribute"]), trigger_recall=False)
        self.updateNodeAttributePanel(logicObject, nodeObject)

    def loadNodeAttributePanel(self, logicObject, nodeObject):
        nodeCate = self.attributePanel.addCategory("Node Data")
        for attributeLabel in self._nodeAttributes.keys():
            nodeCate.addAttribute(attributeLabel, self._nodeAttributes[attributeLabel]["type"], lambda value, obj=nodeObject, spec=self._nodeAttributes[attributeLabel]: self.updateAttribute(obj, spec, value)).setValue(getattr(nodeObject, self._nodeAttributes[attributeLabel]["attribute"]), trigger_recall=False)

    def updateNodeAttributePanel(self, logicObject, nodeObject):
        if "Node Data" in self.attributePanel.categories.keys():
            nodeCate = self.attributePanel.categories["Node Data"]
            for attributeLabel in self._nodeAttributes.keys():
                nodeCate.attributes[attributeLabel].setValue(getattr(nodeObject, self._nodeAttributes[attributeLabel]["attribute"]), trigger_recall=False)
        else:
            self.loadNodeAttributePanel(logicObject, nodeObject)

    def updateAttribute(self, logicObject, spec, value):
        setattr(logicObject, spec["attribute"], value)
        if spec.get("callFunc"):
            getattr(logicObject, spec["callFunc"])()

    def guiPinToLogicPin(self, guiPin):
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

    def addLogic(self, logicObj, nodeObj):
        logicObj.guiNode = nodeObj
        self.simBox.addObject(logicObj)
        self.logicToNode[logicObj] = nodeObj
        if hasattr(self, "node_editor") and nodeObj not in self.node_editor.nodes:
            self.node_editor.nodes.append(nodeObj)
        self.node_editor.rebuild_nets()

    def deleteLogicObj(self, node):
        logic_obj = self.logicToNode.inv.get(node)
        if node == self.lastSelectedNode:
            self.attributePanel.clearCategories()
            self.lastSelectedNode = None
        if logic_obj:
            if hasattr(logic_obj, "guiNode"):
                logic_obj.guiNode = None
            for io in logic_obj.IO.values():
                io.disconnectNet()
                if io.Net:
                    io.Net.resolve()
            self.simBox.removeObject(logic_obj)
            if logic_obj in self.logicToNode:
                del self.logicToNode[logic_obj]
            if node in self.logicToNode.inv:
                del self.logicToNode.inv[node]
            self.simBox.expandNet()
        if hasattr(self, "node_editor"):
            self.node_editor.rebuild_nets()
            self.node_editor.redraw_all()

    def load_all(self):
        self.load_modules()
        for modName in list(reversed(self.all_jsons)):
            self.switch_module(modName)
        self.switch_module("File")

    def load_modules(self):
        module_jsons = guiJsonPaths()
        filebt = self.toolbar.add_button("File")
        filebt.config(command=lambda: self.switch_module("File"))
        for module_path in module_jsons:
            json_obj = loadJson(module_path)
            module_name = json_obj.get("name")
            
            self.all_jsons[module_name] = json_obj
            self.all_jsons[module_name]["__path__"] = module_path
            
            bt = self.toolbar.add_button(module_name)
            bt.config(command=lambda name=module_name: self.switch_module(name))

    def SaveAll(self):
        filename = filedialog.asksaveasfilename(
            defaultextension=".LSproj",
            filetypes=[("LogicSim File", "*.LSproj")],
            title="Save LogicSim Project"
        )
        if filename:
            exporter = Exporter(self, filename, "UntitledApp")
            exporter.Catch()
            exporter.Store()

    def LoadAll(self):
        filename = filedialog.askopenfilename(
            defaultextension=".LSproj",
            filetypes=[("LogicSim File", "*.LSproj")],
            title="Load LogicSim Project"
        )
        if filename:
            importer = Importer(filename, "UntitledApp", self, globals_dict=globals())
            importer.Import()

    def ClearAll(self):
        self.node_editor.clear()
        self.attributePanel.clearCategories()

    def switch_module(self, module_name):
        self.sub_toolbar.clear_buttons()
        
        module_data = self.all_jsons[module_name]
        component_names = getComponents(module_data)
        function_names = getFunctions(module_data)
        components_obj = module_data.get("components", {})
        module_dir = os.path.dirname(module_data["__path__"])
        
        for component_name in component_names:
            pyIconPathRatio, loadingObj, defin = self.get_component_data(
                module_dir, components_obj, component_name
            )
            bt = self.sub_toolbar.add_button(component_name, pyIconPathRatio)
            bt.config(command=lambda loader=loadingObj: self.spawnFromButton(loader))
            self.constructToDefin[defin.get("constructor")] = defin
        for functionName in function_names:
            functionDef = module_data.get("function", {}).get(functionName, {})
            codeFile = functionDef.get("code")
            if codeFile:
                codePath = os.path.join(module_dir, codeFile)
                bt = self.sub_toolbar.add_button(functionName)
                bt.config(command=lambda cp=codePath, fd=functionDef: self.execute_gui_function(cp, fd))
        self.sub_toolbar.force_update()

    def execute_gui_function(self, code_path, function_def):
        params = function_def.get("parameters", {})
        exec_scope = globals().copy()
        exec_scope["self"] = self
        if "path" in params.values() or "path" in params:
            file_path = filedialog.askopenfilename(
                title="Select File",
                filetypes=[("All Files", "*.*")]
            )
            if not file_path:
                return
            exec_scope["path"] = file_path
        with open(code_path, "r", encoding="utf-8") as f:
            code_content = f.read()
        exec(code_content, exec_scope)

    def spawnFromButton(self, loader):
        self.root.config(cursor="plus")
        self.node_editor.grepNextPressGridPos(
            lambda x, y: self.spawnObject(loader, x, y)
        )

    def spawnObject(self, loader, x, y):
        self.root.config(cursor="arrow")
        returnstuff = loader(x, y)
        logicObj = returnstuff[0]
        nodeObj = returnstuff[1]
        self.addLogic(logicObj,nodeObj)

    def get_component_data(self, module_dir, components_obj, component_name):
        component_def = getComponentDefinition(components_obj, component_name)
        pyicon_path = None
        ratio = None
        icon_data = None
        if "children" in component_def.keys():
            if "pyIcon" in component_def["children"].keys():
                icon_data = component_def.get("children", {}).get("pyIcon", {})
                ratio = component_def.get("children", {}).get("pyIcon", {}).get("size")
        if icon_data is not None:
            pyicon_path = os.path.join(module_dir, icon_data.get("path"))
        loadingObjfunc = lambda x, y, name=component_name, defn=component_def, dir_path=module_dir: loadObject(name, defn, self.node_editor, dir_path, x, y)
        return [pyicon_path, ratio], loadingObjfunc, component_def
