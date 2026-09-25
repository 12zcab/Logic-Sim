helpTxt = r"""
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
import sys
import traceback 
def safeEval(expression, context=None):
    try:
        result = eval(expression, context)
        return result
    except Exception as e:
        print(f"Eval Error in [{expression}]: \n{e}")
        return "Error"
def clear_terminal_input_buffer(): 
    try:
        import msvcrt
        while msvcrt.kbhit():
            msvcrt.getch()
    except ImportError:
        import select
        while select.select([sys.stdin], [], [], 0.0)[0]:
            sys.stdin.read(1)
def safetyReplace(text, Dict):
    if not Dict:     
        return text
    sorted_keys = sorted(Dict.keys(), key=len, reverse=True)
    pattern = re.compile(r'\b(' + '|'.join(map(re.escape, sorted_keys)) + r')\b')
    def replace_fn(match):
        key = match.group(0)
        return f'varVault["{key}"]'
    return pattern.sub(replace_fn, text)
 

title = r""".____                 .__         _________.__         
|    |    ____   ____ |__| ____  /   _____/|__| _____  
|    |   /  _ \ / ___\|  |/ ___\ \_____  \ |  |/     \ 
|    |__(  <_> ) /_/  >  \  \___ /        \|  |  Y Y  \
|_______ \____/\___  /|__|\___  >_______  /|__|__|_|  /
        \/    /_____/         \/        \/          \/ """
mainBox = SimBox([])
varVault = {}
print(title) 
while True:  
    inString = input(">") 
    if inString == "":  
        continue
    match inString.split(maxsplit=1)[0].lower(): 
        case "create": 
            Value = safeEval(safetyReplace(inString.split(maxsplit=2)[-1],varVault))
            varVault[inString.split(maxsplit=2)[-2]] = Value
            mainBox.addObject(varVault[inString.split(maxsplit=2)[-2]])
        case "run":
            mainBox.expandNet()
            tickFlag = len(inString.split(' ')) >= 3
            total_ticks = 0
            if tickFlag:
                remainTick = int(inString.split(' ')[2])
            else:
                remainTick = 1
            sleepTick = inString.split(' ', 2)[1] 
            start_time = time.perf_counter()
            try:
                while remainTick > 0: 
                    total_ticks += 1
                    time.sleep(float(sleepTick))
                    mainBox.update()
                    if tickFlag:
                        remainTick -= 1
            except KeyboardInterrupt:
                print("[LOGICSIM] Run Loop Escaped")
                clear_terminal_input_buffer()
            end_time = time.perf_counter() 
            elapsed_time = end_time - start_time
            average_tps = total_ticks / elapsed_time if elapsed_time > 0 else 0
            print("Average Tick Per Second:" + str(average_tps))
        case "help":
            print(helpTxt)
        case "reset":
            varVault = {}
            mainBox = SimBox([])
        case _:
            print(safeEval(safetyReplace(inString,varVault)))
            
            

