from modules.SimpleCLIIO import *
from core.object import *
import time
button1 = keyboard_button("Button1", "space")
output1 = print_output("Output1", "Button1 pressed!")

button1.IOs["Out"].ConnectToIO(output1.IOs["In"])

box = SimBox(Objects=[button1, output1], Nets=[button1.IOs["Out"].connected_net])
while True:
    time.sleep(1)
    box.update()