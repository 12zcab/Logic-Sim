from tkinter import *

class ToolBar(Frame):
    def __init__(self, master=None):
        super().__init__(master)

        self.canvas = Canvas(self, height=50, highlightthickness=0, bd=0)
        self.scrollbar = Scrollbar(self, orient=HORIZONTAL, command=self.canvas.xview)
        
        self.canvas.configure(xscrollcommand=self.scrollbar.set)
        
        self.scrollbar.pack(side=BOTTOM, fill=X)
        self.canvas.pack(side=TOP, fill=BOTH, expand=True)

        self.button_frame = Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.button_frame, anchor="nw")

        self.buttons = []
        self.button_containers = []
        for i in range(1, 25):
            container = Frame(self.button_frame)
            container.pack(side=LEFT, fill=Y)
            container.pack_propagate(False)

            btn = Button(container, text=f"B{i}")
            btn.pack(fill=BOTH, expand=True)

            self.button_containers.append(container)
            self.buttons.append(btn)

        self.button_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind("<Configure>", self._on_canvas_resize)

    def _on_canvas_resize(self, event):
        height = event.height
        for container in self.button_containers:
            container.config(width=height, height=height)
        if self.canvas.find_withtag("all"):
            self.canvas.itemconfig(self.canvas.find_withtag("all")[0], height=height)