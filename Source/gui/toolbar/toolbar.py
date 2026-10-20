import math
import os
import tkinter.font as tkFont
from tkinter import *


def rotatePoint(px, py, cx, cy, angle):
    rad = math.radians(angle)
    cos_a = math.cos(rad)
    sin_a = math.sin(rad)
    nx = cos_a * (px - cx) - sin_a * (py - cy) + cx
    ny = sin_a * (px - cx) + cos_a * (py - cy) + cy
    return nx, ny


class ToolBarButton(Canvas):

    def __init__(
        self,
        master,
        text="",
        pyiconPathRatio=None,
        command=None,
        bg="#202020",
        fg="#FFFFFF",
        active_bg="#333333",
    ):
        super().__init__(
            master, bg=bg, highlightthickness=0, bd=0, cursor="hand2"
        )

        self.text = text
        if pyiconPathRatio == None:
            self.pyicon_path = None
            self.pyicon_ratio = None
        else:
            self.pyicon_path = pyiconPathRatio[0]
            self.pyicon_ratio = pyiconPathRatio[1]
        self.command = command
        self.bg_color = bg
        self.fg_color = fg
        self.active_bg = active_bg
        self.is_hovered = False

        self.bind("<Configure>", self._on_resize)
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        self.bind("<Button-1>", self._on_click)

    def config(self, cnf=None, **kw):
        if "command" in kw:
            self.command = kw.pop("command")
        if cnf and "command" in cnf:
            self.command = cnf.pop("command")
        if kw or cnf:
            super().config(cnf, **kw)

    configure = config

    def _on_enter(self, event):
        self.is_hovered = True
        super().config(bg=self.active_bg)

    def _on_leave(self, event):
        self.is_hovered = False
        super().config(bg=self.bg_color)

    def _on_click(self, event):
        if self.command:
            self.command()

    def _on_resize(self, event):
        self.delete("all")
        w, h = event.width, event.height
        if w <= 1 or h <= 1:
            return
        if self.pyicon_path and os.path.exists(self.pyicon_path):
            max_box_h = int(h * 0.60) if self.text else int(h * 0.85)
            max_box_w = int(w * 0.85)
            
            img_w, img_h = self.pyicon_ratio[0], self.pyicon_ratio[1]
            actual_ratio = img_h / img_w
            
            test_h = max_box_w * actual_ratio
            
            if test_h <= max_box_h:
                icon_w = max_box_w
                icon_h = int(test_h)
            else:
                icon_h = max_box_h
                icon_w = int(max_box_h / actual_ratio)
                
            offset_x = (w - icon_w) / 2
            offset_y = (
                (((h * 0.60) - icon_h) / 2) if self.text 
                else ((h - icon_h) / 2)
            )
            calculated_zoom = min(icon_w / 4.0, icon_h / 3.0)
            icon_scope = {
                "canvas": self,
                "x": offset_x,
                "y": offset_y,
                "w": icon_w,
                "h": icon_h,
                "angle": 0,
                "zoom": calculated_zoom,
                "cx": offset_x + icon_w / 2,
                "cy": offset_y + icon_h / 2,
                "is_selected": False,
                "tags": ("icon_graphics",),
                "rotatePoint": rotatePoint,
                "math": math,
            }

            try:
                with open(self.pyicon_path, "r") as f:
                    code = f.read()
                exec(code, icon_scope)
            except Exception as e:
                print(f"Error rendering pyIcon {self.pyicon_path}: {e}")

        if self.text:
            text_y = h * 0.82 if self.pyicon_path else h / 2
            max_text_h = h * 0.25 if self.pyicon_path else h * 0.6
            max_text_w = w * 0.9

            font_size = max(6, int(max_text_h))
            test_font = tkFont.Font(
                family="Arial", size=font_size, weight="bold"
            )

            while (
                test_font.measure(self.text) > max_text_w
                or test_font.metrics("linespace") > max_text_h
            ) and font_size > 6:
                font_size -= 1
                test_font.configure(size=font_size)

            self.create_text(
                w / 2,
                text_y,
                text=self.text,
                fill=self.fg_color,
                font=test_font,
                anchor="center",
            )


