Description = r"""
Functions:

Create commands
Create functions
Change/ add functions in other scripts

"""

import json
import Data.DataHandler
from core.object import *
from modules import *

class Importer:
    def __init__(self, functions, scriptName):
        self.functions = functions
        self.scriptName = scriptName

    def Importer(self):
        self.Script = Loader.ScriptSearcher(self.scriptName)
        if not self.Script:
            



class Loader:
    def ScriptSearcher(scriptName):
        try:
            with open(scriptName, "x") as file:
                return file
        except FileNotFoundError or FileExistsError:
            return False

class Creator:
    # Allow user to import their assets
    


class Signal:





 