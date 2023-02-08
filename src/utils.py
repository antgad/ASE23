# Miscellaneous support functions

import NUM
import SYM
import math
import re
import io
from copy import deepcopy

## Show

def repCols(cols):
    #TODO
    cols=copy(cols)
    # for _,col in pairs(cols) do
    #     col[#col] = col[1]..":"..col[#col]
    #     for j=2,#col do col[j-1] = col[j] end
    #     col[#col]=nil end 
    # table.insert(cols,1,kap(cols[1], function(k,v) return "Num"..k end))
    # cols[1][#cols[1]]="thingX"
    # return DATA(cols)

# function repCols(cols)
#   cols=copy(cols)
#   for _,col in pairs(cols) do
#     col[#col] = col[1]..":"..col[#col]
#     for j=2,#col do col[j-1] = col[j] end
#     col[#col]=nil end 
#   table.insert(cols,1,kap(cols[1], function(k,v) return "Num"..k end))
#   cols[1][#cols[1]]="thingX"
#   return DATA(cols)
#   end

def show(node, what, cols, nPlaces, lvl=0):
    if node:
        # io.write("| "*lvl + str(node.data.rows) + "  ")
        print("| "*lvl + str(len(node['data'].rows)), end= "  ")
        if (not node.get('left')) or (lvl==0):
            print(o(node['data'].stats(node['data'].cols.y,nPlaces, what="mid")))
        else: 
            print("")
        show(node.get('left'), what,cols, nPlaces, lvl+1)
        show(node.get('right'), what,cols,nPlaces, lvl+1)


## Numerics
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

def cosine(a,b,c):
    x1 = (a**2 + c**2 - b**2)/(2*c)
    x2 = max(0, min(1, x1))
    y = (abs(a**2 - x2**2))**0.5
    return x2, y

## Lists

def map(t, fun): 
    u={}
    for k, v in enumerate(t):
        v, k = fun(v)
        if v!=None:
            if k:
                u[k] = v
            else:
                u[1 + len(u)] = v
    return u

def kap(t, fun):
    u={}
    if type(t)!=dict:
        t = dict(enumerate(t))
    for k, v in t.items():
        v, k = fun(k, v)
        if v!=None:
            if k:
                u[k] = v
            else:
                u[1 + len(u)] = v
    return u

def lt(x):
    return lambda a, b: a[x] < b[x]

def keys(t):
    return sorted(kap(t, lambda k, _: k))

def any(t): return t[rint(0,len(t)-1)]

def many(t,n): 
    u=[]
    for _ in range(n):
        u.append(any(t)) 
    return u

def copy(t):
    """
        Returns deep copy of t
    """
    return deepcopy(t)

## Strings

def oo(t): 
    print(o(t))
    return t 


def o(t, isKeys=None):
    if type(t)!=list and type(t)!=dict:
        return str(t)
    def fun(k, v):
        if "^_" not in str(k):
            return str(f':{o(k)} {o(v)} '), k
    if type(t)==list:
        return "{"+" ".join([str(i) for i in t]) +"}"
    else:
        temp = kap(t, fun)
        return str("{" + " ".join([str(temp[k]) for k in sorted(temp)]))
    

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

def dofile(sFilename):
    #TODO
    data_dict = {}
    return data_dict
