from core.object import *
from modules.LogicGate import *
from .parser import *
import re

# WE IGNORED THE ATTRIBUTES AND PARAMETERS
# BRUH BUT PROBLY I WILL FORGET THIS COMMENT SO UH NVM ALSO I THINK ALL THE COMPOENENTS IN THIS KINDA LEVEL OF unVerilogrize will not have any useful info in there...?

def analyse_file(filename):
    data = parse_verilog_to_pure_gates(os.path.abspath(filename))
    data = BetterDict(data)
    print("\n\nAnalyse Result:")
    print("Creator:" + str(data["creator"]))
    print("Module Number:" + str(len(data["modules"].keys())))
    for moduleKey,moduleValue in data["modules"].items():
        print("  Module Name:" + str(moduleKey))
        #print("    Module Top:" + str(moduleValue["attributes"]["top"]))
        print("  Module Src:" + str(moduleValue["attributes"]["src"]))
        print("  It Have " + str(len(moduleValue["ports"].keys())) + " IO Ports.")
        for portKey,portValue in moduleValue["ports"].items():
            print("    Port:" + str(portKey) + " " + str(portValue["direction"]) + ", have " + str(len(portValue["bits"])) + " Bit(s)")
            print("Connected to Net:",*portValue["bits"])
        print("  It Have " + str(len(moduleValue["cells"].keys())) + " Logic Cells.")
        for cellKey,cellValue in moduleValue["cells"].items():
            if cellValue["hide_name"] == 1:
                print("    Unamed Cell:")
            else:
                print("    " + cellKey + ":")
            cellType = re.findall(r"_(\w+?)(?=_)", cellValue["type"])
            print("      Cell Type:" , *cellType)
            for (PinName, pinDirection), (PinName2, pinConnection) in zip(cellValue["port_directions"].items(), cellValue["connections"].items()):
                print("        ",PinName2, pinDirection, " " , *pinConnection)
        print("    Named Nets:")
        for netKey,netValue in moduleValue["netnames"].items():
            if netValue["hide_name"] == 0:
                print("     ",netKey," ",*netValue["bits"])
    print("\n\n")
    
analyse_file("register.v")