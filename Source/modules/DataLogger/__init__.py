from core.object import *
from TVA import Snap
from tabulate import tabulate


# This creates a Component for collecting data in the simbox (maybe  bruh)
def Logger(Name,IOArray,MonitoredIO):
    DictIO = {}     
    for i in range(len(IOArray)):
        DictIO[IOArray[i]] = IO(IOArray[i])
        DictIO[IOArray[i]].connect(MonitoredIO[i])

    obj = Component(Name,DictIO,doLog) 

    # Return the created component
    return obj

def doLog(self):
    NetObjs = [[]]
    # IOs and Object connected data i Guess
    for IOObj in self.IO.values():
        NetObjs[0].append(IOObj.Value)
    print(str(self.Name) + "===" + str(self.simBox.scheduler.currentTime))
    print(tabulate(NetObjs, headers=self.IO.keys(), tablefmt="grid"))

    # Collect the data for prediction (ig, since when does logic simulator have )
    Snap.ComponentState(NetObjs)
   


## SUMMARIZE CHANGES FOR GUI 
    
 
 
   