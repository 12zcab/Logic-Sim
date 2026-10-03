from ..node.nodeEngine import *
from ...core.module.object import *
from ...modules import *
import json
import os
def loadObjectFromJson(jsonpath,objectName):
    with open(jsonpath, "r", encoding="utf-8") as f:
        object_dict = json.load(f)
    return object_dict.get("components").get(objectName)


def loadObject(name,objDescription, node_editor,jsonpath):
    object = globals()[objDescription["constructor"]](Name=objDescription["name"])
    container = node_editor.addContainer(name,0,0,objDescription["gridW"],objDescription["gridH"],bg_color=objDescription.get("color","#2A394A"),border_color=objDescription.get("bcolor","#00ADB5"))
    if objDescription.get("children").get("svg"):
        container.addChild("svg",objDescription.get("children").get("svg").get("position")[0],objDescription.get("children").get("svg").get("position")[1],objDescription.get("children").get("svg").get("size")[0],objDescription.get("children").get("svg").get("size")[1],svg_data=os.path.join(jsonpath, objDescription.get("children").get("svg").get("path")))
    for pinName, pinDescription in objDescription.get("children").get("pins").items():
        container.addNode(pinName,pinDescription.get("position")[0],pinDescription.get("position")[1])