from MutanterFile import Mutanter
Handler = Mutanter.Handler()

import Source
import TVA
import importlib
from pathlib import Path

File_Path = Path(Source).resolve()

AllItems = importlib.import_module(File_Path)

for Item in File_Path:
    Handler.Connect([Item]) = TVA