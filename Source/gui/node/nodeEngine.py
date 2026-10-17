# Disclaimer: 
# YES, THIS SCRIPT IS MOSTLY WRITTEN BY AI
# I AM SORRY BUT I REALLY DONT KNOW HOW TO DO THIS PART
# I ALREADY SPENT 1.5WEEKS ON THE nodeEngine :|
# By 12zcab :|


import tkinter as tk
from tkinter import ttk
import math
import uuid
from typing import List, Dict, Set, Optional, Tuple, Callable

def rotatePoint(px: float, py: float, cx: float, cy: float, angle: float) -> Tuple[float, float]:
    rad = math.radians(angle)
    cos_a, sin_a = math.cos(rad), math.sin(rad)
    nx = cos_a * (px - cx) - sin_a * (py - cy) + cx
    ny = sin_a * (px - cx) + cos_a * (py - cy) + cy
    return (nx, ny)

class Pin:
    def __init__(self, owner: 'NodeObject', name: str, rel_x: float, rel_y: float, color: Optional[str] = None):
        self.id = str(uuid.uuid4())[:8]
        self.owner = owner
        self.name = name
        self.rel_x = rel_x
        self.rel_y = rel_y
        self.color = color
        self.net: Optional['Net'] = None

    @property
    def abs_pos(self) -> Tuple[float, float]:
        return (self.owner.x + self.rel_x, self.owner.y + self.rel_y)

    def contains_point(self, wx: float, wy: float, anim_val: float = 0.0, tolerance: float = 0.2) -> bool:
        px, py = self.abs_pos
        pr_world = (0.275 + 0.125 * anim_val) + tolerance
        return (px - pr_world) <= wx <= (px + pr_world) and (py - pr_world) <= wy <= (py + pr_world)

class NodeObject:
    def __init__(
        self,
        node_id: str,
        title: str,
        x: float,
        y: float,
        width: float = 4,
        height: float = 3,
        bg_color: Optional[str] = None,
        border_color: Optional[str] = None,
        graphic_code: Optional[str] = None,
        angle: float = 0.0,
        metadata: Optional[object] = None
    ):
        self.id = node_id
        self.title = title
        self.x = float(round(x * 2.0) / 2.0)
        self.y = float(round(y * 2.0) / 2.0)
        self.width = float(round(width * 2.0) / 2.0)
        self.height = float(round(height * 2.0) / 2.0)
        self.bg_color = bg_color
        self.border_color = border_color
        self.graphic_code = graphic_code
        self.angle = angle
        self.metadata = metadata
        self.pins: List[Pin] = []

        self.compiled_code = None
        if self.graphic_code:
            self.compiled_code = compile(self.graphic_code, f"<node_graphic_{self.id}>", "exec")

    def add_pin(self, name: str, cell_x: float, cell_y: float, color: Optional[str] = None) -> Pin:
        rel_x = cell_x + 0.5
        rel_y = cell_y + 0.5
        pin = Pin(self, name, rel_x, rel_y, color)
        self.pins.append(pin)
        return pin

    def contains_point(self, wx: float, wy: float) -> bool:
        cx = self.x + self.width / 2.0
        cy = self.y + self.height / 2.0
        unrot_x, unrot_y = rotatePoint(wx, wy, cx, cy, -self.angle)
        return (self.x <= unrot_x <= self.x + self.width) and (self.y <= unrot_y <= self.y + self.height)

    def get_pin_at(self, wx: float, wy: float, anim_states: Optional[Dict[object, float]] = None) -> Optional[Pin]:
        for pin in self.pins:
            anim_val = anim_states.get(pin, 0.0) if anim_states else 0.0
            if pin.contains_point(wx, wy, anim_val=anim_val):
                return pin
        return None

class Wire:
    def __init__(
        self,
        wire_id: str,
        start_pin: Optional[Pin] = None,
        start_pos: Optional[Tuple[float, float]] = None,
        color: str = "#38bdf8",
        width: float = 3.5
    ):
        self.id = wire_id
        self.start_pin = start_pin
        self.start_pos = start_pos
        self.end_pin: Optional[Pin] = None
        self.end_pos: Optional[Tuple[float, float]] = None
        self.vertices: List[Tuple[float, float]] = []
        self.color = color
        self.width = width
        self.net: Optional['Net'] = None

    def get_full_path(self) -> List[Tuple[float, float]]:
        raw_path = []
        if self.start_pin:
            raw_path.append(self.start_pin.abs_pos)
        elif self.start_pos:
            raw_path.append(self.start_pos)

        raw_path.extend(self.vertices)

        if self.end_pin:
            raw_path.append(self.end_pin.abs_pos)
        elif self.end_pos:
            raw_path.append(self.end_pos)

        return self.enforce_orthogonal(raw_path)

    @staticmethod
    def enforce_orthogonal(path: List[Tuple[float, float]]) -> List[Tuple[float, float]]:
        if len(path) <= 1:
            return path

        ortho = [path[0]]
        for next_pt in path[1:]:
            prev_pt = ortho[-1]
            if abs(next_pt[0] - prev_pt[0]) > 1e-3 and abs(next_pt[1] - prev_pt[1]) > 1e-3:
                elbow = (next_pt[0], prev_pt[1])
                ortho.append(elbow)
            ortho.append(next_pt)

        return Wire.simplify_path(ortho)

    @staticmethod
    def simplify_path(path: List[Tuple[float, float]]) -> List[Tuple[float, float]]:
        if len(path) <= 1:
            return path

        cleaned = [path[0]]
        for pt in path[1:]:
            if math.hypot(pt[0] - cleaned[-1][0], pt[1] - cleaned[-1][1]) > 1e-3:
                cleaned.append(pt)

        if len(cleaned) <= 2:
            return cleaned

        simplified = [cleaned[0]]
        for i in range(1, len(cleaned) - 1):
            px, py = simplified[-1]
            cx, cy = cleaned[i]
            nx, ny = cleaned[i + 1]

            is_collinear_h = (abs(py - cy) < 1e-3 and abs(cy - ny) < 1e-3)
            is_collinear_v = (abs(px - cx) < 1e-3 and abs(cx - nx) < 1e-3)

            if not (is_collinear_h or is_collinear_v):
                simplified.append((cx, cy))

        simplified.append(cleaned[-1])
        return simplified

    def sync_vertices_from_path(self, path: List[Tuple[float, float]]):
        simplified = self.simplify_path(path)
        if len(simplified) <= 2:
            self.vertices = []
        else:
            self.vertices = simplified[1:-1]

class Net:
    def __init__(self, net_id: str, name: str = ""):
        self.id = net_id
        self.name = name or f"NET_{net_id[:6].upper()}"
        self.wires: Set[Wire] = set()
        self.pins: Set[Pin] = set()
    def setAllPinColor(self,color):
        for pin in self.pins:
            pin.color = color
    def setColor(self, color):
        for wire in self.wires:
            wire.color = color

