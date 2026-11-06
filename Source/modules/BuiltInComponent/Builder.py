from core.module.object import *
from modules.Verilog import *

import json
from pathlib import *

def Build(VerilogName, ModuleName : str, SimBox : SimBox):
    if not ".json" in VerilogName:
        VerilogName = f"{VerilogName}.json"

    AboPath = Path(VerilogName).resolve()
    Object = parse_verilog_to_pure_gates(AboPath, ModuleName)
    SimBox.addObject(Object)