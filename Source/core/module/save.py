import os
from .DataHandler import Handler, Loader
from .object import Component, Module, IO, export_value, import_value


class Exporter:
    def __init__(self, Data, File, Name: str, sample_factory=None):
        self.Data = Data
        self.Name = Name
        self.JSon = File
        self.Handler = Handler()
        self.Backet = {}

    def Catch(self, Targets="All", Loop=None):
        app = self.Data

        if os.path.exists(self.JSon):
            try:
                os.remove(self.JSon)
            except Exception:
                pass

        saved_objects = []
        saved_nodes = []

        objects_to_save = []
        if hasattr(app, "logicToNode") and app.logicToNode:
            objects_to_save = list(app.logicToNode.keys())
        elif hasattr(app, "simBox") and hasattr(app.simBox, "Objects"):
            for obj in app.simBox.Objects:
                if obj.parent is None or obj.parent == app.simBox:
                    objects_to_save.append(obj)

        for logic_obj in objects_to_save:
            node_obj = getattr(logic_obj, "guiNode", None)
            if not node_obj and hasattr(app, "logicToNode"):
                node_obj = app.logicToNode.get(logic_obj)
                if node_obj:
                    logic_obj.guiNode = node_obj

            if node_obj:
                node_obj.metadata = logic_obj

            # Directly invoke logic_obj.export()
            if hasattr(logic_obj, "export") and callable(logic_obj.export):
                obj_dict = logic_obj.export()
            else:
                obj_dict = {
                    "__class__": logic_obj.__class__.__name__,
                    "Name": logic_obj.Name,
                    "IO": {k: io.export() for k, io in logic_obj.IO.items()} if hasattr(logic_obj, "IO") and logic_obj.IO else {},
                    "guiNode": node_obj.export() if node_obj and hasattr(node_obj, "export") else None,
                }

            saved_objects.append(obj_dict)

            if node_obj:
                saved_nodes.append({
                    "id": node_obj.id,
                    "constructor": logic_obj.__class__.__name__,
                    "name": getattr(logic_obj, "Name", "Unknown"),
                    "x": node_obj.x,
                    "y": node_obj.y,
                    "angle": node_obj.angle,
                    "width": node_obj.width,
                    "height": node_obj.height,
                    "bg_color": node_obj.bg_color,
                    "border_color": node_obj.border_color,
                    "graphic_code": node_obj.graphic_code,
                })

        self.Backet["saved_objects"] = saved_objects
        self.Backet["saved_nodes"] = saved_nodes

        wires_data = []
        if hasattr(app, "node_editor") and hasattr(app.node_editor, "wires"):
            for wire in app.node_editor.wires:
                if hasattr(wire, "export"):
                    wires_data.append(wire.export())
                else:
                    wires_data.append({
                        "start_node_id": wire.start_pin.owner.id if wire.start_pin and wire.start_pin.owner else None,
                        "start_pin": wire.start_pin.name if wire.start_pin else None,
                        "start_pos": list(wire.start_pos) if wire.start_pos else None,
                        "end_node_id": wire.end_pin.owner.id if wire.end_pin and wire.end_pin.owner else None,
                        "end_pin": wire.end_pin.name if wire.end_pin else None,
                        "end_pos": list(wire.end_pos) if wire.end_pos else None,
                        "vertices": [list(v) for v in wire.vertices],
                        "color": wire.color,
                        "width": wire.width
                    })
        self.Backet["saved_wires"] = wires_data
        return self.Backet

    def Store(self):
        self.Handler.Backet = {self.Name: self.Backet}
        self.Handler.Store(Filename=self.JSon)
        self.Backet = {}




