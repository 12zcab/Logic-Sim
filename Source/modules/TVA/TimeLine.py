# For parallel execution of similar SimBox

# Notes, would u mind adding a special way to start simulation for parallel

from Source.gui import *
from core.object import *


class ParallelBox:

    def __init__(self, TargetBox):
        if not isinstance(TargetBox, list):
            TargetBox = [TargetBox]

        self.Container = {}
        for Target in TargetBox:
            self.Container[str(Target)] = Target

    def Launch(self):
        # Execute the parallel
        pass


    def CloneBox(self, BoxName, RunSpeed : int, RunTime  : int):
        if self.Container[BoxName]:
            self.Container[BoxName].append(RunSpeed, RunTime)

class Comparison:

    def __init__(self, OriBox : SimBox, ParallelList : ParallelBox):
        self.OriBox = OriBox
        self.ParallelBox = ParallelList

    def Compare():
        pass

    def SpecialFunction():
        pass


            
        