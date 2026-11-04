from core import *

class Label(Component):
    def __init__(self, Name):
        super().__init__(Name, [IO("Pin")], self.update)
        self.text = "Text"
    def update(self):
        pass
    
class TPS(Component):
    def __init__(self, Name):
        # Register self.update as the callback (or rename logic to update)
        super().__init__(Name, [], self.update)
        self.text = "TPS:NaN"
        self.deltaTickCount = 0
        self.lastupdate = None

    def update(self):
        pass
    def perdeltatick(self):
        now = time.perf_counter_ns()
        if self.lastupdate is None:
            self.lastupdate = now
            return
        self.deltaTickCount += 1
        if self.deltaTickCount >= 100:
            duration = now - self.lastupdate  # Time elapsed for 100 ticks in nanoseconds
            if duration > 0:
                tps = (100 * 1_000_000_000) / duration
                self.text = f"TPS:{round(tps, 2)}"
            else:
                self.text = "TPS:Inf"
            self.deltaTickCount = 0
            self.lastupdate = now