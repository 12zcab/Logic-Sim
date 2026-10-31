import os
import json
from pathlib import Path

class Loader:

    @staticmethod
    def GetData(FileName, TableName):
        FilePath = Loader.FindPath(FileName)
        if not FilePath or not os.path.exists(FilePath):
            return []
        
        with open(FilePath, "r", encoding="utf-8") as f:
            try:
                items = json.load(f)
            except json.JSONDecodeError:
                return []
        
        if isinstance(items, dict):
            return items.get(TableName, [])
        elif isinstance(items, list):
            found_table = []
            for item in items:
                if isinstance(item, dict) and item.get("TableName") == TableName:
                    found_table.append(item)
            return found_table
        return []

    @staticmethod
    def FindPath(Name: str):
        path_obj = Path(Name)
        if path_obj.is_absolute():
            return path_obj

        pure_name = path_obj.name
        for path in Path(".").rglob(pure_name):
            return path.absolute()
            
        return path_obj.absolute()


class Handler:

    def __init__(self):
        self.Backet = {}

    def Store(self, data = None, Filename: str = "save_data.json"):
        filepath = Loader.FindPath(Filename)
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        data_to_store = data if data is not None else self.Backet
        if not isinstance(data_to_store, (list, dict)):
            data_to_store = [data_to_store]

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data_to_store, f, indent=4)
        return True
        
    @staticmethod
    def Retreive(TableName, Filename: str):
        return Loader.GetData(Filename, TableName)
