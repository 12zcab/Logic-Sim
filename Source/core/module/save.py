import json
import os
from bidict import bidict
from .DataHandler import Handler, Loader

def get_logic_class():
    """Helper to dynamically import the Logic class/enum from the project."""
    try:
        from gui.LogicSim.Logic import Logic
        return Logic
    except ImportError:
        try:
            from modules.LogicSim.Logic import Logic
            return Logic
        except ImportError:
            return None

def serialize_value(val):
    """Recursively converts primitives, lists, BetterDicts, dictionaries, and Logic enums into JSON-serializable formats."""
    Logic = get_logic_class()
    if isinstance(val, (str, int, float, bool, type(None))):
        return val
    elif Logic and isinstance(val, Logic):
        return {"__type__": "Logic", "value": val.name if hasattr(val, "name") else str(val)}
    elif hasattr(val, "name") and not callable(val):
        return {"__type__": "Logic", "value": val.name}
    elif isinstance(val, (dict, object)) and type(val).__name__ in ["BetterDict", "dict"]:
        try:
            return {str(k): serialize_value(v) for k, v in val.items()}
        except Exception:
            return str(val)
    elif isinstance(val, list):
        return [serialize_value(item) for item in val]
    else:
        return str(val)

def deserialize_value(val):
    """Recursively restores JSON data back into primitives, lists, dictionaries, and Logic enums."""
    Logic = get_logic_class()
    if isinstance(val, dict):
        if val.get("__type__") == "Logic":
            v_name = val.get("value")
            if Logic and hasattr(Logic, v_name):
                return getattr(Logic, v_name)
            return v_name
        else:
            return {k: deserialize_value(v) for k, v in val.items()}
    elif isinstance(val, list):
        return [deserialize_value(item) for item in val]
    elif Logic and isinstance(val, str) and val in ["ONE", "ZERO", "X", "Z"]:
        if hasattr(Logic, val):
            return getattr(Logic, val)
    return val

class Exporter:
    def __init__(self, Data, File, Name: str, sample_factory=None):
        self.Data = Data
        self.Name = Name
        self.JSon = File
        self.Handler = Handler()
        self.Backet = {}

    def Catch(self, Targets="All", Loop=None):
        app = self.Data
        
        # 1. Clear / Delete the existing JSON file before saving fresh data
        if os.path.exists(self.JSon):
            try:
                os.remove(self.JSon)
            except Exception:
                pass

        # 2. Map every active logic object and node object to stable index IDs
        logic_to_id = {}
        node_obj_to_id = {}
        nodes_data = []
        
        active_editor_nodes = set()
        if hasattr(app, "node_editor") and hasattr(app.node_editor, "nodes"):
            active_editor_nodes = set(app.node_editor.nodes)

        # Blacklist system attributes that should never be serialized as component settings
        EXCLUDED_ATTRIBUTES = {"simBox", "IO", "node", "canvas", "Parent", "parent", "Name", "name", "updateFunction"}

        if hasattr(app, "logicToNode"):
            for idx, (logic_obj, node_obj) in enumerate(app.logicToNode.items()):
                if active_editor_nodes and node_obj not in active_editor_nodes:
                    continue

                logic_to_id[id(logic_obj)] = idx
                node_obj_to_id[id(node_obj)] = idx
                
                # Capture custom component attributes/states (ROM tables, Flip-Flop states, Latches, etc.)
                attributes = {}
                for attr in dir(logic_obj):
                    if attr.startswith("_") or attr in EXCLUDED_ATTRIBUTES or callable(getattr(logic_obj, attr)):
                        continue
                    try:
                        val = getattr(logic_obj, attr)
                        if isinstance(val, (str, int, float, bool, list, dict)) or type(val).__name__ == "BetterDict" or (get_logic_class() and isinstance(val, get_logic_class())):
                            serialized = serialize_value(val)
                            if serialized is not None:
                                attributes[attr] = serialized
                    except Exception:
                        pass

                nodes_data.append({
                    "id": idx,
                    "constructor": logic_obj.__class__.__name__,
                    "name": getattr(logic_obj, "Name", "Unknown"),
                    "x": getattr(node_obj, "x", 0),
                    "y": getattr(node_obj, "y", 0),
                    "angle": getattr(node_obj, "angle", 0.0),
                    "attributes": attributes
                })
        self.Backet["saved_nodes"] = nodes_data

        # 3. Save wires, pin IO mappings, and Net signal values / statuses
        wires_data = []
        nets_data = []
        
        if hasattr(app, "node_editor"):
            editor = app.node_editor
            
            if hasattr(editor, "wires"):
                for wire in editor.wires:
                    try:
                        start_node_id = None
                        if wire.start_pin and wire.start_pin.owner:
                            start_node_id = node_obj_to_id.get(id(wire.start_pin.owner))

                        end_node_id = None
                        if wire.end_pin and wire.end_pin.owner:
                            end_node_id = node_obj_to_id.get(id(wire.end_pin.owner))

                        wires_data.append({
                            "start_node": start_node_id,
                            "start_pin": wire.start_pin.name if wire.start_pin else None,
                            "start_pos": list(wire.start_pos) if wire.start_pos else None,
                            "end_node": end_node_id,
                            "end_pin": wire.end_pin.name if wire.end_pin else None,
                            "end_pos": list(wire.end_pos) if wire.end_pos else None,
                            "vertices": [list(v) for v in wire.vertices],
                            "color": wire.color,
                            "width": wire.width
                        })
                    except Exception:
                        pass
            
            if hasattr(app, "logicNetToNodeNet"):
                for sim_net, gui_net in app.logicNetToNodeNet.items():
                    net_pins_info = []
                    for pin in gui_net.pins:
                        p_node_id = node_obj_to_id.get(id(pin.owner)) if pin.owner else None
                        if p_node_id is not None:
                            net_pins_info.append({
                                "node_id": p_node_id,
                                "pin_name": pin.name
                            })
                    
                    nets_data.append({
                        "id": gui_net.id,
                        "name": getattr(gui_net, "name", f"NET_{gui_net.id}"),
                        "value": serialize_value(getattr(sim_net, "Value", None)),
                        "pins": net_pins_info
                    })

        self.Backet["saved_wires"] = wires_data
        self.Backet["saved_nets"] = nets_data
        return self.Backet

    def Store(self):  
        self.Handler.Backet = {self.Name: self.Backet}
        self.Handler.Store(Filename = self.JSon)
        self.Backet = {}

