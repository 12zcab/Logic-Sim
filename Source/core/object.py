class Object:
    def __init__(self, IOs, update):
        self.IO = IOs
        self.update = update

class IO:
    def __init__(self, father, name):
        self.father = father
        self.name = name
        self.connections = []
    def connect(io):
        self.father.connections[self.name] = io