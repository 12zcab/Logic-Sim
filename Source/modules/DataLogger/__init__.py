from core.object import *
from tabulate import tabulate

def Logger(Name,IOArray,MonitoredIO):
    DictIO = {}
    for i in range(len(IOArray)):
        DictIO[IOArray[i]] = IO(IOArray[i])
        DictIO[IOArray[i]].connect(MonitoredIO[i])
    obj = Component(Name,DictIO,doLog)
    obj.isObserver = True
    return obj
def doLog(self):
    data = [[]]
    for IOObj in self.IO.values():
        data[0].append(IOObj.Value)
    print(tabulate(data, headers=self.IO.keys(), tablefmt="grid"))