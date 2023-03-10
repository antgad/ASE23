# ### SYM
# Summarize a stream of symbols.

from math import log

class SYM:

    def __init__(self,at=0,txt=""): # Constructor
        self.n   = 0
        self.has = {}
        self.most = 0
        self.mode = None
        self.at=at
        self.txt=txt

    def add(self, x): # update counts of things seen so far         
        if x != '?':
            self.n += 1
            self.has[x] = 1 + (0 if not self.has.get(x) else self.has.get(x))
            if self.has[x] > self.most:
                self.most, self.mode = self.has[x], x
    
    def mid(self): # return the mode
        return self.mode
    
    def div(self): # return the entropy
        def fun(p): return p*log(p, 2)
        e = 0
        for _, n in self.has.items():
            e += fun(n/self.n)
        return -e
    def rnd(self,x,n):
        return x
    
    def dist(slef,s1,s2):
        if s1=="?" and s2=="?":
            return 1
        if s1==s2:
            return 0
        return 1
