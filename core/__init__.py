import random
from module.enum import *
from module.chronos import *
from module.object import *
from module.logger import *
import time
if __name__ == "__main__":
    PROPAGATION_DELAY = 1
    def NotGate(comp, SimBox):
        inVal = comp.IO["IN"].readVal
        outVal = Logic.ONE if inVal == Logic.ZERO else Logic.ZERO
        comp.IO["OUT"].setPower(outVal, Strength.STRONG, Delay=PROPAGATION_DELAY, SimBox=SimBox)
    notGate1 = Component("NOT_1", [IO("IN"), IO("OUT")], NotGate)
    notGate1.IO["OUT"] >> notGate1.IO["IN"]
    sim = SimBox([notGate1])
    sim.init()
    currentTimeStamp = time.process_time_ns()
    for _ in range(10000):
        sim.stepDeltaLoop()
        currentT = sim.scheduler.currentTime
        pinState = notGate1.IO["OUT"].readVal
        print(f"[Time: {currentT:2d} ns]  NOT_1_OUT = {pinState}  (Driving Strength: STRONG)")
        if not sim.scheduler.advanceToNext():
            break
    finishTimeStamp = time.process_time_ns()
    print((finishTimeStamp - currentTimeStamp) / 10000)