from modules.SimpleCLIIO import *
from core.object import *
import time
button1 = keyboard_button("Button1", "space")
output1 = print_output("Output1", "Button1 pressed!")

button1.IO["Out"].connect(output1.IO["In"])

box = SimBox([button1, output1],[button1.IO["Out"].Net])
while True:
    time.sleep(0.1)
    box.update()