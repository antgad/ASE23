# Miscellaneous support functions

import NUM
import SYM
import ROW
import math
import re
import io
from copy import deepcopy
import json
import random
# import OPTIONS
# options=OPTIONS.OPTIONS()

config= {}

## Show
def __init__(self, src):
    with open('config.json') as json_file:
            self.config = json.load(json_file)

def show(node, what=None, cols=None, nPlaces=1, lvl=0):
    if node:
        print("|" * lvl + str(len(node['data'.rows])) + " ", end='')
        if (not node.get('left')) or (lvl==0):
            print(o(node['data'].stats(node['data'].cols.y,nPlaces, what=what)))
        else: 
            print("")
        show(node.get('left'), what,cols, nPlaces, lvl+1)
        show(node.get('right'), what,cols,nPlaces, lvl+1)

def show_grid(node, what=None, cols=None, nPlaces=1, lvl=0):
    if node:
        # io.write("| "*lvl + str(node.data.rows) + "  ")
        print("|.."*lvl, end=" ")#+ str(len(node['data'].rows)), end= "  ")
        if (node.get('left')==None):
            print(o(node['data'].rows[-1].cells[-1]))
        else:
            print(rnd(100*node['c'], 0))
        show_grid(node.get('left'), what,cols, nPlaces, lvl+1)
        show_grid(node.get('right'), what,cols,nPlaces, lvl+1)


## Numerics
Seed=937162211

def rint(lo,hi):
    # return math.floor(0.5+ rand(lo,hi))
    x,_= rand(lo, hi)
    return math.floor(0.5 + x)

def rand(lo=0,hi=1, Seed= 937162211):
    #global Seed
   
    Seed = (16807 * Seed) % 2147483647
    return lo + (hi-lo) * Seed / 2147483647,Seed

def rnd(n,nPlaces=2):
    mult = pow(10,nPlaces)
    return math.floor(n*mult+0.5)/mult

def cosine(a,b,c):
    c = 1e-5 if c==0 else c
    # print(c)
    x1 = (a**2 + c**2 - b**2)/(2*c)
    x2 = max(0, min(1, x1))
    y = (abs(a**2 - x2**2))**0.5
    return x2, y

## Lists

def map(fun,src):
    for i in src:
        fun(i)

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
                u[len(u)] = v
    return u

def lt(x):
    return lambda a, b: a[x] < b[x]

def keys(t):
    return sorted(kap(t, lambda k, _: k))

def any(t,Seed=937162211): 
    random.seed(Seed)
    return random.choices(t)[0]

def many(t,n,Seed=937162211): 
    u=[]
    random.seed(Seed)
    return random.choices(t,k=n)

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
    type_t = type(t)
    if type_t==NUM.NUM or type_t==SYM.SYM or type_t==ROW.ROW:
        t = vars(t)
        t['a'] = str(type_t)
    if type(t)!=list and type(t)!=dict:
        return str(t)
    def fun(k, v):
        if "^_" not in str(k):
            return str(f':{o(k)} {o(v)} '), k
    if type(t)==list:
        return "{"+" ".join([str(i) for i in t]) +"}"
    else:
        temp = kap(t, fun)
        return str("{" + " ".join([str(temp[k]) for k in sorted(temp)]) + "}")
    

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

def dofile(filename = 'auto.csv'):
    """
        Function to read data from repgrid type file
    """
    with open(filename) as f:
        line = f.readline()
        while line:
            if line.startswith('local'):
                replace_underscore = '"' + line.split('"')[1] + '"'
            if line.startswith('return'):
                text = [line[line.find('{'):]]
                text += f.readlines()
            line = f.readline()
    # print(f'local _ = {replace_underscore}')
    for i, line in enumerate(text):
        line = line.strip().replace('=', ':').replace("'", '"').replace("_", replace_underscore)
        if len(line.split(':'))>1:
            k, v = line.split(':')
            line = '"' + k + '":' + v
        text[i] = line
    text = " ".join(text)
    pattern = re.compile("[{][a-zA-Z\d,\"\s\-]+[}]")
    res_match = re.finditer(pattern, text)
    while re.search(pattern, text):
        # print("while...")
        for l in res_match:
            text = text[:l.start()] + '[' + l.group(0)[1:-1] + ']' + text[l.end():]
        pattern = re.compile("[{]{1}[a-zA-Z\d,\"\[\]\s\-]+[}]{1}")
        res_match = re.finditer(pattern, text)
        # print("Next while")
    # print(text)
    return json.loads(text)

def cliffsDelta(self,ns1,ns2,Seed=937162211):
    if len(ns1)>256:
        ns1 = many(ns1,256, Seed)
    if len(ns2)>256:
        ns2 = many(ns2,256,Seed)
    if len(ns1)>10*len(ns2):
        ns1 = many(ns1,10*len(ns2),Seed)
    if len(ns2)>10*len(ns1):
        ns2 = many(ns2,10*len(ns1),Seed)
    n,gt,lt = 0,0,0
    with open('config.json') as json_file:
        config = json.load(json_file)
    for x in ns1:
        for y in ns2:
            n = n + 1
            if x>y:
                gt += 1
            if x < y:
                lt += 1
    return abs(lt - gt)/n > self.config['cliffs']


