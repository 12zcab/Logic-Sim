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
    
    print("\n" + "=" * 80)
    print(" VERILOG NETLIST CONSTRUCTOR DEBUGGER")
    print("=" * 80)
    
    resultModules = []
    for moduleKey, moduleValue in data["modules"].items():
        print(f"\n[+] Building Module: '{moduleKey}'")
        IOArray = []
        InnerBlocks = []
        Nets = {}

        def get_net(bit_id):
            net_key = f"{moduleKey}_{bit_id}"
            if net_key not in Nets:
                Nets[net_key] = Net(net_key)
            return Nets[net_key]

        # -----------------------------------------------------------------
        # 1. BUILD MODULE IO PORTS
        # -----------------------------------------------------------------
        print("\n  --- [1/3] Module Boundary IO Ports ---")
        for portKey, portValue in moduleValue["ports"].items():
            direction = portValue["direction"]
            bits = portValue["bits"]
            print(f"  Port '{portKey}' ({direction}, {len(bits)} bit(s)) -> Yosys Bits: {bits}")
            
            if len(bits) == 1:
                ind_io = IO(str(portKey))
                net = get_net(bits[0])
                ind_io.connectNet(net)
                IOArray.append(ind_io)
                print(f"    -> Pin '{portKey}' linked to Net '{net.Name}' [ID: {hex(id(net))}]")
            else:
                for i, bit_id in enumerate(bits):
                    io_name = f"{portKey}_{i}"
                    ind_io = IO(io_name)
                    net = get_net(bit_id)
                    ind_io.connectNet(net)
                    IOArray.append(ind_io)
                    print(f"    -> Pin '{io_name}' linked to Net '{net.Name}' [ID: {hex(id(net))}]")

        # -----------------------------------------------------------------
        # 2. INSTANTIATE LOGIC CELLS
        # -----------------------------------------------------------------
        print("\n  --- [2/3] Instantiating Logic Cells ---")
        for cellKey, cellValue in moduleValue["cells"].items():
            raw_type = cellValue["type"]
            cellType = re.findall(r"_(\w+?)(?=_)", raw_type)
            gate_type = cellType[0] if cellType else raw_type

            match gate_type:
                case "NAND":
                    ind_comp = NandGate(cellKey)
                case "ORNOT":
                    ind_comp = OrNotGate(cellKey)
                case "DFF":
                    ind_comp = PP0_DFF(cellKey)
                case _:
                    print(f"  [!] UNHANDLED CELL TYPE: '{raw_type}' (parsed: '{gate_type}') on cell '{cellKey}'")
                    continue

            print(f"  Cell '{cellKey}' ({gate_type}):")
            for pinName, pinConnection in cellValue["connections"].items():
                bit_id = pinConnection[0]
                net = get_net(bit_id)
                if pinName in ind_comp.IO:
                    ind_comp.IO[pinName].connectNet(net)
                    print(f"    -> Pin '{pinName}' -> Net '{net.Name}' [ID: {hex(id(net))}]")
                else:
                    print(f"    [!] ERROR: Cell '{cellKey}' does NOT have pin '{pinName}'!")

            InnerBlocks.append(ind_comp)

        # -----------------------------------------------------------------
        # 3. APPLY NET NAMES
        # -----------------------------------------------------------------
        print("\n  --- Net Naming ---")
        for netKey, netValue in moduleValue["netnames"].items():
            for bit_id in netValue["bits"]:
                net_obj = get_net(bit_id)
                if netValue["hide_name"] == 0:
                    net_obj.Name = netKey

        mod = Module(str(moduleKey), IOArray, InnerBlocks)
        resultModules.append(mod)

        # -----------------------------------------------------------------
        # 4. TOPOLOGY AUDIT REPORT
        # -----------------------------------------------------------------
        print("\n  " + "=" * 70)
        print("  NETLIST TOPOLOGY AUDIT REPORT")
        print("  " + "=" * 70)
        
        isolated_nets = 0
        floating_ios = 0

        print("\n  [Boundary IO Pins -> Connected Internal Pins]:")
        for io in mod.IO.values():
            if io.Net is None:
                print(f"    [!] ERROR: IO '{io.Name}' has NO NET attached!")
                floating_ios += 1
            else:
                connected = [
                    f"{pin.parent.Name}.{pin.Name}" if pin.parent else f"MODULE_IO.{pin.Name}"
                    for pin in io.Net.IO
                ]
                print(f"    Port '{io.Name:<10}' -> Net '{io.Net.Name}' [ID: {hex(id(io.Net))}] | Members ({len(connected)}): {connected}")

        print("\n  [All Internal Nets Audit]:")
        for net_key, net in Nets.items():
            connected = [
                f"{pin.parent.Name}.{pin.Name}" if pin.parent else f"MODULE_IO.{pin.Name}"
                for pin in net.IO
            ]
            
            warning = ""
            if len(connected) <= 1:
                warning = " <-- [!] WARNING: ISOLATED NET (1 or 0 pins attached)"
                isolated_nets += 1
            
            print(f"    Net '{net.Name:<15}' [Key: {net_key:<10} | ID: {hex(id(net))}] -> Pins ({len(connected)}): {connected}{warning}")

        print(f"\n  [Audit Summary]")
        print(f"    - Total Internal Components : {len(InnerBlocks)}")
        print(f"    - Total Nets Created       : {len(Nets)}")
        print(f"    - Floating Module IOs      : {floating_ios}")
        print(f"    - Isolated Nets            : {isolated_nets}")
        print("  " + "=" * 70 + "\n")

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
create log Logger("logger", ["CLK", "RST", "FF0_R", "R_PIN", "INV_A", "RST_N", "M_QY", "M_QMY", "S_SIn", "S_RIn", "S_QMY", "S_QY"], [clkbt.IO.OUT,rstbt.IO.OUT,register.child["$auto$ff.cc:337:slice$79"].IO.R,register.child["$auto$ff.cc:337:slice$79"].IO.R,register.child["$auto$ff.cc:337:slice$79"].child["RstInv"].IO.A,register.child["$auto$ff.cc:337:slice$79"].child["RstInv"].IO.Y,register.child["$auto$ff.cc:337:slice$79"].child["M_QY"].IO.Y,register.child["$auto$ff.cc:337:slice$79"].child["M_QMY"].IO.Y,register.child["$auto$ff.cc:337:slice$79"].child["S_SIn"].IO.Y,register.child["$auto$ff.cc:337:slice$79"].child["S_RIn"].IO.Y,register.child["$auto$ff.cc:337:slice$79"].child["S_QMY"].IO.Y,register.child["$auto$ff.cc:337:slice$79"].child["S_QY"].IO.Y])
"""