class NetEngine:
    def __init__(self, event_callback: Optional[Callable[[str, Net, Optional[Pin]], None]] = None):
        self.nets: Dict[str, Net] = {}
        self.event_callback = event_callback

    def rebuild_nets(self, wires: List[Wire], nodes: List[NodeObject]):
        old_pin_net_map = {pin: pin.net for node in nodes for pin in node.pins}
        
        for wire in wires:
            wire.net = None
        for node in nodes:
            for pin in node.pins:
                pin.net = None

        adjacency: Dict[object, Set[object]] = {}

        def add_edge(u, v):
            adjacency.setdefault(u, set()).add(v)
            adjacency.setdefault(v, set()).add(u)

        for wire in wires:
            adjacency.setdefault(wire, set())
            if wire.start_pin:
                add_edge(wire, wire.start_pin)
            if wire.end_pin:
                add_edge(wire, wire.end_pin)

        for i, w1 in enumerate(wires):
            p1_path = w1.get_full_path()
            for j, w2 in enumerate(wires):
                if i >= j:
                    continue
                p2_path = w2.get_full_path()
                if self._paths_touch(p1_path, p2_path):
                    add_edge(w1, w2)

        visited = set()
        raw_components: List[Tuple[Set[Pin], Set[Wire]]] = []

        for node in nodes:
            for pin in node.pins:
                if pin in visited:
                    continue

                component_pins: Set[Pin] = set()
                component_wires: Set[Wire] = set()
                queue = [pin]
                visited.add(pin)

                while queue:
                    curr = queue.pop(0)
                    if isinstance(curr, Pin):
                        component_pins.add(curr)
                    elif isinstance(curr, Wire):
                        component_wires.add(curr)

                    for neighbor in adjacency.get(curr, []):
                        if neighbor not in visited:
                            visited.add(neighbor)
                            queue.append(neighbor)

                if component_pins or component_wires:
                    raw_components.append((component_pins, component_wires))

        for wire in wires:
            if wire not in visited:
                queue = [wire]
                visited.add(wire)
                comp_wires: Set[Wire] = set()
                comp_pins: Set[Pin] = set()

                while queue:
                    curr = queue.pop(0)
                    if isinstance(curr, Wire):
                        comp_wires.add(curr)
                    elif isinstance(curr, Pin):
                        comp_pins.add(curr)

                    for neighbor in adjacency.get(curr, []):
                        if neighbor not in visited:
                            visited.add(neighbor)
                            queue.append(neighbor)

                if comp_pins or comp_wires:
                    raw_components.append((comp_pins, comp_wires))

        existing_net_lookup = {}
        for net in self.nets.values():
            key = (frozenset(net.pins), frozenset(net.wires))
            existing_net_lookup[key] = net

        new_nets: Dict[str, Net] = {}
        matched_net_ids = set()

        for comp_pins, comp_wires in raw_components:
            key = (frozenset(comp_pins), frozenset(comp_wires))
            if key in existing_net_lookup:
                net = existing_net_lookup[key]
                matched_net_ids.add(net.id)
            else:
                net_id = str(uuid.uuid4())[:8]
                net = Net(net_id)
                net.pins = comp_pins
                net.wires = comp_wires
                self._notify_event("NET_CREATE", net, None)

            net.pins = comp_pins
            net.wires = comp_wires
            for p in comp_pins:
                p.net = net
            for w in comp_wires:
                w.net = net
            new_nets[net.id] = net

        destroyed_net_ids = set(self.nets.keys()) - matched_net_ids
        for net_id in destroyed_net_ids:
            old_net = self.nets.get(net_id)
            if old_net:
                self._notify_event("NET_DESTROY", old_net, None)

        self.nets = new_nets

        new_pin_net_map = {pin: pin.net for node in nodes for pin in node.pins}
        for pin, old_net in old_pin_net_map.items():
            new_net = new_pin_net_map.get(pin)
            if old_net != new_net:
                if old_net is not None:
                    self._notify_event("DISCONNECT", old_net, pin)
                if new_net is not None:
                    self._notify_event("CONNECT", new_net, pin)

    @staticmethod
    def _paths_touch(path1: List[Tuple[float, float]], path2: List[Tuple[float, float]]) -> bool:
        for i in range(len(path1) - 1):
            s1_a, s1_b = path1[i], path1[i + 1]
            for j in range(len(path2) - 1):
                s2_a, s2_b = path2[j], path2[j + 1]
                if NodeEditor._dist_segment_to_segment(s1_a, s1_b, s2_a, s2_b) < 0.15:
                    return True
        return False

    def _notify_event(self, event_type: str, net: Net, pin: Optional[Pin]):
        if self.event_callback:
            self.event_callback(event_type, net, pin)


# --- PyIcon Shape Recorder & Hit Testing Helpers ---
class PyIconRecorder:
    def __init__(self):
        self.shapes = []

    def create_polygon(self, *coords, **kwargs):
        pts = self._flatten_coords(coords)
        smooth = kwargs.get("smooth", False)
        if smooth:
            if len(pts) == 4:
                xs = [p[0] for p in pts]
                ys = [p[1] for p in pts]
                x1, x2 = min(xs), max(xs)
                y1, y2 = min(ys), max(ys)
                self.shapes.append(("oval", (x1, y1, x2, y2), kwargs))
                return
            else:
                pts = smooth_polygon(pts, iterations=2)
        self.shapes.append(("polygon", pts, kwargs))

    def create_oval(self, x1, y1, x2, y2, **kwargs):
        self.shapes.append(("oval", (x1, y1, x2, y2), kwargs))

    def create_line(self, *coords, **kwargs):
        pts = self._flatten_coords(coords)
        self.shapes.append(("line", pts, kwargs))

    def create_rectangle(self, x1, y1, x2, y2, **kwargs):
        pts = [(x1, y1), (x2, y1), (x2, y2), (x1, y2)]
        self.shapes.append(("polygon", pts, kwargs))

    def create_text(self, x, y, text="", **kwargs):
        font = kwargs.get("font", ("Consolas", 10))
        font_size = 10
        if isinstance(font, (list, tuple)) and len(font) > 1:
            try:
                font_size = int(font[1])
            except:
                pass
        w_est = max(10.0, len(str(text)) * font_size * 0.7)
        h_est = max(10.0, font_size * 1.4)
        anchor = kwargs.get("anchor", "center")
        
        x1, y1 = x - w_est / 2.0, y - h_est / 2.0
        x2, y2 = x + w_est / 2.0, y + h_est / 2.0
        if anchor in ("w", "nw", "sw"):
            x1, x2 = x, x + w_est
        elif anchor in ("e", "ne", "se"):
            x1, x2 = x - w_est, x
        if anchor in ("n", "nw", "ne"):
            y1, y2 = y, y + h_est
        elif anchor in ("s", "sw", "se"):
            y1, y2 = y - h_est, y

        self.shapes.append(("text", (x1, y1, x2, y2), kwargs))

    @staticmethod
    def _flatten_coords(coords):
        if len(coords) == 1 and isinstance(coords[0], (list, tuple)):
            coords = coords[0]
        pts = []
        for i in range(0, len(coords), 2):
            if i + 1 < len(coords):
                pts.append((float(coords[i]), float(coords[i+1])))
        return pts


def smooth_polygon(pts, iterations=2):
    curr = pts
    for _ in range(iterations):
        next_pts = []
        n = len(curr)
        for i in range(n):
            p0 = curr[i]
            p1 = curr[(i + 1) % n]
            q = (0.75 * p0[0] + 0.25 * p1[0], 0.75 * p0[1] + 0.25 * p1[1])
            r = (0.25 * p0[0] + 0.75 * p1[0], 0.25 * p0[1] + 0.75 * p1[1])
            next_pts.append(q)
            next_pts.append(r)
        curr = next_pts
    return curr


