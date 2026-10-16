string = input()
numarray = list(string)
numset = set(numarray)
base = len(numset)
ans = 0
seen = {}
for i in range(len(numarray)):
    if not numarray[i] in seen.keys():
        if len(seen) == 0:
            seen[numarray[i]] = 1
        elif len(seen) == 1:
            seen[numarray[i]] = 0
        else:
            seen[numarray[i]] = len(seen)
    value = seen[numarray[i]]
    index = len(numarray) - i - 1
    ans += value * (base ** index)
print("Ans is:",ans)
# To people that feels kinda confused when seeing this document, erm this is just a small practice in CS :|