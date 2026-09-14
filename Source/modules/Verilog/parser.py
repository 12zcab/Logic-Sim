import os
import json
import tempfile
import sys
from pprint import pprint
from typing import Dict, Any
from yowasp_yosys import run_yosys

def parse_verilog_to_level3_mux(verilog_absolute_path: str, top_module: str = None) -> Dict[str, Any]:
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
        level3_pipeline = "proc; opt; memory; pmuxtree; techmap; simplemap; splitcells; opt; check"
        yosys_commands.append(level3_pipeline)
        yosys_commands.append(f"write_json {output_json_path}")
        
        yosys_args = []
        for cmd in yosys_commands:
            yosys_args.extend(["-p", cmd])

        print(f"[*] Parsing: {safe_verilog_path}")
        
        exit_code = run_yosys(argv=yosys_args)
        if exit_code != 0:
            raise RuntimeError(f"Yosys Failed Code: {exit_code}")
            
        with open(output_json_path, "r", encoding="utf-8") as f:
            level3_dict = json.load(f)
            
        return level3_dict

    finally:
        if os.path.exists(output_json_path):
            os.remove(output_json_path)

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    target_register_path = os.path.join(current_dir, "register.v")
            
    try:
        netlist_data = parse_verilog_to_level3_mux(target_register_path)
        pprint(netlist_data, indent=4, width=120, depth=None)
                
    except Exception as error:
        print(f"[-] Error happened : {error}", file=sys.stderr)
