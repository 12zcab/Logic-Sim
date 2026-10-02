from nodeEngine import NodeEditor
app = NodeEditor()
app.addContainer("Box1", gridX=3, gridY=2, gridW=3, gridH=3, bg_color="#2A394A", border_color="#00ADB5")
app.addContainer("Box2", gridX=-7, gridY=-3, gridW=3, gridH=3, bg_color="#342A4A", border_color="#BB86FC")
app.containers["Box1"].addNode("Pin0", -1, 0)
app.containers["Box1"].addNode("Pin1", -1, 2)
app.containers["Box1"].addNode("PinOut", 3, 1, bg_color="#00ADB5")
app.containers["Box2"].addNode("Pin0", -1, 1)
app.containers["Box2"].addNode("PinOut", 3, 1, bg_color="#BB86FC")
app.addConnection("Box1", "Pin0", "Box2", "PinOut")
app.update_idletasks()
app.renderAll()
def custom_interval():
    for connection in app.connections:
        connection["Activated"] = not connection.get("Activated", True)
    app.renderAll()
    app.after(1000, app.interval)

app.interval = custom_interval
app.interval()
app.mainloop()
