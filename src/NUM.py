# ### NUM
# Summarizes a stream of numbers.

from math import inf,pow
from utils import rnd, rand, rint
import json


class NUM:

    def __init__(self, at = 0, txt = ""):
        self.at = at
        self.txt = txt
        self.n, self.mu, self.m2 = 0, 0, 0
        self.lo, self.hi = float(inf), -float(inf)
        self.w = -1 if self.txt.endswith('-') else 1
        self.has = {}
        self.ok = True
        self.config={}
        with open('config.json') as json_file:
            self.config = json.load(json_file)

    
    def add(self, x,n=1): # add `n`, update lo,hi and stuff needed for standard deviation
        if x != '?':
            self.n  = self.n + 1
            '''d = x - self.mu
            self.mu += d/self.n
            self.m2 += d*(n - self.mu)'''
            self.lo = min(n, self.lo)
            self.hi = max(n, self.hi) 
            all = len(self.has)
            t,_ = rand()
            if self.config["Max"] > all:
                pos = all+1
            elif t<self.config['Max']/self.n:
                pos = rint(1,all)
            else: 
                pos = 0
            if pos:
                self.has[pos] = x
                self.ok = False

    def has_f(self):
        temp = list(dict(sorted(self.has.items(),key=lambda k: k[1])).values())
        self.ok = True
        return temp

            
    
    def mid(self): # return the mean
        return self.mu
    
    def div(self): # return standard deviation using Welford's algorithm http://t.ly/nn_W
        if self.m2 <0 or self.n < 2:
            return 0
        else:
            return (self.m2/(self.n-1))**0.5

    def rnd(self,x,n):
        if x == "?":
            return x
        else:
            return rnd(x,n)

    def norm(self,n):
        if n=="?":
            return n
        return (n-self.lo)/(self.hi-self.lo+pow(10,-32))

    def dist(self,n1,n2):
        if n1=="?" and n2=="?":
            return 1
        n1,n2= self.norm(n1),self.norm(n2)
        if n1=="?":
            if n2<0.5:
                n1=1
            else:
                n1=0
        if n2=="?":
            if n1<0.5:
                n2=1
            else:
                n2=0
        return abs(n1-n2)