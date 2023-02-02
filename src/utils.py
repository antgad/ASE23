import NUM
import SYM
import math
import re
import io
Seed=937162211

def rint(lo,hi):
    return math.floor(0.5+ rand(lo,hi))

def rand(lo=0,hi=1):
    global Seed
    Seed = (16807 * Seed) % 2147483647
    return lo + (hi-lo) * Seed / 2147483647  



def rnd(n,nPlaces=3):
    mult = pow(10,nPlaces)
    return math.floor(n*mult+0.5)/mult


def coerce(s):
    try:
        return int(s)
    except ValueError:
        try:
            return float(s)
        except ValueError:
            if s.lower()=='true':
                return True
            if s.lower()=='false':
                return False
            return s


def csv(sFilename, fun):
    # TODO
    
    f=io.open(sFilename)
    while True:
        s=f.readline().rstrip()
        if s:
            t=[]
            for s1 in re.findall("([^,]+)",s):
                t.append(coerce(s1))
            fun(t)
        else:
            return f.close()
    
    pass

def map():
    u=[]
    #TODO
    pass

def kap(a,b):
    # TODO
    pass
