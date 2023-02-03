# Miscellaneous support functions

import NUM
import SYM
import math
import re
import io

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
    y = (a**2 - x2**2)**0.5
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
    for k, v in enumerate(t):
        v, k = fun(k, v)
    if k:
        u[k] = v
    else:
        u[1 + len(u)] = v
    return u

'''
function map(t, fun,     u) --> t; map a function `fun`(v) over list (skip nil results) --DONE
  u={}; for k,v in pairs(t) do v,k=fun(v); u[k or (1+#u)]=v end;  return u end
 
function kap(t, fun,     u) --> t; map function `fun`(k,v) over list (skip nil results) --DONE
  u={}; for k,v in pairs(t) do v,k=fun(k,v); u[k or (1+#u)]=v; end; return u end

function sort(t, fun) --> t; return `t`,  sorted by `fun` (default= `<`) --Inbuilt
  table.sort(t,fun); return t end

function lt(x) --> fun;  return a function that sorts ascending on `x`
  return function(a,b) return a[x] < b[x] end end

function keys(t) --> ss; return list of table keys, sorted
  return sort(kap(t, function(k,_) return k end)) end

function push(t, x) --> any; push `x` to end of list; return `x` 
  table.insert(t,x); return x end

function push(t, x) --> any; push `x` to end of list; return `x` 
  table.insert(t,x); return x end

function any(t) return t[rint(#t)] end  --> x; returns one items at random

function many(t,n,    u)  --> t1; returns some items from `t`
   u={}; for i=1,n do u[1+#u]=any(t) end; return u end
'''

## Strings

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