class Importer:
    def __init__(self, FileName: str, TableName, Data, globals_dict: dict = None, spawn_callback=None):
        self.File = FileName
        self.Data = Data
        self.Table = TableName
        self.globals_dict = globals_dict if globals_dict is not None else {}
        self.SpawnCallback = spawn_callback

    def InstantiateObject(self, obj_data: dict) -> Component:
        cls_name = obj_data.get("__class__")
        if not cls_name:
            raise KeyError("Object data is missing mandatory '__class__' field.")

        if cls_name not in self.globals_dict:
            raise KeyError(f"Component constructor '{cls_name}' not found in globals_dict.")

        ctor = self.globals_dict[cls_name]

        try:
            logic_obj = ctor(obj_data["Name"])
        except TypeError:
            logic_obj = ctor(obj_data["Name"], {})

        if "IO" in obj_data and obj_data["IO"]:
            from .BetterDict import BetterDict
            io_dict = BetterDict()
            for io_name, io_data in obj_data["IO"].items():
                io_obj = IO.import_data(io_data)
                io_obj.parent = logic_obj
                io_dict[io_name] = io_obj
            logic_obj.IO = io_dict

        if obj_data.get("guiNode"):
            node_obj = None
            try:
                from gui.node.nodeEngine import NodeObject
                node_obj = NodeObject.from_dict(obj_data["guiNode"], metadata=logic_obj)
            except ImportError:
                pass

            if node_obj:
                node_obj.metadata = logic_obj
                logic_obj.guiNode = node_obj

        if "custom_data" in obj_data and hasattr(logic_obj, "import_custom_data"):
            logic_obj.import_custom_data(obj_data["custom_data"], self.globals_dict)

        return logic_obj

    def _reconstruct_internal_nets(self, top_objects):
        """Recursively collects all IOs across top objects and child modules and merges Nets sharing net_id."""
        def collect_ios(obj):
            ios = []
            if hasattr(obj, "IO") and obj.IO:
                ios.extend(obj.IO.values())
            if hasattr(obj, "child") and obj.child:
                for child_obj in obj.child.values():
                    ios.extend(collect_ios(child_obj))
            return ios

        all_ios = []
        for obj in top_objects:
            all_ios.extend(collect_ios(obj))

        net_groups = {}
        for io in all_ios:
            nid = getattr(io, "_imported_net_id", None)
            if nid:
                if nid not in net_groups:
                    net_groups[nid] = []
                net_groups[nid].append(io)

        # Merge nets for IOs sharing the same net_id
        for nid, io_list in net_groups.items():
            master_io = io_list[0]
            for other_io in io_list[1:]:
                master_io.connect(other_io)

        # Freeze nets on modules after reconstruction
        for obj in top_objects:
            if hasattr(obj, "_freeze_internal_nets"):
                obj._freeze_internal_nets()

    def Import(self, Table=None, globals_dict: dict = None, Loop=None):
        if globals_dict is not None:
            self.globals_dict = globals_dict

        if Table is None:
            raw_data = Handler.Retreive(self.Table, self.File)
            if not raw_data:
                raw_data = Loader.GetData(self.File.replace(".json", ""), self.Table)
            Table = raw_data

        if isinstance(Table, dict):
            data_to_import = Table.get(self.Table, Table)
            if not isinstance(data_to_import, dict):
                data_to_import = Table

            app = self.Data

            if hasattr(app, "ClearAll"):
                app.ClearAll()
            elif hasattr(app, "node_editor") and hasattr(app.node_editor, "clear"):
                app.node_editor.clear()

            nodes_by_id = {}
            imported_top_objects = []

            if "saved_objects" in data_to_import and data_to_import["saved_objects"]:
                for obj_data in data_to_import["saved_objects"]:
                    logic_obj = self.InstantiateObject(obj_data)
                    imported_top_objects.append(logic_obj)
                    node_obj = getattr(logic_obj, "guiNode", None)

                    if logic_obj and node_obj:
                        nodes_by_id[str(node_obj.id)] = node_obj
                        nodes_by_id[node_obj.id] = node_obj

                        if hasattr(app, "node_editor") and hasattr(app.node_editor, "nodes"):
                            if node_obj not in app.node_editor.nodes:
                                app.node_editor.nodes.append(node_obj)

                        if hasattr(app, "addLogic"):
                            app.addLogic(logic_obj, node_obj)
                        elif hasattr(app, "simBox"):
                            app.simBox.addObject(logic_obj)
                    elif logic_obj:
                        if hasattr(app, "simBox"):
                            app.simBox.addObject(logic_obj)

            # Reconstruct all internal module nets by _imported_net_id
            self._reconstruct_internal_nets(imported_top_objects)

            # Restore external canvas wire connections
            saved_wires = data_to_import.get("saved_wires", [])
            if saved_wires and hasattr(app, "node_editor"):
                try:
                    from gui.node.nodeEngine import Wire
                except ImportError:
                    Wire = None

                if Wire is not None:
                    editor = app.node_editor
                    for wdata in saved_wires:
                        s_nid = wdata.get("start_node_id") if "start_node_id" in wdata else wdata.get("start_node")
                        s_node = nodes_by_id.get(str(s_nid)) if s_nid is not None else nodes_by_id.get(s_nid)
                        s_pin = next((p for p in s_node.pins if p.name == wdata.get("start_pin")), None) if s_node else None

                        e_nid = wdata.get("end_node_id") if "end_node_id" in wdata else wdata.get("end_node")
                        e_node = nodes_by_id.get(str(e_nid)) if e_nid is not None else nodes_by_id.get(e_nid)
                        e_pin = next((p for p in e_node.pins if p.name == wdata.get("end_pin")), None) if e_node else None

                        wire = Wire(
                            wire_id=wdata.get("id", f"wire_{len(editor.wires)+1}"),
                            start_pin=s_pin,
                            start_pos=tuple(wdata["start_pos"]) if wdata.get("start_pos") else None,
                            color=wdata.get("color", "#38bdf8"),
                            width=wdata.get("width", 3.5)
                        )
                        wire.end_pin = e_pin
                        wire.end_pos = tuple(wdata["end_pos"]) if wdata.get("end_pos") else None
                        wire.vertices = [tuple(v) for v in wdata.get("vertices", [])]
                        editor.wires.append(wire)

                    if hasattr(editor, "rebuild_nets"):
                        editor.rebuild_nets()

            if hasattr(app, "logicToNode") and isinstance(app.logicToNode, dict):
                if hasattr(app, "node_editor") and hasattr(app.node_editor, "nodes"):
                    for node in app.node_editor.nodes:
                        if hasattr(node, "metadata") and node.metadata:
                            app.logicToNode[node.metadata] = node

            if hasattr(app, "simBox") and hasattr(app.simBox, "init"):
                app.simBox.init()

            if hasattr(app, "node_editor"):
                if hasattr(app.node_editor, "update_dirty_node_graphics"):
                    app.node_editor.update_dirty_node_graphics()
                if hasattr(app.node_editor, "redraw_all"):
                    app.node_editor.redraw_all()

            return self.Data
        return Table