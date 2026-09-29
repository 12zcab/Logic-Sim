from tkinter import *

class NodeEditor(Tk):
    def __init__(self):
        super().__init__()
        self.title("Node Editor")
        self.geometry("800x600")
        
        self.canvas = Canvas(self, bg="#1e1e1e", highlightthickness=0)
        self.canvas.pack(fill=BOTH, expand=True)
        
        # Mouse bindings
        self.canvas.bind("<ButtonPress-1>", self.on_press)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)
        
        self.canvas.bind("<MouseWheel>", self.on_mouse_wheel)
        self.canvas.bind("<Button-4>", self.on_mouse_wheel)  # Linux scroll up
        self.canvas.bind("<Button-5>", self.on_mouse_wheel)  # Linux scroll down
        
        self.canvas.bind("<ButtonPress-2>", self.start_pan)
        self.canvas.bind("<B2-Motion>", self.pan_canvas)
        
        self.zoom = 1.0
        self.pan_x = 0.0
        self.pan_y = 0.0
        self.grid_size = 5
        
        self.logical_nodes = {}
        self.selected_node_name = None
        self.drag_offset_logical_x = 0.0
        self.drag_offset_logical_y = 0.0
        
        self.addRect("GreenBox", 50, 30, 110, 80, "#00ff88")
        self.addRect("RedBox", -60, -40, -10, 10, "#ff0022")
        
        self.update_idletasks()
        self.render_all()

    def addRect(self, name, x0, y0, x1, y1, colour="#00ff88"):
        self.logical_nodes[name] = {
            "x": float(x0), "y": float(y0),
            "w": float(x1 - x0), "h": float(y1 - y0),
            "colour": colour,
            "canvas_id": None
        }

    def get_center(self):
        w = max(self.canvas.winfo_width(), 800)
        h = max(self.canvas.winfo_height(), 600)
        return w / 2, h / 2, w, h

    def to_logical_space(self, win_x, win_y):
        cx, cy, _, _ = self.get_center()
        log_x = (win_x - cx - self.pan_x) / self.zoom
        log_y = (win_y - cy - self.pan_y) / self.zoom
        return log_x, log_y

    def to_window_space(self, log_x, log_y):
        cx, cy, _, _ = self.get_center()
        win_x = log_x * self.zoom + cx + self.pan_x
        win_y = log_y * self.zoom + cy + self.pan_y
        return win_x, win_y

    def render_all(self):
        self.canvas.delete("all")
        cx, cy, w, h = self.get_center()
        
        log_left, log_top = self.to_logical_space(0, 0)
        log_right, log_bottom = self.to_logical_space(w, h)
        
        step = self.grid_size
        start_x = (int(log_left) // step) * step
        start_y = (int(log_top) // step) * step
        
        # Draw grid lines
        for lx in range(start_x, int(log_right) + step, step):
            wx, _ = self.to_window_space(lx, 0)
            self.canvas.create_line(wx, 0, wx, h, fill="#2b2b2b", tags="grid_line")
            
        for ly in range(start_y, int(log_bottom) + step, step):
            _, wy = self.to_window_space(0, ly)
            self.canvas.create_line(0, wy, w, wy, fill="#2b2b2b", tags="grid_line")

        for name, node in self.logical_nodes.items():
            x0, y0 = self.to_window_space(node["x"], node["y"])
            x1, y1 = self.to_window_space(node["x"] + node["w"], node["y"] + node["h"])
            node["canvas_id"] = self.canvas.create_rectangle(x0, y0, x1, y1, fill=node["colour"], tags="node")
            
        self.canvas.tag_lower("grid_line")

    def on_mouse_wheel(self, event):
        cx, cy, _, _ = self.get_center()
        if event.num == 4 or event.delta > 0:
            scale_factor = 1.1
        else:
            scale_factor = 0.9
        mx, my = event.x, event.y
        self.pan_x = (mx - cx) - scale_factor * (mx - cx - self.pan_x)
        self.pan_y = (my - cy) - scale_factor * (my - cy - self.pan_y)
        self.zoom *= scale_factor
        self.render_all()

    def start_pan(self, event):
        self.drag_start_x = event.x
        self.drag_start_y = event.y

    def pan_canvas(self, event):
        self.pan_x += event.x - self.drag_start_x
        self.pan_y += event.y - self.drag_start_y
        self.drag_start_x = event.x
        self.drag_start_y = event.y
        self.render_all()
        
    def on_press(self, event):
        clicked_items = self.canvas.find_withtag("current")
        if clicked_items and "node" in self.canvas.gettags(clicked_items[0]):
            clicked_id = clicked_items[0]
            for name, node in self.logical_nodes.items():
                if node["canvas_id"] == clicked_id:
                    self.selected_node_name = name
                    break
            if self.selected_node_name:
                node = self.logical_nodes.pop(self.selected_node_name)
                self.logical_nodes[self.selected_node_name] = node
                mouse_log_x, mouse_log_y = self.to_logical_space(event.x, event.y)
                self.drag_offset_logical_x = mouse_log_x - node["x"]
                self.drag_offset_logical_y = mouse_log_y - node["y"]
                self.render_all()
    def on_drag(self, event):
        if self.selected_node_name:
            node = self.logical_nodes[self.selected_node_name]
            mouse_log_x, mouse_log_y = self.to_logical_space(event.x, event.y)
            
            target_logical_x = mouse_log_x - self.drag_offset_logical_x
            target_logical_y = mouse_log_y - self.drag_offset_logical_y
            
            # Snap position to grid step
            snap_x = round(target_logical_x / self.grid_size) * self.grid_size
            snap_y = round(target_logical_y / self.grid_size) * self.grid_size
            
            if node["x"] != snap_x or node["y"] != snap_y:
                node["x"] = snap_x
                node["y"] = snap_y
                self.render_all()

    def on_release(self, event):
        self.selected_node_name = None

if __name__ == "__main__":
    app = NodeEditor()
    app.mainloop()