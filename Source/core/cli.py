helptxt = r"""
ehhh
create something PythonRepresentation
PythonRepresentaion  (Print Result) direct execute 
run Speed [Tick]    Speed is must input but Tick is optional(Tick = how many tick u wanna run,leave blank for unlimited)
Ctrl-C to Escape from Run Loop
"""

from core.object import *
from modules import *
import time
import re
def safetyReplace(text, Dict):
    if not Dict:
        return text
    sorted_keys = sorted(Dict.keys(), key=len, reverse=True)
    pattern = re.compile(r'\b(' + '|'.join(map(re.escape, sorted_keys)) + r')\b')
    def replace_fn(match):
        key = match.group(0)
        return f'SafeVarVault["{key}"]'
    return pattern.sub(replace_fn, text)


title = r""".____                 .__         _________.__         
|    |    ____   ____ |__| ____  /   _____/|__| _____  
|    |   /  _ \ / ___\|  |/ ___\ \_____  \ |  |/     \ 
|    |__(  <_> ) /_/  >  \  \___ /        \|  |  Y Y  \
|_______ \____/\___  /|__|\___  >_______  /|__|__|_|  /
        \/    /_____/         \/        \/          \/ """
MagicBoxYay = SimBox([])
SafeVarVault = {} 
print(title)
while True:
    In = input(">")
    match In.split(maxsplit=1)[0].lower():
        case "create":
            Value = eval(safetyReplace(In.split(maxsplit=2)[-1],SafeVarVault))
            SafeVarVault[In.split(maxsplit=2)[-2]] = Value
            MagicBoxYay.addObject(SafeVarVault[In.split(maxsplit=2)[-2]])
        case "run":
            MagicBoxYay.expandNet()
            whileCond = len(In.split(' ')) >= 3
            if whileCond:
                RemainTick = In.split(' ')[2]
            else:
                RemainTick = 1
            SleepTick = In.split(' ', 1)[1]
            try:
                while RemainTick > 0:
                    time.sleep(float(SleepTick))
                    MagicBoxYay.update()
                    if whileCond:
                        RemainTick -= 1
            except KeyboardInterrupt:
                print("[LOGICSIM] Run Loop Escaped")
        case "help":
            print(helptxt)
        case _:
            print(eval(safetyReplace(In,SafeVarVault)))
