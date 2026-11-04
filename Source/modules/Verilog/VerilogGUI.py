# given path.

def spawnVerilog(app,path,node_editor,x=0,y=0):
    app.root.config(cursor="arrow")
    result = parseFileIntoObject(path,objonly = False)
    obj = result[0]
    name = obj.Name
    inputPins = result[1]
    outputPins = result[2]
    pyIcon = """
import math
name = "Verilog Component"
if 'node' in globals() and node is not None and hasattr(node, 'metadata') and node.metadata is not None:
    if hasattr(node.metadata, "Name"):
        name = node.metadata.Name
y_mid = y + h * (3.0 / 6.0)
cx = x + w / 2.0
cy = y + h / 2.0
txt_x, txt_y = rotatePoint(cx, cy, cx, cy, angle)
padding = 0.85  # Keep text within 85% of node width
char_count = max(len(name), 1)
size_from_w = int((w * padding) / (char_count * 0.6))
size_from_h = int(h * 0.4)  # Prevent text from overflowing height
font_size = max(6, min(size_from_w, size_from_h))
if font_size > 0:
    canvas.create_text(
        txt_x, txt_y,
        text=name, fill="#FFFFFF", anchor="center",
        font=("Arial", font_size, "bold"), tags=tags
    )"""
    node = node_editor.create_node(
        title=name,
        x=x,
        y=y,
        width=4,
        height=max(len(inputPins), len(outputPins)),
        bg_color="black",
        border_color="white",
        graphic_code=pyIcon,
        metadata=obj
    )
    for pin in inputPins:
        node.add_pin(pin.Name, -1, inputPins.index(pin), color="#222222")
    for pin in outputPins:
        node.add_pin(pin.Name, 4, outputPins.index(pin), color="#222222")
    app.addLogic(obj, node)


self.root.config(cursor="plus")
self.node_editor.grepNextPressGridPos(
    lambda x, y, app=self, p=path: spawnVerilog(app, p, app.node_editor, x, y)
)