from gui.node.nodeEngine import *
from core.module.object import *
from modules import *
import json
import os

from pathlib import Path

def guiJsonPaths() -> list[str]:
    source_dir = None
    for parent in Path(__file__).resolve().parents:
        if parent.name == "Source":
            source_dir = parent
            break
        elif (parent / "Source").is_dir():
            source_dir = parent / "Source"
            break
    if not source_dir:
        raise FileNotFoundError("Could not automatically locate the 'Source' directory.")
    return [str(file.resolve()) for file in source_dir.rglob("gui.json")]

def loadJson(jsonpath):
    with open(jsonpath, "r", encoding="utf-8") as f:
        object_dict = json.load(f)
    return object_dict
def getComponents(moduleDescription):
    return moduleDescription.get("components", []).keys()
def getComponentDefinition(componentsDescription, componentName):
    return componentsDescription.get(componentName)

def loadObject(name,objDescription, node_editor,jsonpath):
    object = globals()[objDescription["constructor"]](Name=name)
    container = node_editor.addContainer(name,0,0,objDescription["size"][0],objDescription["size"][1],bg_color=objDescription.get("color","#2A394A"),border_color=objDescription.get("bcolor","#00ADB5"))
    if objDescription.get("children").get("svg"):
        with open(os.path.join(jsonpath, objDescription.get("children").get("svg").get("path")), "r") as f:
            python_script = f.read()
        container.addChild("pyIcon",objDescription.get("children").get("svg").get("position")[0],objDescription.get("children").get("svg").get("position")[1],objDescription.get("children").get("svg").get("size")[0],objDescription.get("children").get("svg").get("size")[1],python_script=python_script)
    for pinName, pinDescription in objDescription.get("pins").items():
        container.addNode(pinName,pinDescription.get("position")[0],pinDescription.get("position")[1])
    return [object,container]