class Importer: 
    def __init__(self, FileName: str, TableName, Data, spawn_callback=None):  
        self.File = FileName  
        self.Data = Data
        self.Table = TableName  
        self.SpawnCallback = spawn_callback  

    def Import(self, Table=None, Loop=None):
        if Table is None:
            raw_data = Handler.Retreive(self.Table, self.File)
            if not raw_data:
                raw_data = Loader.GetData(self.File.replace(".json", ""), self.Table)
            Table = raw_data

        if isinstance(Table, dict):
            data_to_import = Table.get(self.Table, Table)
            if not isinstance(data_to_import, dict):
                data_to_import = Table

            spawned_nodes_map = {}
            logic_objects = []

            # 1. Clear existing scene items before loading
            if hasattr(self.Data, "node_editor") and hasattr(self.Data.node_editor, "clear"):
                self.Data.node_editor.clear()

            # 2. Recreate nodes, angles, and custom attribute states (ROM tables, FlipFlops, Latches)
            if "saved_nodes" in data_to_import and self.SpawnCallback:
                for node_info in data_to_import["saved_nodes"]:
                    node_id = node_info.get("id")
                    constructor = node_info.get("constructor")
                    x = node_info.get("x", 0)
                    y = node_info.get("y", 0)
                    angle = node_info.get("angle", 0.0)
                    attributes = node_info.get("attributes", {})

                    logic_obj, node_obj = self.SpawnCallback(constructor, x, y, angle)
                    
                    if logic_obj and node_obj:
                        logic_objects.append(logic_obj)
                        for attr, val in attributes.items():
                            if hasattr(logic_obj, attr):
                                restored_val = deserialize_value(val)
                                try:
                                    # Avoid overwriting internal BetterDict objects like `IO` entirely; 
                                    # instead, write values safely to attributes.
                                    current_attr = getattr(logic_obj, attr, None)
                                    if type(current_attr).__name__ == "BetterDict" and isinstance(restored_val, dict):
                                        for sub_k, sub_v in restored_val.items():
                                            if hasattr(current_attr, sub_k):
                                                setattr(current_attr, sub_k, sub_v)
                                            else:
                                                current_attr[sub_k] = sub_v
                                    else:
                                        setattr(logic_obj, attr, restored_val)
                                except Exception:
                                    pass

                        if hasattr(logic_obj, "update"):
                            logic_obj.update()

                        spawned_nodes_map[node_id] = node_obj

            # 3. Recreate wires and reconnect them to node pins
            if "saved_wires" in data_to_import and hasattr(self.Data, "node_editor"):
                try:
                    from gui.node.nodeEngine import Wire, WireNet
                except ImportError:
                    try:
                        from modules.Data.nodeEngine import Wire, WireNet
                    except ImportError:
                        Wire = None
                        WireNet = None

                if Wire is not None:
                    editor = self.Data.node_editor

                    for wire_info in data_to_import["saved_wires"]:
                        s_node_id = wire_info.get("start_node")
                        s_pin_name = wire_info.get("start_pin")
                        start_pos = wire_info.get("start_pos")
                        
                        e_node_id = wire_info.get("end_node")
                        e_pin_name = wire_info.get("end_pin")
                        end_pos = wire_info.get("end_pos")
                        
                        vertices = wire_info.get("vertices", [])
                        color = wire_info.get("color", "#38bdf8")
                        width = wire_info.get("width", 3.5)

                        start_pin = None
                        if s_node_id is not None and s_node_id in spawned_nodes_map:
                            node_obj = spawned_nodes_map[s_node_id]
                            if node_obj and hasattr(node_obj, "pins"):
                                start_pin = next((p for p in node_obj.pins if p.name == s_pin_name), None)

                        end_pin = None
                        if e_node_id is not None and e_node_id in spawned_nodes_map:
                            node_obj = spawned_nodes_map[e_node_id]
                            if node_obj and hasattr(node_obj, "pins"):
                                end_pin = next((p for p in node_obj.pins if p.name == e_pin_name), None)

                        new_wire = Wire(
                            wire_id=f"wire_{len(editor.wires)+1}",
                            start_pin=start_pin,
                            start_pos=tuple(start_pos) if start_pos else None,
                            color=color,
                            width=width
                        )
                        new_wire.end_pin = end_pin
                        new_wire.end_pos = tuple(end_pos) if end_pos else None
                        new_wire.vertices = [tuple(v) for v in vertices]

                        editor.wires.append(new_wire)

                    # 4. Rebuild NetEngine simulation nets and restore Net States/Values & Names
                    if hasattr(editor, "rebuild_nets"):
                        editor.rebuild_nets()

                    saved_nets = data_to_import.get("saved_nets", [])
                    if saved_nets and hasattr(self.Data, "logicNetToNodeNet") and hasattr(editor, "engine"):
                        for net_meta in saved_nets:
                            saved_name = net_meta.get("name")
                            saved_val = deserialize_value(net_meta.get("value"))
                            saved_pin_refs = net_meta.get("pins", [])
                            
                            for net_obj in editor.engine.nets.values():
                                match_count = 0
                                for p in net_obj.pins:
                                    p_nid = None
                                    for n_id, n_obj in spawned_nodes_map.items():
                                        if p.owner == n_obj:
                                            p_nid = n_id
                                            break
                                    if any(ref["node_id"] == p_nid and ref["pin_name"] == p.name for ref in saved_pin_refs):
                                        match_count += 1
                                
                                if match_count > 0 and match_count == len(net_obj.pins) == len(saved_pin_refs):
                                    net_obj.name = saved_name
                                    
                                    sim_net = self.Data.logicNetToNodeNet.inv.get(net_obj)
                                    if sim_net and saved_val is not None:
                                        sim_net.Value = saved_val
                                        if hasattr(sim_net, "resolve"):
                                            sim_net.resolve()
                                    break

                    # 5. Trigger update pass on all restored logic objects and simulation boxes
                    for logic_obj in logic_objects:
                        if hasattr(logic_obj, "update"):
                            try:
                                logic_obj.update()
                            except Exception:
                                pass

                    if hasattr(self.Data, "simBox") and hasattr(self.Data.simBox, "expandNet"):
                        try:
                            self.Data.simBox.expandNet()
                        except Exception:
                            pass

                    if hasattr(editor, "redraw_all"):
                        editor.redraw_all()

            return self.Data

        return Table