def showTree(node, what, cols, nPlaces, lvl = 0):
  if node:
    print("|.. "*lvl + "[" + str(len(node['data'].rows)) + "]", end= "  ")
    if (not node.get('left')) or (lvl==0):
        print(o(node['data'].stats(node['data'].cols.y,nPlaces, what="mid")))
    else: 
        print("")
    show(node.get('left'), what,cols,nPlaces, lvl+1)
    show(node.get('right'), what,cols,nPlaces, lvl+1)

def bins(cols,rowss):
    out = []
    for col in cols:
        ranges = {}
        for y,rows in rowss.items():
            for row in rows:
                x = row.cells[col.at]
                if (x != "?"):
                    k = int(bin(col,x))
                    if not k in ranges:
                        ranges[k] = RANGE(col.at,col.txt,x)
                    extend(ranges[k], x, y)
        ranges = list(dict(sorted(ranges.items(), key = lambda k:k[1].lo)).values())
        r = ranges if isinstance(col, SYM.SYM) else mergeAny(ranges)
        out.append(r)
    return out

def bin(self,col, x):
    with open('config.json') as json_file:
        config = json.load(json_file)
    if (x=="?") or (isinstance(col, SYM.SYM)):
        return x
    tmp = (col.hi - col.lo)/(self.config['bins']-1)
    if col.hi == col.lo:
        return 1
    else:
        return math.floor(x/tmp + .5)*tmp

def merge(col1,col2):
  new = deepcopy(col1)
  if isinstance(col1, SYM.SYM):
      for n in col2.has:
        new.add(n)
  else:
    for n in col2.has:
        new.add(new,n)
    new.lo = min(col1.lo,col2.lo)
    new.hi = max(col1.hi,col2.hi) 
  return new

def RANGE(at,txt,lo,hi=None):
    return {'at':at, 'txt':txt, 'lo':lo, 'hi':lo or hi or lo, 'y':SYM.SYM()}

def extend(range,n,s):
    range['lo'] = min(range['lo'], n)
    range['hi'] = max(range['hi'], n )
    range['y'].add(s)

def itself(x):
    return x

def value(has,nB = 1, nR = 1, sGoal = True):
    b,r = 0,0
    for x,n in has.items():
        if x == sGoal:
            b += n
        else:
            r += n
    b, r = b/(nB+1/float("inf")), r/(nR+1/float("inf"))
    return b**2/(b+r)

def merge2(col1,col2):
  new = merge(col1,col2)
  if new.div() <= (col1.div()*col1.n + col2.div()*col2.n)/new.n:
    return new
  
def mergeAny(ranges0):
    def noGaps(t):
        for j in range(1, len(t)):
            t[j]['lo'] = t[j-1]['hi']
        t[0]['lo'] = float("-inf")
        t[len(t)-1]['hi'] = float("inf")
        return t
    ranges1 = []
    j = 0
    while j <= (len(ranges0)-1):
        left=ranges0[j]
        if j ==len(ranges0) - 1:
            right = None
        else:
            right = ranges0[j+1]
        if right:
            y = merge2(left['y'],right['y'])
            if y:
                j += 1
                left['hi'], left['y'] = right['hi'], y
        ranges1.append(left)
        j = j+1
    if len(ranges0)==len(ranges1):
        return noGaps(ranges0)
    return mergeAny(ranges1)

def showRule(rule):
    def pretty(rangeR):
        return rangeR['lo'] if rangeR['lo']==rangeR['hi'] else [rangeR['lo'],rangeR['hi']]
    def merge(t0):
        right, left ={}, {}
        j = 1
        t = []
        while j<= len(t0):
            left = t0[j-1]
            right = None if j==len(t0) else t0[j]
            if right and right['hi'] == left['lo']:
                left['hi'] = right['hi']
                j += 1
            t.append({'lo': left['lo'], 'hi': left['hi']})
            J += 1
        return t if len(t0) == len(t) else merge(t)
    def merges(attr, ranges):
        return list(map(pretty,merge(sorted(ranges, key =  lambda k: k['lo'])))), attr
    return kap(rule, merges)


    pass

def selects(rule, rows):
    def disjunction(ranges, row):
        for range in ranges:
            lo,hi,at = range['lo'], range['hi'], range['ar']
            x = row.cells['at']
            if (x == '?') or (lo == hi == x) or (lo <= x and x < hi):
                return True
        return False

    def conjunction(row):
        for ranges in rule.values():
            if not disjunction(ranges, row):
                return False
        return True
    def fun(r):
        if conjunction(r):
            return r
    return(list(map(fun,rows)))

    pass

def per(t,p=0.5):
    p=math.floor(p*len(t))+0.5
    return t[max(1,min(len(t),p))]



def diffs(nums1,nums2):
    def fun(k,nums):
        return cliffsDelta(nums.has,nums2[k].has), nums.txt
    return kap(nums1,fun)

def firstN(sortedRanges,scoreFun):
    def printRange(r):
        print(r['range'].txt, r['range'].lo, r['range'].hi, rnd(r['val']), dict(r['range'].y.has))
    print()
    map( printRange, sortedRanges)
    first = sortedRanges[0]['val']
    print()
    def useful(range):
        if range['val'] > 0.05 and range['val'] > first/10:
            return range
    
    sortedRanges = list(map(useful, sortedRanges))
    most, out = -1, -1
    sortedRanges = [i for i  in sortedRanges if i != None]
    for n in range(1, len(sortedRanges)+1):
        temp, rule = scoreFun(i['range'] for i in sortedRanges[:n])
        if temp and temp>most:
            out, most = rule, temp
    return out, most





    
