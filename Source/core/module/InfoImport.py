from object import *
from modules.Data.DataHandler import *

import inspect

# Initial by user, then loop to request further import if child object has child

def ExportObjectData(ParentObject : object.__class__.__self__, Info):
    Data = Handler().Backet

    FoundData = {"Exec" : {}, "Object" : {}}
    if Info == "All":
        for Name, Value in ParentObject.__dict__.items():
            if not FoundData[str(Value.type)]:
                FoundData[str(Value.type)] = {}

            if isinstance(Value, callable):
                FoundData[str(Value.type)][Name] = inspect.getsource(Value)
            else:
                FoundData[str(Value.type)][Name] = Value

    for Name, Value in ParentObject.__dict__.items():
        if Info[Name]: 
            FoundData[Name] = Value

    return FoundData

def ImportObjectData(ParentObject : object.__class__.__self__, Info : dict):
    Success = []
    for Name, _ in ParentObject.__dict__.items():
        if Info[Name]: 
            setattr(ParentObject, Name, Info[Name])  
            Success.append(Name) 
   
    return Success 

def Compare(ParentObject : object.__class__.__self__, CloneObject : object.__class__.__self__):
    Difference = {[ParentObject.name, CloneObject.name]}    
    for Name, Value in ParentObject.__dict__.items():
        if not Value == CloneObject.__dict__.item(Name):
            Difference[Name] = [Value, CloneObject.__dict__item(Name)]
        elif not CloneObject.__dict__.item(Name):
            Difference[Name] = "Not Exist"

    return Difference