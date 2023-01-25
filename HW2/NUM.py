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
    
function NUM.new(i,at,txt) --> NUM;  constructor; 
  i.at, i.txt = at or 0, txt or "" -- column position and name
  i.n, i.mu, i.m2 = 0, 0, 0
  i.lo, i.hi = math.huge, -math.huge 
  i.w = i.txt:find"-$" and -1 or 1 end

function NUM.add(i,n,    d) --> NUM; add `n`, update lo,hi and stuff needed for standard deviation
  if n ~= "?" then
    i.n  = i.n + 1
    d = n - i.mu
    i.mu = i.mu + d/i.n
    i.m2 = i.m2 + d*(n - i.mu)
    i.lo = math.min(n, i.lo)
    i.hi = math.max(n, i.hi) end end


if "-" in self.txt:
            self.w = -1
        else:
            self.w = 1

i.w = -1 if i.txt.find("-") != -1 else 1

