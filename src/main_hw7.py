import random
from NUM import NUM
import OPTIONS
# from SYM import SYM
import os
# import utils
from stats import *
# from grid_utils import *
import json
options=OPTIONS.OPTIONS()
help="""
xpln: multi-goal semi-supervised explanation
(c)2023
USAGE: lua xpln.lua [OPTIONS] [-g ACTIONS]
  
OPTIONS:
  -b  --bootstrap    bootstrap               = 512
  -c  --cliff   cliff's delta threshold      = .4
  -C  --conf    conf                         = 0.05
  -D  --cohen   cohen                        = 0.35
  -F  --Fmt     Fmt                          = %6.2f
  -w  --width   width                        = 40
  -g  --go      start-up action              = nothing
  -h  --help    show help                    = false
  -M  --Max     numbers                      = 512
  
ACTIONS:
"""

def main(funs,saved={},fails=0):
    options.cli_setting(help)
    for k,v in options.items():
        saved[k]=v
    with open("config.json", "w") as outfile:
        json.dump(saved, outfile)
    # print('json dumped')
    load_configs()
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


def test_ok(n=1):
    random.seed(n)

def test_sample():
    for i in range(10):
        print("".join(samples(["a","b","c","d","e"])))

def test_num():
    num = NUM()
    for x in range(1,11): 
        num.add(x)
    print(num.n, num.mu, num.div())

def test_gauss():
    t = []
    n = NUM()
    for i in range(10**4):
        t.append(gaussian(10,2))
        n.add(t[-1])
    print(n.n, n.mu, n.sd)

def test_basic():
    print("\t\ttruee", 
            bootstrap( {8, 7, 6, 2, 5, 8, 7, 3}, {8, 7, 6, 2, 5, 8, 7, 3}),
            cliffsDelta( {8, 7, 6, 2, 5, 8, 7, 3}, {8, 7, 6, 2, 5, 8, 7, 3}))
    print("\t\tfalse", 
            bootstrap(  {8, 7, 6, 2, 5, 8, 7, 3},  {9, 9, 7, 8, 10, 9, 6}),
            cliffsDelta( {8, 7, 6, 2, 5, 8, 7, 3}, {9, 9, 7, 8, 10, 9, 6})) 
    print("\t\tfalse", 
            bootstrap({0.34, 0.49, 0.51, 0.6,   .34,  .49,  .51, .6}, 
                    {0.6,  0.7,  0.8,  0.9,   .6,   .7,   .8,  .9}),
            cliffsDelta({0.34, 0.49, 0.51, 0.6,   .34,  .49,  .51, .6}, 
                        {0.6,  0.7,  0.8,  0.9,   .6,   .7,   .8,  .9}))

def test_bootmu():
    a,b=[],[]
    for i in range(100):
        a.append(gaussian(10,1))
    print("","mu","sd","cliffs","boot","both")
    print("","--","--","------","----","----")
    for mu in range(100,111):
        mu = round(mu*0.1, 1)
        b=[]
        for i in range(100):
            b.append(gaussian(mu,1))
        cl=cliffsDelta(a,b)
        bs=bootstrap(a,b)
        print("",mu,1,cl,bs,cl and bs) 

def test_pre():
    print("\neg3")
    d=1.00
    for i in range(10):
        t1,t2=[], []
        for j in range(32):
            t1.append(gaussian(10,1))
            t2.append(gaussian(d*10,1))
        print("\t", round(d, 2), d<1.1, bootstrap(t1,t2), bootstrap(t1,t1))
        d=d+0.05

def test_five():
    for rx in tiles(scottKnot([
            RX([0.34,0.49,0.51,0.6,.34,.49,.51,.6],"rx1"),
            RX([0.6,0.7,0.8,0.9,.6,.7,.8,.9],"rx2"),
            RX([0.15,0.25,0.4,0.35,0.15,0.25,0.4,0.35],"rx3"),
            RX([0.6,0.7,0.8,0.9,0.6,0.7,0.8,0.9],"rx4"),
            RX([0.1,0.2,0.3,0.4,0.1,0.2,0.3,0.4],"rx5")])):
        print(rx.name,rx.rank,rx.show)

def test_six():
    for rx in tiles(scottKnot([
            RX([101,100,99,101,99.5,101,100,99,101,99.5],"rx1"),
            RX([101,100,99,101,100,101,100,99,101,100],"rx2"),
            RX([101,100,99.5,101,99,101,100,99.5,101,99],"rx3"),
            RX([101,100,99,101,100,101,100,99,101,100],"rx4")])):
        print(rx.name,rx.rank,rx.show)

def test_tiles():
    rxs,a,b,c,d,e,f,g,h,j,k=[],[],[],[],[],[],[],[],[],[],[]
    a = [gaussian(10,1) for _ in range(1000)]       # 1
    b = [gaussian(10.1,1) for _ in range(1000)]     # 2
    c = [gaussian(20,1) for _ in range(1000)]       # 3
    d = [gaussian(30,1) for _ in range(1000)]       # 4
    e = [gaussian(30.1,1) for _ in range(1000)]     # 5
    f = [gaussian(10,1) for _ in range(1000)]       # 6
    g = [gaussian(10,1) for _ in range(1000)]       # 7
    h = [gaussian(40,1) for _ in range(1000)]       # 8
    j = [gaussian(40,3) for _ in range(1000)]       # 9
    k = [gaussian(10,1) for _ in range(1000)]       # 10
    for i,v in enumerate([a,b,c,d,e,f,g,h,j,k]):
        rxs.append(RX(v, "rx" + str(i+1)))
    rxs.sort(key = lambda x: x.mid())
    for rx in tiles(rxs):
        print("",rx.name,rx.show)

def test_sk():
    rxs = []
    a = [gaussian(10,1) for _ in range(1000)]       # 1
    b = [gaussian(10.1,1) for _ in range(1000)]     # 2
    c = [gaussian(20,1) for _ in range(1000)]       # 3
    d = [gaussian(30,1) for _ in range(1000)]       # 4
    e = [gaussian(30.1,1) for _ in range(1000)]     # 5
    f = [gaussian(10,1) for _ in range(1000)]       # 6
    g = [gaussian(10,1) for _ in range(1000)]       # 7
    h = [gaussian(40,1) for _ in range(1000)]       # 8
    j = [gaussian(40,3) for _ in range(1000)]       # 9
    k = [gaussian(10,1) for _ in range(1000)]       # 10
    for i,v in enumerate([a,b,c,d,e,f,g,h,j,k]):
        rxs.append(RX(v, "rx" + str(i+1)))
    for rx in tiles(scottKnot(rxs)):
        print("",rx.rank,rx.name,rx.show)


eg("ok","set randomseed", test_ok)
eg('sample', 'demo random number generation', test_sample)
eg('nums', 'demo of NUM', test_num)
eg('gauss', 'test gauss', test_gauss)
eg('basic', 'test bootstrap and cliffsDelta', test_basic)
eg('bootmu', 'test bootstrap', test_bootmu)
eg('pre', 'test bootstrap eg3', test_pre)
eg('five', 'test tiles and scottKnot', test_five)
eg('six', 'test tiles and scottKnot', test_six)
eg('tiles', 'test tiles', test_tiles)
eg('sk', 'test scottKnot', test_sk)

main(egs)
