from core import *
from modules.LogicGate import *
from modules.FlipFlop import *
from .parser import *
import re
from collections import defaultdict
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
def parseFileIntoObject(filename):
    data = parse_verilog_to_pure_gates(os.path.abspath(filename))
    data = BetterDict(data)
    print("\n\nCreating Module:")
    print("Creator:" + str(data["creator"]))
    print("Module Number:" + str(len(data["modules"].keys())))
    resultModules = []
    for moduleKey,moduleValue in data["modules"].items():
        print("  Module Name:" + str(moduleKey))
        IOArray = []
        InnerBlocks = []
        Nets = defaultdict(lambda: Net())
        #print("    Module Top:" + str(moduleValue["attributes"]["top"]))
        print("  Module Src:" + str(moduleValue["attributes"]["src"]))
        print("  It Have " + str(len(moduleValue["ports"].keys())) + " IO Ports.")
        for portKey,portValue in moduleValue["ports"].items():
            print("    Port:" + str(portKey) + " " + str(portValue["direction"]) + ", have " + str(len(portValue["bits"])) + " Bit(s)")
            if len(portValue["bits"]) == 1:
                IndividualIO = IO(str(portKey))
                if not Nets[str(moduleKey) + "_" + str(portValue["bits"][0])]:
                    Nets[str(moduleKey) + "_" + str(portValue["bits"][0])] = Net(str(moduleKey) + "_" + str(portValue["bits"][0]))
                IndividualIO.Net = Nets[str(moduleKey) + "_" + str(portValue["bits"][0])]
                IOArray.append(IndividualIO)
            else:
                for i in range(len(portValue["bits"])):
                    IndividualIO = IO(str(portKey) + "_" + str(i))
                    if not Nets[str(moduleKey) + "_" + str(portValue["bits"][i])]:
                        Nets[str(moduleKey) + "_" + str(portValue["bits"][i])] = Net(str(moduleKey) + "_" + str(portValue["bits"][i]))
                    IndividualIO.Net = Nets[str(moduleKey) + "_" + str(portValue["bits"][i])]
                    IOArray.append(IndividualIO)
            print("Connected to Net:",*portValue["bits"])
        print("  It Have " + str(len(moduleValue["cells"].keys())) + " Logic Cells.")
        for cellKey,cellValue in moduleValue["cells"].items():
            if cellValue["hide_name"] == 1:
                print("    Unamed Cell:")
            else:
                print("    " + cellKey + ":")
            cellType = re.findall(r"_(\w+?)(?=_)", cellValue["type"])
            print("      Cell Type:" , *cellType)
            match cellType[0]:
                case "NAND":
                    IndividualComponent = NandGate(cellKey)
                case "ORNOT":
                    IndividualComponent = OrNotGate(cellKey)
                case "DFF":
                    IndividualComponent = PP0_DFF(cellKey)
            for (PinName, pinConnection) in cellValue["connections"].items():
                IndividualComponent.IO[PinName].connectNet(Nets[str(moduleKey) + "_" + pinConnection[0]])
            InnerBlocks.append(IndividualComponent)
        print("    Named Nets:")
        for netKey,netValue in moduleValue["netnames"].items():
            if netValue["hide_name"] == 0:
                print("     ",netKey," ",*netValue["bits"])
            for id in netValue["bits"]:
                Nets[str(moduleKey) + "_" + str(id)].Name = netKey
        resultModules.append(Module(str(moduleKey),IOArray,InnerBlocks))
    print("\n\n")
    return resultModules[0]
#analyse_file("register.v")


"""
create register parseFileIntoObject("register.v")
create clkbt keyboard_button("clk","[")
create rstbt keyboard_button("rst","]")
create enbt keyboard_button("en",'\\')
create d0 keyboard_button("d0","1")
create d1 keyboard_button("d1","2")
create d2 keyboard_button("d2","3")
create d3 keyboard_button("d3","4")
create d4 keyboard_button("d4","5")
create d5 keyboard_button("d5","6")
create d6 keyboard_button("d6","7")
create d7 keyboard_button("d7","8")
clkbt.IO.OUT >> register.IO.clk
rstbt.IO.OUT >> register.IO.rst
enbt.IO.OUT >> register.IO.en
d0.IO.OUT >> register.IO.d_0
d1.IO.OUT >> register.IO.d_1
d2.IO.OUT >> register.IO.d_2
d3.IO.OUT >> register.IO.d_3
d4.IO.OUT >> register.IO.d_4
d5.IO.OUT >> register.IO.d_5
d6.IO.OUT >> register.IO.d_6
d7.IO.OUT >> register.IO.d_7
create log Logger("logger",["CLK","RST","EN","I0","I1","I2","I3","I4","I5","I6","I7","O0","O1","O2","O3","O4","O5","O6","O7"],[clkbt.IO.OUT,rstbt.IO.OUT,enbt.IO.OUT,register.IO.d_0,register.IO.d_1,register.IO.d_2,register.IO.d_3,register.IO.d_4,register.IO.d_5,register.IO.d_6,register.IO.d_7,register.IO.q_0,register.IO.q_1,register.IO.q_2,register.IO.q_3,register.IO.q_4,register.IO.q_5,register.IO.q_6,register.IO.q_7])
"""