def point_in_polygon(x: float, y: float, poly: list) -> bool:
    n = len(poly)
    if n < 3:
        return False
    inside = False
    p1x, p1y = poly[0]
    for i in range(1, n + 1):
        p2x, p2y = poly[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y
    return inside


def point_near_segment(px, py, v, w) -> float:
    vx, vy = v
    wx, wy = w
    l2 = (wx - vx) ** 2 + (wy - vy) ** 2
    if l2 == 0:
        return math.hypot(px - vx, py - vy)
    t = max(0.0, min(1.0, ((px - vx) * (wx - vx) + (py - vy) * (wy - vy)) / l2))
    proj_x = vx + t * (wx - vx)
    proj_y = vy + t * (wy - vy)
    return math.hypot(px - proj_x, py - proj_y)


def point_near_polygon_outline(x: float, y: float, poly: list, threshold: float) -> bool:
    n = len(poly)
    for i in range(n):
        p1 = poly[i]
        p2 = poly[(i + 1) % n]
        if point_near_segment(x, y, p1, p2) <= threshold:
            return True
    return False


def point_near_polyline(x: float, y: float, pts: list, threshold: float) -> bool:
    for i in range(len(pts) - 1):
        if point_near_segment(x, y, pts[i], pts[i+1]) <= threshold:
            return True
    return False


def hit_test_shapes(px: float, py: float, shapes: list, tolerance: float = 3.0) -> bool:
    for shape_type, data, kwargspx in shapes:
        fill = kwargspx.get("fill", "")
        outline = kwargspx.get("outline", "")
        width = float(kwargspx.get("width", 1))

        has_fill = bool(fill and str(fill).lower() not in ("", "transparent", "none"))
        has_outline = bool(outline and str(outline).lower() not in ("", "transparent", "none"))

        if shape_type == "polygon":
            pts = data
            inside = False
            if has_fill and point_in_polygon(px, py, pts):
                inside = True
            if not inside and has_outline and point_near_polygon_outline(px, py, pts, width + tolerance):
                inside = True
            if inside:
                return True

        elif shape_type == "oval":
            x1, y1, x2, y2 = data
            cx, cy = (x1 + x2) / 2.0, (y1 + y2) / 2.0
            rx, ry = abs(x2 - x1) / 2.0, abs(y2 - y1) / 2.0
            if rx <= 0 or ry <= 0:
                continue
            norm = ((px - cx) / rx) ** 2 + ((py - cy) / ry) ** 2
            inside = False
            if has_fill and norm <= 1.0:
                inside = True
            if not inside and has_outline:
                dist_to_edge = abs(math.hypot(px - cx, py - cy) - (rx + ry) / 2.0)
                if dist_to_edge <= (width / 2.0 + tolerance):
                    inside = True
            if inside:
                return True

        elif shape_type == "line":
            pts = data
            if has_outline or has_fill:
                if point_near_polyline(px, py, pts, width + tolerance):
                    return True

        elif shape_type == "text":
            x1, y1, x2, y2 = data
            if x1 <= px <= x2 and y1 <= py <= y2:
                return True

    return False
# ----------------------------------------------------

class NodeEditor(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.grid_size = 1.0
        self.wire_grid_size = 0.5
        self.snap_enabled = True

        self.colors = {
            "bg": "#090d16",
            "grid": "#1e293b",
            "border_hover": "#38bdf8",
            "border_select": "#f59e0b",
            "wire_default": "#38bdf8",
            "pin_default": "#ef4444",
            "pin_connected": "#10b981",
            "pin_hover": "#facc15",
            "instruction_bg": "#131b2e",
            "instruction_fg": "#94a3b8",
            "tooltip_bg": "#131b2e",
            "tooltip_fg": "#f8fafc",
            "tooltip_border": "#38bdf8",
            "shadow": "#03050a"
        }

        self.nodes: List[NodeObject] = []
        self.wires: List[Wire] = []
        self.engine = NetEngine(event_callback=self._handle_net_event)

        self.pan_x: float = 0.0
        self.pan_y: float = 0.0
        self.zoom: float = 35.0

        self.selected_object: Optional[object] = None
        self.hovered_object: Optional[object] = None
        self.drag_target: Optional[object] = None
        self.drag_node_offset: Tuple[float, float] = (0.0, 0.0)
        self.drag_start_pos: Tuple[float, float] = (0, 0)
        self.current_mouse_screen: Tuple[float, float] = (0.0, 0.0)
        self.current_mouse_world: Tuple[float, float] = (0.0, 0.0)
        self.active_wire: Optional[Wire] = None

        self.drag_wire_initial_path: Optional[List[Tuple[float, float]]] = None
        self.drag_wire_segment_index: Optional[int] = None

        self._grep_press_callback: Optional[Callable[[float, float], None]] = None

        self.anim_states: Dict[object, float] = {}

        self._event_listeners: Dict[str, List[Callable[..., None]]] = {
            "connect": [],
            "disconnect": [],
            "net_create": [],
            "net_destroy": [],
            "select": [],
            "hover": [],
            "node_add": [],
            "node_delete": [],
            "wire_add": [],
            "wire_delete": []
        }

        self.canvas = tk.Canvas(self, bg=self.colors["bg"], highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.canvas.bind("<Configure>", lambda e: self.redraw_all())
        
        # Bind single, double, and triple clicks uniformly to handle rapid clicking as click events
        self.canvas.bind("<ButtonPress-1>", self._on_left_click)
        self.canvas.bind("<Double-Button-1>", self._on_left_click)
        self.canvas.bind("<Triple-Button-1>", self._on_left_click)

        self.canvas.bind("<B1-Motion>", self._on_left_drag)
        self.canvas.bind("<ButtonRelease-1>", self._on_left_release)
        self.canvas.bind("<ButtonPress-3>", self._on_right_click)
        self.canvas.bind("<ButtonPress-2>", self._on_middle_press)
        self.canvas.bind("<B2-Motion>", self._on_middle_drag)
        self.canvas.bind("<Motion>", self._on_mouse_move)
        self.canvas.bind("<MouseWheel>", self._on_mouse_wheel)

        self.canvas.focus_set()
        self.canvas.bind("<Key>", self._on_key_press)

        self._animate_loop()

    def grepNextPressGridPos(self, returnfunction: Callable[[float, float], None]):
        self._grep_press_callback = returnfunction

    def _on_key_press(self, event):
        if event.keysym.lower() == 'r':
            target_node = None
            if isinstance(self.selected_object, NodeObject):
                target_node = self.selected_object
            elif isinstance(self.hovered_object, NodeObject):
                target_node = self.hovered_object

            if target_node:
                self.rotate_node(target_node)

    def rotate_node(self, node: NodeObject, angle_deg: float = 90.0):
        cx = node.width / 2.0
        cy = node.height / 2.0
        for pin in node.pins:
            nx, ny = rotatePoint(pin.rel_x, pin.rel_y, cx, cy, angle_deg)
            pin.rel_x = round(nx * 2.0) / 2.0
            pin.rel_y = round(ny * 2.0) / 2.0

        node.angle = (node.angle + angle_deg) % 360.0
        node.x = self.snap_node_coord(node.x)
        node.y = self.snap_node_coord(node.y)

        self.engine.rebuild_nets(self.wires, self.nodes)
        self.redraw_all()

    def _get_anim_val(self, key: object, is_active: bool) -> float:
        curr = self.anim_states.get(key, 0.0)
        target = 1.0 if is_active else 0.0
        if abs(curr - target) > 1e-3:
            step = 0.20 if target > curr else -0.20
            new_val = max(0.0, min(1.0, curr + step))
            self.anim_states[key] = new_val
            return new_val
        self.anim_states[key] = target
        return target

    def _animate_loop(self):
        needs_redraw = False
        selected_net = self.get_selected_net()

        for node in self.nodes:
            is_node_active = (node == self.selected_object or node == self.hovered_object)
            val = self._get_anim_val(node, is_node_active)
            if 0.0 < val < 1.0:
                needs_redraw = True

            for pin in node.pins:
                is_pin_active = (pin == self.hovered_object) or (pin == self.selected_object and not self.active_wire)
                pval = self._get_anim_val(pin, is_pin_active)
                if 0.0 < pval < 1.0:
                    needs_redraw = True

        for wire in self.wires:
            is_wire_active = (
                wire == self.selected_object or
                wire == self.hovered_object or
                (selected_net is not None and wire.net == selected_net) or
                (isinstance(self.hovered_object, tuple) and self.hovered_object[0] == wire)
            )
            wval = self._get_anim_val(wire, is_wire_active)
            if 0.0 < wval < 1.0:
                needs_redraw = True

        if needs_redraw:
            self.redraw_all()

        self.after(16, self._animate_loop)

    def bind_event(self, event_name: str, callback: Callable[..., None]):
        if event_name in self._event_listeners:
            self._event_listeners[event_name].append(callback)

    def _emit(self, event_name: str, *args, **kwargs):
        for cb in self._event_listeners.get(event_name, []):
            cb(*args, **kwargs)

    def get_selected_net(self) -> Optional[Net]:
        if isinstance(self.selected_object, Wire):
            return self.selected_object.net
        if isinstance(self.selected_object, Pin):
            return self.selected_object.net
        if isinstance(self.selected_object, Net):
            return self.selected_object
        return None

    def snap_node_coord(self, val: float) -> float:
        return float(round(val * 2.0) / 2.0) if self.snap_enabled else val

    def snap_wire_coord(self, val: float) -> float:
        return float(round(val * 2.0) / 2.0) if self.snap_enabled else val

    def snap_wire_point(self, wx: float, wy: float) -> Tuple[float, float]:
        target_pin = self._hit_test_pin(wx, wy)
        if target_pin:
            return target_pin.abs_pos
        return (self.snap_wire_coord(wx), self.snap_wire_coord(wy))

    def world_to_screen(self, wx: float, wy: float) -> Tuple[float, float]:
        return (wx * self.zoom + self.pan_x, wy * self.zoom + self.pan_y)

    def screen_to_world(self, sx: float, sy: float) -> Tuple[float, float]:
        return ((sx - self.pan_x) / self.zoom, (sy - self.pan_y) / self.zoom)

    def _draw_rounded_rect(self, x1: float, y1: float, x2: float, y2: float, radius: Optional[float] = None, **kwargs):
        if radius is None:
            radius = 0.25 * self.zoom
        if radius <= 0:
            return self.canvas.create_rectangle(x1, y1, x2, y2, **kwargs)
        w, h = abs(x2 - x1), abs(y2 - y1)
        r = min(radius, w / 2.0, h / 2.0)
        pts = [
            x1 + r, y1, x1 + r, y1, x2 - r, y1, x2 - r, y1,
            x2, y1, x2, y1 + r, x2, y1 + r, x2, y2 - r,
            x2, y2 - r, x2, y2, x2 - r, y2, x2 - r, y2,
            x1 + r, y2, x1 + r, y2, x1, y2, x1, y2 - r,
            x1, y2 - r, x1, y1 + r, x1, y1 + r, x1, y1
        ]
        return self.canvas.create_polygon(pts, smooth=True, **kwargs)

    def redraw_all(self):
        self.canvas.delete("all")
        self._draw_grid()
        self._draw_wires()
        self._draw_nodes()
        self._draw_instructions()
        self._draw_hover_tooltip()

    def _draw_grid(self):
        w = self.canvas.winfo_width() or 1000
        h = self.canvas.winfo_height() or 700

        grid_step = self.zoom
        if grid_step < 6:
            return

        min_wx = math.floor((-self.pan_x / self.zoom))
        max_wx = math.ceil(((w - self.pan_x) / self.zoom))
        min_wy = math.floor((-self.pan_y / self.zoom))
        max_wy = math.ceil(((h - self.pan_y) / self.zoom))

        dot_count = (max_wx - min_wx + 1) * (max_wy - min_wy + 1)
        if dot_count > 2500:
            return

        dot_r = max(1.5, 2.0 * (self.zoom / 30.0))
        curr_wx = min_wx
        while curr_wx <= max_wx:
            sx = curr_wx * self.zoom + self.pan_x
            curr_wy = min_wy
            while curr_wy <= max_wy:
                sy = curr_wy * self.zoom + self.pan_y
                self.canvas.create_oval(sx - dot_r, sy - dot_r, sx + dot_r, sy + dot_r, fill=self.colors["grid"], outline="")
                curr_wy += 1
            curr_wx += 1

    def _draw_nodes(self):
        selected_net = self.get_selected_net()
        corner_r = 0.25 * self.zoom

        for node in self.nodes:
            sx, sy = self.world_to_screen(node.x, node.y)
            sw, sh = node.width * self.zoom, node.height * self.zoom

            is_selected = (node == self.selected_object)
            is_hovered = (node == self.hovered_object)

            if (not node.bg_color in [None, "transparent"]) or (not node.border_color in [None, "transparent"]):
                node_anim = self._get_anim_val(node, is_selected or is_hovered)
                if is_selected:
                    border_col = self.colors["border_select"]
                    border_w = 2.0 + 1.2 * node_anim
                elif is_hovered:
                    border_col = self.colors["border_hover"]
                    border_w = 2.0 + 0.8 * node_anim
                else:
                    border_col = node.border_color
                    border_w = 2.0 if border_col else 0.0
                so = 0.25 * self.zoom
                if node.bg_color:
                    self._draw_rounded_rect(sx + so, sy + so, sx + sw + so, sy + sh + so, radius=corner_r, fill=self.colors["shadow"], outline="")
                bg_fill = node.bg_color if node.bg_color else ""
                b_out = border_col if border_col else ""
                self._draw_rounded_rect(sx, sy, sx + sw, sy + sh, radius=corner_r, fill=bg_fill, outline=b_out, width=border_w)

            if node.compiled_code:
                tags = (f"node_{node.id}", f"node_graphic_{node.id}")
                exec_scope = {
                    "canvas": self.canvas,
                    "x": sx,
                    "y": sy,
                    "w": sw,
                    "h": sh,
                    "cx": sx + sw / 2.0,
                    "cy": sy + sh / 2.0,
                    "angle": node.angle,
                    "is_selected": is_selected,
                    "tags": tags,
                    "zoom": self.zoom,
                    "rotatePoint": rotatePoint,
                    "math": math,
                    "node": node,
                    "metadata": node.metadata
                }
                exec(node.compiled_code, exec_scope)

            for pin in node.pins:
                px, py = pin.abs_pos
                psx, psy = self.world_to_screen(px, py)
                is_pin_hovered = (pin == self.hovered_object)
                is_pin_active = is_pin_hovered or (pin == self.selected_object and not self.active_wire)

                pin_anim = self._get_anim_val(pin, is_pin_active)
                pr = (0.28 + 0.1 * pin_anim) * self.zoom

                if is_pin_hovered:
                    pin_col = self.colors["pin_hover"]
                elif pin.color:
                    pin_col = pin.color
                elif pin.net and selected_net == pin.net:
                    pin_col = self.colors["border_select"]
                elif pin.net:
                    pin_col = self.colors["pin_connected"]
                else:
                    pin_col = self.colors["pin_default"]

                pin_r = 0.12 * self.zoom
                self._draw_rounded_rect(
                    psx - pr, psy - pr, psx + pr, psy + pr,
                    radius=pin_r, fill=pin_col, outline="#666666", width=1.5 if is_pin_active else 1.0,
                    tags=f"node_{node.id}"
                )

                font_size = int(8 * (self.zoom / 35.0))
                if font_size > 0:
                    text_col = "#000000" if is_pin_hovered else "#ffffff"
                    self.canvas.create_text(
                        psx, psy, text=pin.name, fill=text_col, anchor="center",
                        font=("Consolas", font_size, "bold"), tags=f"node_{node.id}"
                    )

    def _draw_wires(self):
        selected_net = self.get_selected_net()

        for wire in self.wires:
            path = wire.get_full_path()
            if len(path) < 2:
                continue

            screen_pts = [self.world_to_screen(pt[0], pt[1]) for pt in path]
            flat_pts = [c for pt in screen_pts for c in pt]

            is_net_selected = (selected_net is not None and wire.net == selected_net)
            is_hovered = (self.hovered_object == wire or (isinstance(self.hovered_object, tuple) and self.hovered_object[0] == wire))

            wire_anim = self._get_anim_val(wire, is_net_selected or is_hovered)

            if is_net_selected:
                color = self.colors["border_select"]
                width = wire.width + 1.8 * wire_anim
            elif is_hovered:
                color = self.colors["border_hover"]
                width = wire.width + 1.2 * wire_anim
            else:
                color = wire.color
                width = wire.width

            self.canvas.create_line(*flat_pts, fill=color, width=width * (self.zoom / 35.0), smooth=False)

        if self.active_wire:
            path = self.active_wire.get_full_path()
            if len(path) >= 1:
                cur_wx, cur_wy = self.current_mouse_world
                target_pos = self.snap_wire_point(cur_wx, cur_wy)

                last_pt = path[-1]
                ortho_path = list(path)
                if last_pt[0] != target_pos[0] and last_pt[1] != target_pos[1]:
                    elbow = (target_pos[0], last_pt[1])
                    ortho_path.extend([elbow, target_pos])
                else:
                    ortho_path.append(target_pos)

                s_pts = [self.world_to_screen(pt[0], pt[1]) for pt in ortho_path]
                flat_s = [c for pt in s_pts for c in pt]
                if len(flat_s) >= 4:
                    self.canvas.create_line(*flat_s, fill=self.active_wire.color, width=2.5 * (self.zoom / 35.0), dash=(6, 4))

    def _draw_instructions(self):
        h = self.canvas.winfo_height() or 700
        text = (
            "Strict 90° Edge-Main Controls (Dual Edge/Center 0.5 Grid):\n"
            "• L-Click / Rapid-Click: Select Net / Toggle Node / Drag\n"
            "• R Key: Rotate Selected/Hovered Node\n"
            "• Shift + L-Click: Branch Sub-Wire from Edge / Pin\n"
            "• R-Click: Delete Node or Full Wire\n"
            "• Shift + R-Click: Cut Wire Segment (Net Split)\n"
            "• Hover Wire: View Connected Node:Pin List\n"
            "• M-Click + Drag: Pan Canvas | Scroll: Zoom"
        )
        x1, y1 = 12, h - 135
        x2, y2 = 380, h - 12
        corner_r = 0.25 * self.zoom
        self._draw_rounded_rect(x1, y1, x2, y2, radius=corner_r, fill=self.colors["instruction_bg"], outline="#334155")
        self.canvas.create_text(x1 + 10, y1 + 61, text=text, fill=self.colors["instruction_fg"], anchor="w", font=("Consolas", 8))

    def _draw_hover_tooltip(self):
        wire = None
        if isinstance(self.hovered_object, Wire):
            wire = self.hovered_object
        elif isinstance(self.hovered_object, tuple) and isinstance(self.hovered_object[0], Wire):
            wire = self.hovered_object[0]

        if not wire or not wire.net or not wire.net.pins:
            return

        connected_items = [f"{p.owner.title}:{p.name}" for p in wire.net.pins]
        if not connected_items:
            return

        msx, msy = self.current_mouse_screen
        header = f"Net: {wire.net.name}"
        lines = [header, "Connected Pins:"] + [f" • {item}" for item in connected_items]

        box_w = max(len(l) for l in lines) * 7.5 + 20
        box_h = len(lines) * 16 + 14

        tx1 = msx + 15
        ty1 = msy + 15

        c_w = self.canvas.winfo_width() or 1000
        c_h = self.canvas.winfo_height() or 700

        if tx1 + box_w > c_w - 10:
            tx1 = msx - box_w - 10
        if ty1 + box_h > c_h - 10:
            ty1 = msy - box_h - 10

        tx2 = tx1 + box_w
        ty2 = ty1 + box_h

        corner_r = 0.25 * self.zoom
        self._draw_rounded_rect(tx1, ty1, tx2, ty2, radius=corner_r, fill=self.colors["tooltip_bg"], outline=self.colors["tooltip_border"], width=1.5)

        curr_y = ty1 + 14
        self.canvas.create_text(tx1 + 10, curr_y, text=header, fill=self.colors["tooltip_border"], anchor="w", font=("Helvetica", 9, "bold"))
        curr_y += 16

        for l in lines[1:]:
            self.canvas.create_text(tx1 + 10, curr_y, text=l, fill=self.colors["tooltip_fg"], anchor="w", font=("Consolas", 8))
            curr_y += 15

    def _get_nearest_point_on_wire(self, wire: Wire, wx: float, wy: float) -> Tuple[float, float]:
        path = wire.get_full_path()
        best_pt = (wx, wy)
        min_dist = float('inf')

        for i in range(len(path) - 1):
            p1, p2 = path[i], path[i + 1]
            proj = self._project_point_onto_ortho_segment((wx, wy), p1, p2)
            d = math.hypot(wx - proj[0], wy - proj[1])
            if d < min_dist:
                min_dist = d
                best_pt = proj

        return (self.snap_wire_coord(best_pt[0]), self.snap_wire_coord(best_pt[1]))

    def _get_nearest_wire_in_editor(self, wx: float, wy: float, radius: float = 12.0) -> Optional[Tuple[Wire, Tuple[float, float]]]:
        best_wire = None
        best_pt = (wx, wy)
        min_dist = radius / self.zoom

        for wire in self.wires:
            if wire == self.active_wire:
                continue
            path = wire.get_full_path()
            for i in range(len(path) - 1):
                p1, p2 = path[i], path[i + 1]
                proj = self._project_point_onto_ortho_segment((wx, wy), p1, p2)
                d = math.hypot(wx - proj[0], wy - proj[1])
                if d < min_dist:
                    min_dist = d
                    best_wire = wire
                    best_pt = proj

        if best_wire:
            return best_wire, (self.snap_wire_coord(best_pt[0]), self.snap_wire_coord(best_pt[1]))
        return None

    @staticmethod
    def _project_point_onto_ortho_segment(p, v, w) -> Tuple[float, float]:
        px, py = p
        vx, vy = v
        wx, wy = w
        l2 = (wx - vx) ** 2 + (wy - vy) ** 2
        if l2 == 0:
            return v
        t = max(0.0, min(1.0, ((px - vx) * (wx - vx) + (py - vy) * (wy - vy)) / l2))
        return (vx + t * (wx - vx), vy + t * (wy - vy))

    def _get_wire_segment_at(self, wire: Wire, wx: float, wy: float) -> Optional[int]:
        path = wire.get_full_path()
        threshold = ((wire.width / 2.0) + 3.0) / self.zoom
        for i in range(len(path) - 1):
            p1, p2 = path[i], path[i + 1]
            if self._dist_to_segment((wx, wy), p1, p2) <= threshold:
                return i
        return None

    def _append_ortho_point(self, wire: Wire, target_pos: Tuple[float, float]):
        path = wire.get_full_path()
        if not path:
            wire.vertices.append(target_pos)
            return

        last_pt = path[-1]
        if last_pt[0] != target_pos[0] and last_pt[1] != target_pos[1]:
            elbow = (target_pos[0], last_pt[1])
            wire.vertices.append(elbow)
        wire.vertices.append(target_pos)

    def _on_left_click(self, event):
        self.canvas.focus_set()
        wx, wy = self.screen_to_world(event.x, event.y)

        if self._grep_press_callback is not None:
            callback = self._grep_press_callback
            self._grep_press_callback = None
            grid_x = self.snap_wire_coord(wx)
            grid_y = self.snap_wire_coord(wy)
            callback(grid_x, grid_y)
            return

        self.drag_start_pos = (event.x, event.y)
        is_shift = bool(event.state & 0x0001)

        clicked_pin = self._hit_test_pin(wx, wy)
        clicked_node = self._hit_test_node(wx, wy)
        clicked_wire, seg_idx = self._hit_test_wire(wx, wy)
        if clicked_node:
            self.nodes.append(self.nodes.pop(self.nodes.index(clicked_node)))
        if is_shift:
            if clicked_wire:
                branch_pos = self._get_nearest_point_on_wire(clicked_wire, wx, wy)
                wire_id = f"wire_{len(self.wires) + 1}"
                self.active_wire = Wire(wire_id, start_pos=branch_pos, color=clicked_wire.color)
                self.selected_object = None
            elif clicked_pin:
                wire_id = f"wire_{len(self.wires) + 1}"
                self.active_wire = Wire(wire_id, start_pin=clicked_pin, color=self.colors["wire_default"])
                self.selected_object = None
            self.redraw_all()
            return

        if self.active_wire:
            if clicked_pin:
                if clicked_pin != self.active_wire.start_pin:
                    self._append_ortho_point(self.active_wire, clicked_pin.abs_pos)
                    self.active_wire.end_pin = clicked_pin
                    self.wires.append(self.active_wire)
                    created_wire = self.active_wire
                    self.active_wire = None
                    self.selected_object = created_wire
                    self.engine.rebuild_nets(self.wires, self.nodes)
                    self._emit("wire_add", created_wire)
            else:
                wire_snap = self._get_nearest_wire_in_editor(wx, wy, radius=12.0)
                if wire_snap:
                    target_wire, attach_pos = wire_snap
                    self._append_ortho_point(self.active_wire, attach_pos)
                    self.active_wire.end_pos = attach_pos
                    self.wires.append(self.active_wire)
                    created_wire = self.active_wire
                    self.active_wire = None
                    self.selected_object = created_wire
                    self.engine.rebuild_nets(self.wires, self.nodes)
                    self._emit("wire_add", created_wire)
                else:
                    snap_pos = self.snap_wire_point(wx, wy)
                    self._append_ortho_point(self.active_wire, snap_pos)
        else:
            if clicked_pin:
                wire_id = f"wire_{len(self.wires) + 1}"
                self.active_wire = Wire(wire_id, start_pin=clicked_pin, color=self.colors["wire_default"])
                self.selected_object = None
            elif clicked_node:
                self.selected_object = clicked_node
                self.drag_target = clicked_node
                self.drag_node_offset = (wx - clicked_node.x, wy - clicked_node.y)
            elif clicked_wire:
                self.selected_object = clicked_wire
                if seg_idx is not None:
                    self.drag_target = clicked_wire
                    self.drag_wire_initial_path = clicked_wire.get_full_path()
                    self.drag_wire_segment_index = seg_idx
            else:
                self.selected_object = None

        self._emit("select", self.selected_object)
        self.redraw_all()

    def _on_left_drag(self, event):
        wx, wy = self.screen_to_world(event.x, event.y)
        self.current_mouse_screen = (event.x, event.y)
        self.current_mouse_world = (wx, wy)

        if self.drag_target:
            if isinstance(self.drag_target, NodeObject):
                node = self.drag_target
                ox, oy = self.drag_node_offset
                node.x = self.snap_node_coord(wx - ox)
                node.y = self.snap_node_coord(wy - oy)
            elif isinstance(self.drag_target, Wire):
                wire = self.drag_target
                P = self.drag_wire_initial_path
                k = self.drag_wire_segment_index

                if P and k is not None and 0 <= k < len(P) - 1:
                    p_k, p_k1 = P[k], P[k + 1]
                    n = len(P)
                    is_horizontal = (abs(p_k[1] - p_k1[1]) < 1e-3)

                    if is_horizontal:
                        new_y = self.snap_wire_coord(wy)
                        if k == 0 and k == n - 2:
                            new_path = [P[0], (P[0][0], new_y), (P[1][0], new_y), P[1]]
                        elif k == 0:
                            new_path = [P[0], (P[0][0], new_y), (P[1][0], new_y)] + P[2:]
                        elif k == n - 2:
                            new_path = P[:n - 2] + [(P[n - 2][0], new_y), (P[n - 1][0], new_y), P[n - 1]]
                        else:
                            new_path = P[:k] + [(P[k][0], new_y), (P[k + 1][0], new_y)] + P[k + 2:]
                    else:
                        new_x = self.snap_wire_coord(wx)
                        if k == 0 and k == n - 2:
                            new_path = [P[0], (new_x, P[0][1]), (new_x, P[1][1]), P[1]]
                        elif k == 0:
                            new_path = [P[0], (new_x, P[0][1]), (new_x, P[1][1])] + P[2:]
                        elif k == n - 2:
                            new_path = P[:n - 2] + [(new_x, P[n - 2][1]), (new_x, P[n - 1][1]), P[n - 1]]
                        else:
                            new_path = P[:k] + [(new_x, P[k][1]), (new_x, P[k + 1][1])] + P[k + 2:]

                    if len(new_path) <= 2:
                        wire.vertices = []
                    else:
                        wire.vertices = new_path[1:-1]

            self.redraw_all()
        elif self.active_wire:
            self.redraw_all()

    def _on_left_release(self, event):
        if self.drag_target:
            if isinstance(self.drag_target, Wire):
                wire = self.drag_target
                wire.sync_vertices_from_path(wire.get_full_path())
                self.drag_wire_initial_path = None
                self.drag_wire_segment_index = None

            self.drag_target = None
            self.engine.rebuild_nets(self.wires, self.nodes)
            self.redraw_all()

    def _on_right_click(self, event):
        self.canvas.focus_set()
        wx, wy = self.screen_to_world(event.x, event.y)
        is_shift = bool(event.state & 0x0001)

        if self.active_wire:
            self.active_wire = None
        else:
            clicked_node = self._hit_test_node(wx, wy)
            clicked_wire, _ = self._hit_test_wire(wx, wy)

            if is_shift and clicked_wire:
                seg_idx = self._get_wire_segment_at(clicked_wire, wx, wy)
                if seg_idx is not None:
                    self._delete_wire_segment(clicked_wire, seg_idx)
            else:
                if clicked_node:
                    self.delete_node(clicked_node)
                elif clicked_wire:
                    self.delete_wire(clicked_wire)

            self.engine.rebuild_nets(self.wires, self.nodes)

        self.redraw_all()

    def _delete_wire_segment(self, wire: Wire, seg_idx: int):
        path = wire.get_full_path()
        if len(path) < 2:
            return

        if len(path) == 2:
            self.delete_wire(wire)
            return

        self.wires.remove(wire)

        path_left = path[:seg_idx + 1]
        path_right = path[seg_idx + 1:]

        if len(path_left) >= 2:
            w1 = Wire(f"wire_{len(self.wires) + 1}", color=wire.color, width=wire.width)
            if wire.start_pin:
                w1.start_pin = wire.start_pin
                w1.vertices = path_left[1:-1]
            else:
                w1.start_pos = path_left[0]
                w1.vertices = path_left[1:-1]
            w1.end_pos = path_left[-1]
            self.wires.append(w1)

        if len(path_right) >= 2:
            w2 = Wire(f"wire_{len(self.wires) + 1}", color=wire.color, width=wire.width)
            w2.start_pos = path_right[0]
            w2.vertices = path_right[1:-1]
            if wire.end_pin:
                w2.end_pin = wire.end_pin
            else:
                w2.end_pos = path_right[-1]
            self.wires.append(w2)

    def _on_mouse_move(self, event):
        wx, wy = self.screen_to_world(event.x, event.y)
        self.current_mouse_screen = (event.x, event.y)
        self.current_mouse_world = (wx, wy)

        prev_hovered = self.hovered_object

        clicked_pin = self._hit_test_pin(wx, wy)
        clicked_node = self._hit_test_node(wx, wy)
        clicked_wire, seg_idx = self._hit_test_wire(wx, wy)

        if clicked_pin:
            self.hovered_object = clicked_pin
        elif clicked_node:
            self.hovered_object = clicked_node
        elif clicked_wire:
            self.hovered_object = clicked_wire
        else:
            self.hovered_object = None

        if prev_hovered != self.hovered_object:
            self._emit("hover", self.hovered_object)
            self.redraw_all()
        elif self.active_wire or isinstance(self.hovered_object, Wire):
            self.redraw_all()

    def _on_mouse_wheel(self, event):
        factor = 1.12 if event.delta > 0 else 0.88
        new_zoom = self.zoom * factor

        mx, my = event.x, event.y
        self.pan_x = mx - (mx - self.pan_x) * (new_zoom / self.zoom)
        self.pan_y = my - (my - self.pan_y) * (new_zoom / self.zoom)
        self.zoom = new_zoom
        self.redraw_all()

    def _on_middle_press(self, event):
        self.canvas.focus_set()
        self.drag_start_pos = (event.x, event.y)

    def _on_middle_drag(self, event):
        dx = event.x - self.drag_start_pos[0]
        dy = event.y - self.drag_start_pos[1]
        self.pan_x += dx
        self.pan_y += dy
        self.drag_start_pos = (event.x, event.y)
        self.redraw_all()

    def _hit_test_node(self, wx: float, wy: float) -> Optional[NodeObject]:
        sx, sy = self.world_to_screen(wx, wy)
        for node in reversed(self.nodes):
            has_bg = node.bg_color is not None and node.bg_color.lower() not in ("", "transparent")
            has_border = node.border_color is not None and node.border_color.lower() not in ("", "transparent")

            if has_bg or has_border:
                if node.contains_point(wx, wy):
                    return node

            if node.compiled_code:
                sw, sh = node.width * self.zoom, node.height * self.zoom
                nsx, nsy = self.world_to_screen(node.x, node.y)
                recorder = PyIconRecorder()
                exec_scope = {
                    "canvas": recorder,
                    "x": nsx,
                    "y": nsy,
                    "w": sw,
                    "h": sh,
                    "cx": nsx + sw / 2.0,
                    "cy": nsy + sh / 2.0,
                    "angle": node.angle,
                    "is_selected": (node == self.selected_object),
                    "tags": (),
                    "zoom": self.zoom,
                    "rotatePoint": rotatePoint,
                    "math": math,
                    "node": node,
                    "metadata": node.metadata
                }
                try:
                    exec(node.compiled_code, exec_scope)
                    if hit_test_shapes(sx, sy, recorder.shapes, tolerance=3.0):
                        return node
                except Exception:
                    pass

            if has_bg or has_border:
                if node.contains_point(wx, wy):
                    return node
        return None

    def _hit_test_pin(self, wx: float, wy: float) -> Optional[Pin]:
        for node in self.nodes:
            pin = node.get_pin_at(wx, wy, anim_states=self.anim_states)
            if pin:
                return pin
        return None

    def _hit_test_wire(self, wx: float, wy: float) -> Tuple[Optional[Wire], Optional[int]]:
        for wire in self.wires:
            threshold = ((wire.width / 2.0) + 3.0) / self.zoom
            path = wire.get_full_path()
            for i in range(len(path) - 1):
                p1, p2 = path[i], path[i + 1]
                if self._dist_to_segment((wx, wy), p1, p2) <= threshold:
                    return wire, i
        return None, None

    @staticmethod
    def _dist_segment_to_segment(p1, p2, p3, p4) -> float:
        d1 = NodeEditor._dist_to_segment(p1, p3, p4)
        d2 = NodeEditor._dist_to_segment(p2, p3, p4)
        d3 = NodeEditor._dist_to_segment(p3, p1, p2)
        d4 = NodeEditor._dist_to_segment(p4, p1, p2)
        return min(d1, d2, d3, d4)

    @staticmethod
    def _dist_to_segment(p, v, w) -> float:
        px, py = p
        vx, vy = v
        wx, wy = w
        l2 = (wx - vx) ** 2 + (wy - vy) ** 2
        if l2 == 0:
            return math.hypot(px - vx, py - vy)
        t = max(0.0, min(1.0, ((px - vx) * (wx - vx) + (py - vy) * (wy - vy)) / l2))
        proj_x = vx + t * (wx - vx)
        proj_y = vy + t * (wy - vy)
        return math.hypot(px - proj_x, py - proj_y)

    def create_node(
        self,
        title: str,
        x: float,
        y: float,
        width: float = 4,
        height: float = 3,
        bg_color: Optional[str] = "transparent",
        border_color: Optional[str] = "transparent",
        graphic_code: Optional[str] = None,
        angle: float = 0.0,
        metadata: Optional[object] = None
    ) -> NodeObject:
        sx = self.snap_node_coord(x)
        sy = self.snap_node_coord(y)
        node = NodeObject(
            f"node_{len(self.nodes)+1}", title, sx, sy, width, height,
            bg_color=bg_color, border_color=border_color, graphic_code=graphic_code, angle=angle,
            metadata=metadata
        )
        self.nodes.append(node)
        self._emit("node_add", node)
        self.redraw_all()
        self.engine.rebuild_nets(self.wires, self.nodes)
        return node

    def delete_node(self, node: NodeObject):
        if node in self.nodes:
            node_pins = set(node.pins)
            removed_wires = [w for w in self.wires if w.start_pin in node_pins or w.end_pin in node_pins]
            for w in removed_wires:
                self.delete_wire(w)
            self.nodes.remove(node)
            if self.selected_object == node:
                self.selected_object = None
            self._emit("node_delete", node)

    def delete_wire(self, wire: Wire):
        if wire in self.wires:
            self.wires.remove(wire)
            if self.selected_object == wire:
                self.selected_object = None
            self._emit("wire_delete", wire)

    def clear(self):
        self.nodes.clear()
        self.wires.clear()
        self.selected_object = None
        self.hovered_object = None
        self.engine.rebuild_nets(self.wires, self.nodes)
        self.redraw_all()

    def reset_view(self):
        self.pan_x = 0.0
        self.pan_y = 0.0
        self.zoom = 35.0
        self.redraw_all()

    def _handle_net_event(self, event_type: str, net: Net, pin: Optional[Pin]):
        pin_name = f"{pin.owner.title}:{pin.name}" if pin else "None"
        if event_type == "CONNECT":
            self._emit("connect", net, pin)
        elif event_type == "DISCONNECT":
            self._emit("disconnect", net, pin)
        elif event_type == "NET_CREATE":
            self._emit("net_create", net)
        elif event_type == "NET_DESTROY":
            self._emit("net_destroy", net)

NAND_GATE_PYICON_CODE = """
import math

u = zoom

y_in0 = y + 0.5 * u
y_out = y + 1.5 * u
y_in1 = y + 2.5 * u

x_gate_back = x + 1.0 * u
x_gate_flat_end = x + 2.0 * u

y_top = y + 0.0 * u
y_bot = y + 3.0 * u
y_mid = y + 1.5 * u

rx = 0.8 * u
ry = (y_bot - y_top) / 2.0
arc_center_x = x_gate_flat_end
arc_center_y = y_mid

pts = [(x_gate_back, y_top), (x_gate_flat_end, y_top)]
num_arc_pts = 16
for i in range(num_arc_pts + 1):
    a = (math.pi / 2.0) - (i / num_arc_pts) * math.pi
    px = arc_center_x + rx * math.cos(a)
    py = arc_center_y - ry * math.sin(a)
    pts.append((px, py))

pts.extend([(x_gate_flat_end, y_bot), (x_gate_back, y_bot)])

gate_tip_x = arc_center_x + rx
r_bubble = 0.2 * u
cx_bubble = gate_tip_x + r_bubble

line_in0 = [(x - 0.5 * u, y_in0), (x_gate_back, y_in0)]
line_in1 = [(x - 0.5 * u, y_in1), (x_gate_back, y_in1)]
line_out = [(cx_bubble + r_bubble, y_out), (x + 4.5 * u, y_out)]

pts = [rotatePoint(px, py, cx, cy, angle) for px, py in pts]
line_in0 = [rotatePoint(px, py, cx, cy, angle) for px, py in line_in0]
line_in1 = [rotatePoint(px, py, cx, cy, angle) for px, py in line_in1]
line_out = [rotatePoint(px, py, cx, cy, angle) for px, py in line_out]

bubble_center = rotatePoint(cx_bubble, y_mid, cx, cy, angle)

stroke_w = max(2, int(u * 0.08))
select_w = stroke_w + max(2, int(u * 0.06))

flat_line0 = [coord for pt in line_in0 for coord in pt]
flat_line1 = [coord for pt in line_in1 for coord in pt]
flat_out = [coord for pt in line_out for coord in pt]

canvas.create_line(*flat_line0, fill="#FFFFFF", width=stroke_w, tags=tags)
canvas.create_line(*flat_line1, fill="#FFFFFF", width=stroke_w, tags=tags)
canvas.create_line(*flat_out, fill="#FFFFFF", width=stroke_w, tags=tags)

flat_pts = [coord for pt in pts for coord in pt]

if is_selected:
    canvas.create_polygon(
        flat_pts,
        fill="",
        outline="#00E5FF",
        width=select_w,
        joinstyle="miter",
        smooth=False,
        tags=tags
    )
    canvas.create_oval(
        bubble_center[0] - r_bubble - select_w / 2, bubble_center[1] - r_bubble - select_w / 2,
        bubble_center[0] + r_bubble + select_w / 2, bubble_center[1] + r_bubble + select_w / 2,
        fill="",
        outline="#00E5FF",
        width=stroke_w,
        tags=tags
    )

canvas.create_polygon(
    flat_pts,
    fill="#181818",
    outline="#FFFFFF",
    width=stroke_w,
    joinstyle="miter",
    smooth=False,
    tags=tags
)

canvas.create_oval(
    bubble_center[0] - r_bubble, bubble_center[1] - r_bubble,
    bubble_center[0] + r_bubble, bubble_center[1] + r_bubble,
    fill="#181818",
    outline="#FFFFFF",
    width=stroke_w,
    tags=tags
)
"""

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Node Editor - Dual Edge/Center 0.5 Grid Alignment")
    root.geometry("1100x700")

    app = NodeEditor(root)
    app.pack(fill=tk.BOTH, expand=True)

    app.bind_event("net_create", lambda net: print(f"[EVENT] Net Created: {net.name} (ID: {net.id})"))
    app.bind_event("net_destroy", lambda net: print(f"[EVENT] Net Destroyed: {net.name} (ID: {net.id})"))
    app.bind_event("connect", lambda net, pin: print(f"[EVENT] Connected Pin {pin.owner.title}:{pin.name} to {net.name}"))
    app.bind_event("disconnect", lambda net, pin: print(f"[EVENT] Disconnected Pin {pin.owner.title}:{pin.name} from {net.name}"))

    nand_gate = app.create_node(
        title="Nand Gate",
        x=5,
        y=5,
        width=4,
        height=3,
        bg_color="transparent",
        border_color="transparent",
        graphic_code=NAND_GATE_PYICON_CODE
    )
    nand_gate.add_pin("A", -1, 0, color="#1d2536")
    nand_gate.add_pin("B", -1, 2, color="#1d2536")
    nand_gate.add_pin("Y", 4, 1, color="#1d2536")

    app.engine.rebuild_nets(app.wires, app.nodes)
    app.redraw_all()

    root.mainloop()