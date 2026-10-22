import os
from tkinter import Tk, PanedWindow, VERTICAL, RAISED, BOTH
from bidict import bidict

from gui.node.nodeEngine import *
from gui.toolbar.toolbar import *
from gui.loader import *
from gui.attribute.attributePanel import *
from core import *
from core.module.object import *


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
        self.lowerToolbarPaned.add(self.lowerMidToolbarPaned, minsize = 200)
        self.node_editor = NodeEditor(self.lowerMidToolbarPaned)
        self.attributePanel = AttributePanel(self.lowerMidToolbarPaned)
        self.lowerMidToolbarPaned.add(self.node_editor, stretch="always")
        self.lowerMidToolbarPaned.add(self.attributePanel, width=200, stretch="never")
        
        self.node_editor.bind_event("net_create", lambda net: self.createNetEvent(net))
        self.node_editor.bind_event("net_destroy", lambda net: self.destroyNetEvent(net))
        self.node_editor.bind_event("connect", lambda net, pin: self.connectPinEvent(net, pin))
        self.node_editor.bind_event("disconnect", lambda net, pin: self.disconnectPinEvent(net, pin))
        self.node_editor.bind_event("node_delete", lambda node: self.deleteLogicObj(node))
        self.node_editor.bind_event("select", lambda obj: self.handle_node_click(obj))
        self.node_editor.bind_event("node_move", lambda node: self.handle_node_move(node))
    def handle_node_move(self,node):
        self.updateNodeAttributePanel(self.logicToNode.inv.get(node),node)
    def handle_node_click(self, obj):
        if isinstance(obj, NodeObject):
            logic_obj = self.logicToNode.inv.get(obj)
            if logic_obj and getattr(logic_obj, "onclick", None):
                logic_obj.onclick()
            if not self.lastSelectedNode == obj:
                self.loadAttributePanel(logic_obj,obj)
            else:
                self.updateAttributePanel(logic_obj,obj)
            self.lastSelectedNode = obj
    def loadAttributePanel(self,logicObject,nodeObject):
        self.attributePanel.clearCategories()
        self.attributePanel.setTitle(logicObject.Name)
        definition = self.constructToDefin[logicObject.__class__.__name__].get("attributes",None)
        if definition:
            for key in definition.keys():
                cate = self.attributePanel.addCategory(key)
                for key2 in definition[key].keys():
                    attr = cate.addAttribute(key2,definition[key][key2]["type"],lambda value,logicObject=logicObject,definition=definition,key=key,key2=key2: self.updateAttribute(logicObject,definition[key][key2],value))
                    attr.setValue(getattr(logicObject,definition[key][key2]["attribute"]) ,trigger_recall = False)
        self.loadNodeAttributePanel(logicObject,nodeObject)
    def updateAttributePanel(self,logicObject,nodeObject):
        self.attributePanel.setTitle(logicObject.Name)
        definition = self.constructToDefin[logicObject.__class__.__name__].get("attributes",None)
        if definition:
            for key in definition.keys():
                cate = self.attributePanel.categories[key]
                for key2 in definition[key].keys():
                    attr = cate.attributes[key2]
                    attr.setValue(getattr(logicObject,definition[key][key2]["attribute"]) ,trigger_recall = False)
        self.updateNodeAttributePanel(logicObject,nodeObject)
    def loadNodeAttributePanel(self,logicObject,nodeObject):
        nodeCate = self.attributePanel.addCategory("Node Data")
        #nodeCate.addAttribute("x","float",lambda value,obj=nodeObject: self.updateAttribute(obj,{"type":"integer","attribute":"x"},value)).setValue(getattr(nodeObject,"x") ,trigger_recall = False)
        for attributeLabel in self._nodeAttributes.keys():
            nodeCate.addAttribute(attributeLabel,self._nodeAttributes[attributeLabel]["type"],lambda value,obj=nodeObject,spec=self._nodeAttributes[attributeLabel]: self.updateAttribute(obj,spec,value)).setValue(getattr(nodeObject,self._nodeAttributes[attributeLabel]["attribute"]) ,trigger_recall = False)
    def updateNodeAttributePanel(self,logicObject,nodeObject):
        if "Node Data" in self.attributePanel.categories.keys():
            nodeCate = self.attributePanel.categories["Node Data"]
            #x = nodeCate.attributes["x"]
            #x.setValue(getattr(nodeObject,"x") ,trigger_recall = False)
            for attributeLabel in self._nodeAttributes.keys():
                nodeCate.attributes[attributeLabel].setValue(getattr(nodeObject,self._nodeAttributes[attributeLabel]["attribute"]) ,trigger_recall = False)
        else:
            self.loadNodeAttributePanel(logicObject,nodeObject)
    def updateAttribute(self,logicObject,spec,value):
        setattr(logicObject,spec["attribute"],value)
        if spec.get("callFunc"):
            getattr(logicObject,spec["callFunc"])()
    def guiPinToLogicPin(self, guiPin):
        return self.logicToNode.inv[guiPin.owner].IO[guiPin.name]

    def createNetEvent(self, net):
        sim_net = Net(value=Logic.ZERO)
        self.logicNetToNodeNet[sim_net] = net
        self.simBox.expandNet()

    def destroyNetEvent(self, net):
        sim_net = self.logicNetToNodeNet.inv.get(net)
        if sim_net:
            for io in list(sim_net.IO):
                io.disconnectNet()
                if io.Net:
                    io.Net.resolve()
                if io.parent and hasattr(io.parent, "update"):
                    io.parent.update()
            if sim_net in self.logicNetToNodeNet:
                del self.logicNetToNodeNet[sim_net]
        self.simBox.expandNet()

    def connectPinEvent(self, net, pin):
        logic_io = self.guiPinToLogicPin(pin)
        sim_net = self.logicNetToNodeNet.inv.get(net)
        if sim_net:
            logic_io.connectNet(sim_net)
            sim_net.resolve()
            for io in list(sim_net.IO):
                if io.parent and hasattr(io.parent, "update"):
                    io.parent.update()
        self.simBox.expandNet()

    def disconnectPinEvent(self, net, pin):
        logic_io = self.guiPinToLogicPin(pin)
        sim_net = self.logicNetToNodeNet.inv.get(net)

        logic_io.disconnectNet()

        if sim_net:
            sim_net.resolve()
            for io in list(sim_net.IO):
                if io.parent and hasattr(io.parent, "update"):
                    io.parent.update()

        if logic_io.Net:
            logic_io.Net.resolve()

        if logic_io.parent and hasattr(logic_io.parent, "update"):
            logic_io.parent.update()
        self.simBox.expandNet()

    def addLogic(self, logicObj, nodeObj):
        self.simBox.addObject(logicObj)
        self.logicToNode[logicObj] = nodeObj
        self.node_editor.rebuild_nets()
    def deleteLogicObj(self, node):
        logic_obj = self.logicToNode.inv.get(node)
        if node == self.lastSelectedNode:
            self.attributePanel.clearCategories()
        if logic_obj:
            for io in logic_obj.IO.values():
                net = io.Net
                if net:
                    if hasattr(net, "remove"):
                        try:
                            net.remove(io)
                        except Exception:
                            pass
                    net.resolve()
                    
            self.simBox.removeObject(logic_obj)
            del self.logicToNode.inv[node]
            self.simBox.expandNet()
            
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
            pyIconPathRatio, loadingObj , defin= self.get_component_data(
                module_dir, components_obj, component_name
            )
            bt = self.sub_toolbar.add_button(component_name,pyIconPathRatio)
            bt.config(command=lambda loader=loadingObj: self.spawnFromButton(loader))
            self.constructToDefin[defin.get("constructor")] = defin
        self.sub_toolbar.force_update()

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
        self.addLogic(logicObj, nodeObj)

    def get_component_data(self, module_dir, components_obj, component_name):
        component_def = getComponentDefinition(components_obj, component_name)
        pyicon_path = None
        ratio = None
        if "children" in component_def.keys():
            if "pyIcon" in component_def["children"].keys():
                icon_data = component_def.get("children", {}).get("pyIcon", {})
                ratio = component_def.get("children", {}).get("pyIcon", {}).get("size")
        if icon_data.get("path"):
            pyicon_path = os.path.join(module_dir, icon_data.get("path"))
        loadingObjfunc = lambda x, y, name=component_name, defn=component_def, dir_path=module_dir: loadObject(name, defn, self.node_editor, dir_path, x, y)
        return [pyicon_path,ratio], loadingObjfunc,component_def