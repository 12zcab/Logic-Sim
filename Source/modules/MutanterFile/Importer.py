from pathlib import Path
from Data import DataHandler
import types
import Mutanter
import Importer

Handler = Mutanter.Handler()
Handler.Connect(Importer)


class Connector:
    @staticmethod
    def LoadFileFromPath(Targets, FileType=None):

        FoundItems = {}
        Targets = [Targets] if not isinstance(Targets, list) else Targets

        for Target in Targets:
            _Path = Path(Target).resolve()
            FoundItems[str(Target)] = []
            if _Path.is_dir():
                for item_Path in _Path.iterdir():
                    with item_Path.open("r", encoding="rb") as file:
                        FoundItems[str(Target)].append(file)
            else:
                with _Path.open("r", encoding="rb") as file:
                    FoundItems[str(Target)].append(file)

        return FoundItems
        

    def Connect():
        pass

    def Disconnect():
        pass

class Modifier:

    def MakeModule():
        pass








