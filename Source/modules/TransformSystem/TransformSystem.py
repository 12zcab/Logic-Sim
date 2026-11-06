from typing import Dict, Any, List, Union
# Assuming these custom modules exist in your framework workspace
# from core.module.object import *
# from modules.LogicGate import *

class Number:
    def __init__(self, SimBox: Any):
        self.SimBox = SimBox
        self.Objects = SimBox.Components

    def InitLogic(self, Objects: Any, Logic: List[dict], Changes: List[dict]):
        for Object in self.Objects:
            if hasattr(Objects, Object.name):  # Use hasattr to verify if a matching name attribute exists
                Object.Logic = Logic
                Object.Change = Changes
        
    def Activate(self, Objects: List[Any]):
        for Object in Objects:
            if Object not in self.Objects:
                return
        
            # If Object.Logic is a list of dictionaries containing Pin mapping configuration states
            for item in Object.Logic: 
                for Pin, New in item.items():
                    # Safely handle the pin mapping check if IOs dictionary exists
                    if hasattr(Object, "IOs") and Pin in Object.IOs and Object.IOs[Pin]:
                        if hasattr(New, Pin):
                            setattr(Object, Pin, getattr(New, Pin))

            # Fixed parameter assignment syntax layout matching logic gate evaluations
            for item in Object.Change:
                for Pin, Con in item.items():
                    if hasattr(Object, "IOs") and Pin in Object.IOs:
                        current_io_val = Object.IOs[Pin]
                        if current_io_val in Con:
                            setattr(Object, Pin, Con[current_io_val])

    def Change(self, Object: Any, ListName: str, ValueDict: dict):
        if Object not in self.Objects:
            return
        if not hasattr(Object, ListName):
            return  

        target_list = getattr(Object, ListName)
        if not isinstance(target_list, list):
            return

        for Key, Value in ValueDict.items():
            # Check if key exists inside the target item configuration structures
            found = False
            for item in target_list:
                if isinstance(item, dict) and Key in item:
                    item[Key] = Value
                    found = True
                    break
            if not found:
                target_list.append({Key: Value})


class Bool:
    def __init__(self, SimBox: Any):
        self.SimBox = SimBox
        self.Objects = SimBox.Objects

    def initLogic(self, Objects: Any, Logic: List[Any]):
        for Object in self.Objects:
            if hasattr(Objects, Object.name):
                Object.BoolLogic = Logic

    def Activate(self, Objects: Any):
        for Object in self.Objects:
            if hasattr(Objects, Object.name) and getattr(Object, "BoolLogic", None):
                for item in Object.BoolLogic:
                    # Expecting item to be a tuple/list structured as (IOs, Gate)
                    if len(item) < 2:
                        continue
                    IOs, Gate = item[0], item[1]
                    
                    if not isinstance(IOs, list):
                        IOs = [IOs]
                        
                    is_complete = True
                    for IO in IOs:
                        if hasattr(Object, "Net") and (IO not in Object.Net or not Object.Net[IO]):
                            print(f"IO {IO} is not completed")
                            is_complete = False
                            break 

                    if is_complete and Gate:
                        # Evaluates or ticks the LogicGate runtime instance if active
                        if hasattr(Gate, "evaluate"):
                            Gate.evaluate()
                        elif callable(Gate):
                            Gate()


class String:
    def __init__(self, SimBox: Any):
        self.SimBox = SimBox
        # Fixed potential attribute initialization referencing matching properties
        self.Objects = getattr(SimBox, "Components", getattr(SimBox, "Objects", []))

    def initLogic(self, Objects: Any, Logic: List[dict], Changes: List[Any]):  
        for Object in self.Objects:
            if hasattr(Objects, Object.name):
                Object.StringLogic = Logic
                Object.StringChange = Changes  # Fixed syntax typo: replaced minus sign (-) with assignment (=)

    def Activate(self, Objects: Any):
        for Object in self.Objects:
            if not hasattr(Objects, Object.name) or not getattr(Object, "StringLogic", None):
                continue

            for item in Object.StringLogic:
                for Int, Con in item.items():
                    if not hasattr(Object, Int):
                        continue
                    current_val = getattr(Object, Int)
                    if hasattr(Con, current_val):
                        setattr(Object, Int, getattr(Con, current_val))

            if hasattr(Object, "StringChange") and Object.StringChange:
                for item in Object.StringChange:
                    for Int, Info in item.items():
                        if hasattr(Object, Int) and hasattr(Info, "Con") and hasattr(Info, "Change"):
                            if getattr(Object, Int) == Info.Con:
                                setattr(Object, Int, Info.Change)