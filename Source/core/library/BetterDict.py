class BetterDict(dict):
    def __getattr__(self, Name):
        if Name in self:
            return self[Name]
        raise AttributeError(f"'BetterDict' object has no attribute '{Name}'")
    def __setattr__(self,Name,Value):
        self[Name] = [Value]
    def __delattr__(self,Name):
        if Name in self:
            del self[Name]
        else:
            raise AttributeError(f"'BetterDict' object has no attribute '{Name}'")