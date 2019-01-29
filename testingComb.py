import itertools

def getComb(stuff):
    for L in range(0, len(stuff)+1):
        for subset in itertools.combinations(stuff, L):
            if subset:
                yield list(subset)
             
for var in getComb(xrange(0,5)):
    for r,n in enumerate(var):
        print n,r
