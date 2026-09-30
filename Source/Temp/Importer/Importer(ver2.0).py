# Since the old version is too shit and anti human, i want to create a whole new version. Bruh
# On top of that, the old one is hard to track (The main issue) while having heavy security issue 
# I have searched the better way to make the structure ( Ai + YT video )

# Son, this things can self destruct


from Temp.Data import *
import importlib
import pkgutil
import logging
import copy
import types
from typing import *


logging.basicConfig(level=logging.INFO)



class Loader:

    @staticmethod
    def LoadModule(TargetNames : Union[List[Union[str, any]], str]):
        FoundItems = []
        for Target in TargetNames:
            try:
               FoundItems.append(importlib.import_module(Target))
            except ImportError as e:
                print(f"{Target}" " does not exist due to" f"{e}")


    @staticmethod
    def LoadFromPath(TargetPaths : str, prefix : str = ""):
        FoundItems = []

        for _, modname, _ in pkgutil.iter_importers(TargetPaths):
            Target = f"{prefix}{modname}"
            try:
               FoundItems.append(importlib.import_module(Target))
            except ImportError as e:
                print(f"{Target}" " does not exist due to" f"{e}")

        return FoundItems

    @staticmethod
    def CloneImport(TargetImport, AssignName : str):
        Import = Loader.LoadModule(TargetImport)

        CloneImport = types.ModuleType(f"Assignname")
        setattr(CloneImport, "__name__", str(AssignName))

        for key, value in Import.__dict__.items():
            if key == "__name__" or "__loader__" or "__spec__":
                continue

            setattr(Import, key, value)

        return CloneImport    
   

class Modifier:

    @staticmethod
    def ApplyAttr(TargetImport, Modinfo : any):

        try:
            Import = Loader.LoadModule(TargetImport)
        except ImportError:
            print("Import can not be found from ApplyMod")

        Name = getattr(Import, "__name__")

        for ModPart, Mod in Modinfo:
            if isinstance(Mod, callable) or not isinstance(Mod, str):
                setattr(Import, str(ModPart), Mod)
                logging.info(f"{ModPart} has been replaced")
            elif isinstance(Mod, str):
                try:
                   Compile = compile(Mod)
                   exec(Compile, Import.__dict__)
                   logging.info(f"{ModPart} has been compiled and attached to the {Name}")
                except Exception as e:
                    logging.info(f" Bruh {ModPart} is shitted inserted black man disappeared")
            else:
                setattr(Import, ModPart, Mod)

        return Import


    @staticmethod
    def DeleteAttr(TargetImport,  ModNames):
        try:
           Import = Loader.LoadModule(TargetImport)
        except ImportError as e:
            logging.info(f"{e} this shit has appeared as {TargetImport} is not a thing, try harder son")

        for AttrName in ModNames:
            if AttrName:
                pass
            delattr(Import, AttrName)
            logging.info(f"{AttrName} is deleted")

        return Import


class Connector:

    @staticmethod

    def Connect():
        pass


    def Disconnect():
        pass


class HandlerForNoob:

    print("This is more automatic but u can still use manually if u are cool")
    # Handler store the log of the past things so no worry, easy things u know but this is a fixed way, however since u can change this importer, maybe u can do CoolStuff


    def __init__(self):
        pass



    def Connect(self, ImportName, TargetScript):
        Import = Loader.LoadModule(ImportName)



    


        


        

        

            

    

        
            
            






    



        