class ToolBar(Frame):

    def __init__(self, master=None):
        super().__init__(master, bg="#111111")

        self.canvas = Canvas(
            self, height=50, highlightthickness=0, bd=0, bg="#111111"
        )
        self.scrollbar = Scrollbar(
            self,
            troughcolor="#111111",
            background="#222222",
            orient=HORIZONTAL,
            command=self.canvas.xview,
        )

        self.canvas.configure(xscrollcommand=self.scrollbar.set)

        self.scrollbar.pack(side=BOTTOM, fill=X)
        self.canvas.pack(side=TOP, fill=BOTH, expand=True)

        self.button_frame = Frame(self.canvas, bg="#111111")
        self.canvas.create_window((0, 0), window=self.button_frame, anchor="nw")

        self.button_containers = []
        self.buttons = []

        self.button_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            ),
        )
        self.canvas.bind("<Configure>", self._on_canvas_resize)

    def add_button(self, text, pyiconPathRatio=None):
        container = Frame(self.button_frame, bg="#111111")
        container.pack(side=LEFT, fill=Y, padx=2)
        container.pack_propagate(False)

        btn = ToolBarButton(container, text=text, pyiconPathRatio=pyiconPathRatio)
        btn.pack(fill=BOTH, expand=True)

        self.button_containers.append(container)
        self.buttons.append(btn)
        return btn

    def clear_buttons(self):
        for container in self.button_containers:
            container.destroy()

        self.button_containers.clear()
        self.buttons.clear()

        self.canvas.configure(scrollregion=(0, 0, 0, 0))

    def force_update(self):
        self.update_idletasks()
        height = self.canvas.winfo_height()
        for container in self.button_containers:
            container.config(width=height, height=height)
            for child in container.winfo_children():
                if isinstance(child, ToolBarButton):
                    child.event_generate("<Configure>")
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_canvas_resize(self, event):
        height = event.height
        for container in self.button_containers:
            container.config(width=height, height=height)

    def __init__(self, master=None):
        super().__init__(master, bg="#111111")

        self.canvas = Canvas(
            self, height=50, highlightthickness=0, bd=0, bg="#111111"
        )
        self.scrollbar = Scrollbar(
            self,
            troughcolor="#111111",
            background="#222222",
            orient=HORIZONTAL,
            command=self.canvas.xview,
        )

        self.canvas.configure(xscrollcommand=self.scrollbar.set)

        self.scrollbar.pack(side=BOTTOM, fill=X)
        self.canvas.pack(side=TOP, fill=BOTH, expand=True)

        self.button_frame = Frame(self.canvas, bg="#111111")
        self.canvas.create_window((0, 0), window=self.button_frame, anchor="nw")

        self.button_containers = []
        self.buttons = []

        self.button_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            ),
        )
        self.canvas.bind("<Configure>", self._on_canvas_resize)

    def add_button(self, text, pyiconPathRatio=None):
        container = Frame(self.button_frame, bg="#111111")
        container.pack(side=LEFT, fill=Y, padx=2)
        container.pack_propagate(False)

        btn = ToolBarButton(container, text=text, pyiconPathRatio=pyiconPathRatio)
        btn.pack(fill=BOTH, expand=True)

        self.button_containers.append(container)
        self.buttons.append(btn)
        return btn

    def clear_buttons(self):
        for container in self.button_containers:
            container.destroy()

        self.button_containers.clear()
        self.buttons.clear()

        self.canvas.configure(scrollregion=(0, 0, 0, 0))

    def _on_canvas_resize(self, event):
        height = event.height
        for container in self.button_containers:
            container.config(width=height, height=height)