import os
import json
import tempfile
import sys
from typing import Dict, Any
from yowasp_yosys import run_yosys
import json
def parse_verilog_to_pure_gates(verilog_absolute_path: str, top_module: str = None) -> Dict[str, Any]:
    """
    Synthesizes Verilog to a pure gate-level JSON netlist.
    All DFFs, latches, and multiplexers (MUXes) are lowered into 
    elementary logic gates ($_AND_, $_OR_, $_NOT_, $_NAND_, etc.).
    """
    if not os.path.isabs(verilog_absolute_path):
        raise ValueError(f"Not Absolute Path: {verilog_absolute_path}")
    
    if not os.path.exists(verilog_absolute_path):
        raise FileNotFoundError(f"Cant Find the File: {verilog_absolute_path}")
    safe_verilog_path = verilog_absolute_path.replace('\\', '/')

    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as tmp_file:
        output_json_path = tmp_file.name.replace('\\', '/')

    try:
        yosys_commands = []
        yosys_commands.append(f"read_verilog {safe_verilog_path}")
        
        if top_module:
            yosys_commands.append(f"hierarchy -top {top_module}")
        else:
            yosys_commands.append("hierarchy -auto-top")
        
        gate_level_pipeline = (
            "proc; opt; memory; pmuxtree; "
            "techmap; simplemap; splitcells; "
            "dfflegalize -cell $_DFF_P_ 0 -cell $_DFF_PP0_ 0; "
            "abc -g gates; "
            "opt; check"
        )
        
        yosys_commands.append(gate_level_pipeline)
        yosys_commands.append(f"write_json {output_json_path}")
        
        yosys_args = []
        for cmd in yosys_commands:
            yosys_args.extend(["-p", cmd])

        print(f"[*] Parsing to pure gate netlist: {safe_verilog_path}")
        
        exit_code = run_yosys(argv=yosys_args)
        if exit_code != 0:
            raise RuntimeError(f"Yosys Failed Code: {exit_code}")
            
        with open(output_json_path, "r", encoding="utf-8") as f:
            gate_netlist_dict = json.load(f)
            
        return gate_netlist_dict

    finally:
        if os.path.exists(output_json_path):
            os.remove(output_json_path)

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    target_register_path = os.path.join(current_dir, "register.v")
            
    try:
        netlist_data = parse_verilog_to_pure_gates(target_register_path)
        with open("output.json", "w") as f:
            json.dump(netlist_data, f, indent=4)
    except Exception as error:
        print(f"[-] Error happened : {error}", file=sys.stderr)