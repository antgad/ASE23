# ### NUM
# Summarizes a stream of numbers.

from math import inf

class NUM:

    def __init__(self, at, txt):
        self.at = at or 0, self.txt = txt or ""
        self.n, self.mu, self.m2 = 0, 0, 0
        self.lo, self.hi = inf, -inf
        self.w = -1 if "-" in self.txt else 1
    
    def add(self, n): # add `n`, update lo,hi and stuff needed for standard deviation
        if n != '?':
            self.n  = self.n + 1
            d = n - self.mu
            self.mu = self.mu + d/self.n
            self.m2 = self.m2 + d*(n - self.mu)
            self.lo = min(n, self.lo)
            self.hi = max(n, self.hi) 
    
    def mid(self): # return the mean
        return self.mu
    
    def div(self): # return standard deviation using Welford's algorithm http://t.ly/nn_W
        if self.m2 <0 or self.n < 2:
            return 0
        else:
            return (self.m2/(self.n-1))**0.5