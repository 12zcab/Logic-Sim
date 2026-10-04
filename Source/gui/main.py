from tkinter import *
from .node.nodeEngine import *
from .toolbar.toolbar import *
from .connector import *
root = Tk()
root.title("LogicSim - Node Editor")
root.geometry("900x700")

paned_window = PanedWindow(
    root,
    orient=VERTICAL,
    sashwidth=6,
    sashrelief=RAISED,
    bg="#2D2D2D"
)
paned_window.pack(fill=BOTH, expand=True)

toolbar = ToolBar(master=paned_window)
node_editor = NodeEditor(master=paned_window)

paned_window.add(toolbar, minsize=40, height=80)
paned_window.add(node_editor, minsize=200)

moduleJsons = guiJsonPaths()

addBox = toolbar.add_button("Add Box")
addBox.config(command=lambda: node_editor.addContainer("Box", gridX=3, gridY=2, gridW=3, gridH=3, bg_color="#2A394A", border_color="#00ADB5"))
root.mainloop()