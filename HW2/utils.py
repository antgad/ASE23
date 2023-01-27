import NUM
import SYM
import math
import re

Seed=937162211

def rand(lo=0,hi=1):
    Seed = (16807 * Seed) % 2147483647
    return lo + (hi-lo) * Seed / 2147483647 



def rnd(n,nPlaces=3):
    mult = pow(10,nPlaces)
    return math.floor(n*mult+0.5)


def coerce(s):
    try:
        return int(s)
    except ValueError:
        try:
            return float(s)
        except ValueError:
            return True if re.match("^%s*(.-)%s*$", s)!=None else False


def csv(sFilename, fun, s, t):
    # TODO
    
    # with open(sFilename) as f:
    #     for s in f.readlines():
    #         t = []
    #         for s1 in s.split():  # s:gmatch("([^,]+)")
    #             t.append(coerce(s1))
    #         fun(t)
    
    pass

def map():
    # TODO
    pass

def kap():
    # TODO
    pass
