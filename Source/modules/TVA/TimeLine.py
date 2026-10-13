# For parallel execution of similar SimBox

# Notes, would u mind adding a special way to start simulation for parallel
# Mid change vars bruh
# Forget the below

# Can be accessed by Gui Engine i think

from Source.gui import *
from core.object import *


class ParallelContainer:  
    def __init__(self, List):
        self.Container = {}
        self.List = List

    def Launch(self):
        # Execute the parallel
        for BoxRequested in self.List:
            Found = self.Container[BoxRequested]

            if not Found:
                print("Require the box in container")

            print("Execute")
            Results.append("Bruh")

        Results = Comparison.Compare(self.List, Results)
        return 
    
    def DefineClone(self, SpecialChange, Name):
 
        if not self.Container[str(Name)]:
            return print("CloneBox does not exist") 
          
        for ChangeVar, NewValue in SpecialChange:   
            self.Container[str(Name)][ChangeVar] = NewValue
   
class Comparison: 
    @staticmethod
    def Compare(List, Results):
        Different = []
        for Box1, Box2 in List:
            for key1, item1 in Results[Box1]:
                for key2, item2 in Results[Box2]:
                    if key1 == key2:
                        if not item1 == item2:
                            print(f" {key1} : {item1} / {item2}  [from {Box1.Name} and {Box2.name}]")
                            Different.append(key1)

        return Different         