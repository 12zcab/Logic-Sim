from object import *

# Initial by user, then loop to request further import if child object has child
def ExportObjectData(ParentObject : object.__class__.__self__, Info : list):
    FoundData = {}
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