from gui.node.nodeEngine import *
from core.module.object import *
from modules import *
import json
import os
import math
import re
import pydot
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


def loadObject(name, objDescription, node_editor, jsonpath):
    object = globals()[objDescription['constructor']](Name=name)
    return object


def loadContainer(name, objDescription, node_editor, jsonpath):
    container = node_editor.addContainer(
        name, 0, 0, objDescription['size'][0], objDescription['size'][1],
        bg_color=objDescription.get('color', '#2A394A'),
        border_color=objDescription.get('bcolor', '#00ADB5')
    )
    if objDescription.get('children') and objDescription.get('children').get('pyIcon'):
        pyicon_def = objDescription.get('children').get('pyIcon')
        icon_path = os.path.join(jsonpath, pyicon_def.get('path'))
        with open(icon_path, 'r') as f:
            python_script = f.read()
        container.addChild(
            'pyIcon', pyicon_def.get('position')[0], pyicon_def.get('position')[1],
            pyicon_def.get('size')[0], pyicon_def.get('size')[1], python_script=python_script
        )
    if objDescription.get('pins'):
        for pinName, pinDescription in objDescription.get('pins').items():
            container.addNode(pinName, pinDescription.get('position')[0], pinDescription.get('position')[1])
    return container