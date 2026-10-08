# This put different file type content into a module assigned by user
# an extend version of mutanter

from pathlib import Path
import types, importlib
import Mutanter
import Transformer

# For different type of folder

Handler = Mutanter.Handler()
Handler.Connect(Transformer)


def GetFilePathFromFolder(Folders, FileName : str = None, FileType : str =None):
    FoundItems = {}
    Folders = [Folders] if not isinstance(Folders, list) else Folders

    for Folder in Folders:
        FolderPath = Path(Folder).resolve()

        if not FileType.startswith("."):
            FileType = f".{FileType}"

        for File in FolderPath.iterdir():
            if Path(File).resolve().name == FileName:
                if Path(File).resolve().suffix == FileType:
                    FoundItems[FileName]= Path(File).resolve()
                else:
                    print( F" File Match require name : {FileName} but not the type requested : {FileType}")
            else:
                print(f"{FileName} can not be found in {Folder}")
        
   
    return FoundItems 

def ReadFile(Paths):
    ReadItems = {}
    for FilePath in Paths:

        path = Path(FilePath)

        if path.suffix in [".txt" , ".py" , ".mod" , ".log"]:
            ReadItems.setdefault(path.name) = path.read_text(encoding="utf-8")
    
        if path.suffix == ".json":
            ReadItems.setdefault(path.name) = path.read_text(encoding="utf-8")
        else: 
            ReadItems.setdefault(path.name) = path.read_bytes

    return ReadItems


def Transform(Reads, ModuleName):
    ReturnRef = {}
    File = types.ModuleType(ModuleName)

    for Name, Read in Reads.items():
        setattr(File, Name, Read)
        ReturnRef[Name] = Read


def UpdateData(NewDataName , ModuleName : str, path : str, OldDataName = None):

    if not isinstance(NewDataName, dict):
        NewDataName = {NewDataName}

    if not isinstance(NewDataName, dict):
        NewDataName = {NewDataName}

    File = ReadFile(path)


    if OldDataName:
        for OldName in OldDataName:
            for NewName in NewDataName:
                if NewName == OldName:
                    NewData = importlib.import_module(ModuleName).__getattr__(NewName)
                    File.replace(OldName, NewData)
                else:
                    File.update({NewName : NewData})