from collections import defaultdict

class Event:
    def __init__(self, targetIO, Val, Strength):
        self.targetIO = targetIO
        self.Val = Val
        self.Strength = Strength

class Kairos:
    def __init__(self):
        self.queue = defaultdict(lambda: defaultdict(list))
        self.currentTime = 0
        self.currentDelta = 0

    def schedule(self, targetIO, Val, Strength, Delay=0):
        if Delay == 0:
            targetTime = self.currentTime
            targetDelta = self.currentDelta + 1
        else:
            targetTime = self.currentTime + Delay
            targetDelta = 0
        self.queue[targetTime][targetDelta].append(Event(targetIO, Val, Strength))

    def hasCurrentEvent(self):
        return len(self.queue[self.currentTime]) > 0

    def getNextEvent(self):
        if not self.queue[self.currentTime]:
            return []
        nextDelta = min(self.queue[self.currentTime].keys())
        self.currentDelta = nextDelta
        events = self.queue[self.currentTime].pop(nextDelta)
        if not self.queue[self.currentTime]:
            del self.queue[self.currentTime]
        return events

    def advanceToNext(self):
        futureTimes = [t for t in self.queue.keys() if t > self.currentTime]
        if not futureTimes:
            if self.currentTime in self.queue and not self.queue[self.currentTime]:
                del self.queue[self.currentTime]
            return False
        self.currentTime = min(futureTimes)
        self.currentDelta = 0
        return True