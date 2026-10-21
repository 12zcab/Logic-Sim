from gui.node.nodeEngine import *
from core.module.object import *
from modules import *
import json
import os
import math
import re
from pathlib import Path


def guiJsonPaths() -> list[str]:
    source_dir = None
    for parent in Path(__file__).resolve().parents:
        if parent.name == 'Source':
            source_dir = parent
            break
        elif (parent / 'Source').is_dir():
            source_dir = parent / 'Source'
            break
    if not source_dir:
        raise FileNotFoundError("Could not automatically locate the 'Source' directory.")
    return [str(file.resolve()) for file in source_dir.rglob('gui.json')]


def loadJson(jsonpath):
    with open(jsonpath, 'r', encoding='utf-8') as f:
        object_dict = json.load(f)
    return object_dict


def getComponents(moduleDescription):
    return moduleDescription.get('components', []).keys()


def getComponentDefinition(componentsDescription, componentName):
    return componentsDescription.get(componentName)


def loadObject(name, objDescription, node_editor, jsonpath,x=0,y=0):
    obj = globals()[objDescription['constructor']](Name=name)
    pyIcon = None
    if objDescription.get("children"):
        if objDescription["children"].get("pyIcon"):
            with open(os.path.join(jsonpath,objDescription["children"]["pyIcon"]["path"]), 'r') as iconFile:
                pyIcon = iconFile.read()
    node = node_editor.create_node(
        title=name,
        x=x,
        y=y,
        width=objDescription['size'][0],
        height=objDescription['size'][1],
        bg_color=objDescription['color'],
        border_color=objDescription['bcolor'],
        graphic_code=pyIcon,
        metadata=obj
    )
    for key,value in objDescription["pins"].items():
        node.add_pin(key, value["position"][0], value["position"][1], color="#222222")
    return [obj,node]
