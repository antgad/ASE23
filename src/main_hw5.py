from DATA import DATA
from NUM import NUM
import OPTIONS
from SYM import SYM
import os
from utils import *
from grid_utils import *
import json
options=OPTIONS.OPTIONS()
help="""
data.py : an example csv reader script
(c)2023
USAGE:   data.py  [OPTIONS] [-g ACTION]
OPTIONS:
  -b  --bins    initial number of bins       = 16
  -c  --cliffs  cliff's delta threshold      = .147
  -F  --Far     distance to distant          = .95
  -g  --go      start-up action              = nothing
  -h  --help    show help                    = false
  -H  --Halves  search space for clustering  = 512
  -m  --min     size of smallest cluster     = .5
  -M  --Max     numbers                      = 512
  -p  --p       dist coefficient             = 2
  -r  --rest    how many of rest to sample   = 4
  -R  --Reuse   child splits reuse a parent pole = true
  -s  --seed    random number seed           = 937162211
ACTIONS:
"""

def main(funs,saved={},fails=0):

    options.cli_setting(help)
    for k,v in options.items():
        saved[k]=v
    with open("config.json", "w") as outfile:
        json.dump(saved, outfile)
    if options['help']:
        print(help)
    
    else:
        for what,fun in funs.items():
            if options['go'] =='all' or what ==options['go']:
                for k, v in saved.items():
                    options[k] = v

                if funs[what]() is False:
                    fails = fails + 1
                    print("❌ fail:", what)
                else:
                    print("✅ pass:", what)

    os.remove('config.json')
    exit(fails)

egs = {}

def eg(key,s,fun):
    global help
    egs[key] = fun
    help += "  -g  {}\t{}\n".format(key, s)

def disp_setting():
    return str(options)


def test_sym():
    sym = SYM.SYM()

    for x in ["a", "a", "a", "a", "b", "b", "c"]:
        sym.add(x)

    print(sym.mid(), rnd(sym.div()))
    return rnd(sym.div()) == 1.379

def test_rand():
    Seed = 1
    t=[]
    for i in range(1,1001):
        t.append(rint(0,100))
    
    u=[]
    for i in range(1,1001):
        u.append(rint(0,100))
    
    for k,v in enumerate(t):
        assert(v == u[k])

def test_some():
    options['Max'] = 32
    num1 = NUM.NUM()
    for i in range(1,1001):
        num1.add(i)
    print(num1.has)

def test_num():
    num1, num2 = NUM.NUM(), NUM.NUM()
    global Seed
    Seed = options['seed']
    for i in range(1,10**3+1):
        num1.add(rand(0,1))
    Seed = options['seed']
    for i in range(1,10**3+1):
        num2.add(rand(0,1)**2)
    m1 = rnd(num1.mid(),1)
    m2 = rnd(num2.mid(),1)
    d1 = rnd(num1.div(),1)
    d2 = rnd(num2.div(),1)
    print(1, m1, d1)
    print(2, m2, d2) 
    return (m1 > m2) and (0.5 == rnd(m1,1))

def helper_csv(t):
    global var
    var = var + len(t)

def test_csv():
    csv(options['file'], helper_csv)
    return (var == 3192)

def test_data():
    data = DATA(options['file'])
    col=data.cols.x[1]
    print(col.lo, col.hi, col.mid(), col.div())
    print(o(data.stats(data.cols.y, 2, what="mid")))

def test_clone():
    data1 = DATA(options['file'])
    data2 = data1.clone(data1.rows)
    print(data1.stats(data1.cols.y, 2, what="mid"))
    print(data2.stats(data2.cols.y, 2, what="mid"))

def test_cliffs():
    assert(False == cliffsDelta([8,7,6,2,5,8,7,3],[8,7,6,2,5,8,7,3]))
    assert(True  == cliffsDelta([8,7,6,2,5,8,7,3],[9,9,7,8,10,9,6])) 
    t1,t2=[],[]
    for i in range(1,1001):
        t1.append(rand(0,1))
    for i in range(1,1001):
        t2.append(rand(0,1)**.5)
    assert(False == cliffsDelta(t1,t1)) 
    assert(True  == cliffsDelta(t1,t2)) 
    diff =False
    j = 1.0
    while (not diff):
        def function(x):
            return x*j
        t3=list(map(function, t1))
        diff=cliffsDelta(t1,t3)
        print(">",rnd(j),diff) 
        j*=1.025

def test_dist():
    data = DATA(options['file'])
    num1  = NUM.NUM()
    for row in data.rows:
        num1.add(data.dist(row, data.rows[1]))
    print({'lo':num1.lo, 'hi':num1.hi, 'mid':rnd(num1.mid()), 'div':rnd(num1.div())})

def test_half():
    data = DATA(options['file'])
    left,right,A,B,mid,c = data.half() 
    print(len(left),len(right))
    l,r = data.clone(left), data.clone(right)
    print(A.cells, c)
    print(mid.cells) 
    print(B.cells)
    print("l", l.stats('mid', l.cols.y, 2))
    print("r", r.stats('mid', r.cols.y, 2))

def test_tree():
    data = DATA(options['file'])
    showTree(data.tree(), "mid" ,data.cols.y,1)

def test_sway():
    data = DATA(options['file'])
    best,rest = data.sway()
    print("\nall ", data.stats('mid', data.cols.y, 2))
    print("", data.stats('div', data.cols.y, 2))
    print("\nbest",best.stats('mid', best.cols.y, 2))
    print("", best.stats('div', best.cols.y, 2))
    print("\nrest", rest.stats('mid', rest.cols.y, 2))
    print("", rest.stats('div', rest.cols.y, 2))

def test_bins():
    global b4
    data = DATA(options['file'])
    best,rest = data.sway()
    print("all","","","",{'best':len(best.rows), 'rest':len(rest.rows)})
    for k,t in enumerate(bins(data.cols.x,{'best':best.rows, 'rest':rest.rows})):
        for range in t:
            if range['txt'] != b4:
                print("")
            b4 = range['txt']
            print(range['txt'],range['lo'],range['hi'],
            rnd(value(range['y'].has, len(best.rows),len(rest.rows),"best")), 
            range['y'].has)

eg('the', 'show options', disp_setting)
eg('rand', 'demo random number generation', test_rand)
eg('some', 'demo of reservoir sampling', test_some)
eg('nums', 'demo of NUM', test_num)
eg('sym', 'demo SYMS', test_sym)
eg('csv', 'reading csv files', test_csv)
eg('data', 'showing DATA sets', test_data)
eg('clone', 'replicate structure of a DATA', test_clone)
eg('cliffs', 'start tests', test_cliffs)
eg('dist', 'distance test', test_dist)
eg('half', 'divide data in half', test_half)
eg('tree', 'make snd show tree of clusters', test_tree)
eg('sway', 'optimizing', test_sway)
eg('bins', 'find deltas between best and rest', test_bins)
main(egs)

