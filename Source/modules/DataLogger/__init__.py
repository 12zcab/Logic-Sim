from core.object import *
from tabulate import tabulate

def Logger(name,IOArray,MonitoredIO):
    DictIO = {}
    for i in range(len(IOArray)):
        DictIO[IOArray[i]] = CircuitIO(IOArray[i])
        DictIO[IOArray[i]].ConnectToIO(MonitoredIO[i])
    return CircuitObject(name,DictIO,doLog)
def doLog(self):
    data = [[]]
    for IO in self.IOs.values():
        data[0].append(IO.GetInput())
    print(tabulate(data, headers=self.IOs.keys(), tablefmt="grid"))