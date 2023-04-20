from DATA import DATA
from NUM import NUM
import OPTIONS
from SYM import SYM
import os
from utils import *
import utils
from grid_utils import *
import json
import time
import pandas as pd
options=OPTIONS.OPTIONS()
import statistics
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt
help="""
xpln: multi-goal semi-supervised explanation
(c)2023
USAGE: lua xpln.lua [OPTIONS] [-g ACTIONS]
  
OPTIONS:
  -b  --bins    initial number of bins       = 16
  -c  --cliffs  cliff's delta threshold      = .147
  -d  --d       different is over sd*d       = .35
  -f  --file    data file                    = ../etc/project_data/china.csv
  -F  --Far     distance to distant          = .95
  -g  --go      start-up action              = nothing
  -h  --help    show help                    = false
  -H  --Halves  search space for clustering  = 512
  -m  --min     size of smallest cluster     = .5
  -M  --Max     numbers                      = 512
  -p  --p       dist coefficient             = 2
  -r  --rest    how many of rest to sample   = 10
  -R  --Reuse   child splits reuse a parent pole = true
  -s  --seed    random number seed           = 937162211
  -t  --Type   Distance Type(Eucledian/Jaccard) = 0

ACTIONS:
"""

# auto93.csv   coc1000.csv    healthCloseIsses12mths0001-hard.csv   nasa93dem.csv   SSM.csv
#  auto2.csv        china.csv    coc10000.csv   healthCloseIsses12mths0011-easy.csv   pom.csv    SSN.csv
def main(funs,saved={},fails=0):
    options.cli_setting(help)
    file_num = int(input("Enter file_num:"))
    start_time = time.time()
    file_list = ["auto2.csv", "auto93.csv", "china.csv", "coc1000.csv", "coc10000.csv", "healthCloseIsses12mths0001-hard.csv", "healthCloseIsses12mths0011-easy.csv", "nasa93dem.csv", "pom.csv", "SSM.csv", "SSN.csv"] 
    options['file'] = "../etc/project_data/" + file_list[file_num]
    df=pd.read_csv(options['file'],na_values='?')
    df.columns = df.columns.str.strip()
    le=LabelEncoder()
    for col in df.columns:
        if df[col].dtype.kind in 'biufc':
            temp=int(df[col].mean())
            df[col].fillna(temp,inplace=True)
        
        if df[col].dtype=='object'and col[0].islower():
            tmp=le.fit_transform(df[col])
            df[col]=tmp.copy()
            print("Label Encoding Applied to "+col)
            label_mapping = dict(zip(le.classes_, le.transform(le.classes_)))
            print(label_mapping)#json.dumps(label_mapping, indent=4))


    options['file']=options['file'][:-4]+"_updated.csv"
    df.to_csv(options['file'],index=False)
    for k,v in options.items():
        saved[k]=v
    with open("config.json", "w") as outfile:
        json.dump(saved, outfile)
    birth=time.time()
    best1=[]
    best2=[]
    xpln1=[]
    xpln2=[]
    times1=[]
    times2=[]
    iterator=[]
    data = DATA(options['file'])
    for i in range(50):
        iterator.append(i)
        start_time = time.time()
        best,rest, evals = data.sway()
        best1.append(best)
        rule,most=data.xpln(best,rest)
        xpln1.append((data.subset(utils.selects(rule,data.rows))))
        end_time = time.time()
        runtime = end_time - start_time
        times1.append(runtime)
    
    saved['Type']=1
    
    with open("config.json", "w") as outfile:
        json.dump(saved, outfile)
    data2 = DATA(options['file'])
    for i in range(50):
    
        start_time = time.time()
        best,rest, evals = data2.sway()
        best2.append(best)
        bextXpln,restXpln=data.xpln2(best,rest)
        xpln2.append((data.subset(bextXpln)))
        end_time = time.time()
        runtime = end_time - start_time
        times2.append(runtime)
    sways,xplns,bestValXpln1,bestValXpln2,bestValSway1,bestValSway2=utils.stats(data,best1,best2,xpln1,xpln2)
    print('++++++++++++++++++++++++++++++STATS++++++++++++++++++++++++++++++')

    
    print("Avg Runtime 1: "+str(statistics.mean(times1)))
    print("Avg Runtime 2: "+str(statistics.mean(times2)))
    print('all',o(data.stats(data.cols.y,2,what='mid')))
    print("Sway1: "+ str(bestValSway1))
    print("Sway2: "+ str(bestValSway2))
    print("Xpln1: "+ str(bestValXpln1))
    print("Xpln2: "+ str(bestValXpln2))
    top,_ = data.betters(len(best.rows))
    top = data.clone(top)
    print('sort with', len(data.rows), 'evals', o(top.stats(top.cols.y,2,what='mid')))
    plt.plot(range(len(times1)), times1, label='Sway1/Xpln1')
    plt.plot(range(len(times2)), times2, label='Sway2/Xpln2')
    plt.xlabel('Iteration')
    plt.ylabel('Runtime')
    plt.title('Runtime of iterations')
    plt.legend()
    plt.show()
    



    '''if options['help']:
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
                    print("✅ pass:", what)'''
        

    

    
    os.remove('config.json')
    exit(fails)

egs = {}

def eg(key,s,fun):
    global help
    egs[key] = fun
    help += "  -g  {}\t{}\n".format(key, s)

def disp_setting():
    oo(options)
    return str(options)

def test_sym():
    sym = SYM.SYM()

    for x in ["a", "a", "a", "a", "b", "b", "c"]:
        sym.add(x)

    print(sym.mid(), rnd(sym.div()))
    return rnd(sym.div()) == 1.38

def test_rand():
    Seed = 1
    t=[rint(0, 100) for i in range(1000)]
    Seed = 1    
    u=[rint(0, 100) for i in range(1000)]
    for k,v in enumerate(t):
        assert(v == u[k])

def test_some():
    options['Max'] = 32
    num1 = NUM.NUM()
    for i in range(1,10001):
        num1.add(i)
    # oo(num1.has)

def test_num():
    num1, num2 = NUM.NUM(), NUM.NUM()
    #global Seed
    Seed = options['seed']
    for i in range(10000):
        a,Seed=rand(0,1,Seed)
        num1.add(a)
    print(num1.mid())
    Seed = options['seed']
    for i in range(10000):
        a,Seed=rand(0,1,Seed)
        num2.add(a**2)
    print(num2.mid())

    m1 = rnd(num1.mid(),1)
    m2 = rnd(num2.mid(),1)
    d1 = rnd(num1.div(),1)
    d2 = rnd(num2.div(),1)
    print(1, m1, d1)
    print(2, m2, d2)

    return num1.mid()>num2.mid() and (0.5 == rnd(num1.mid(),1))

def helper_csv(t):
    global var
    var = var + len(t)

def test_csv():
    n = 0

    def f(t):
        nonlocal n
        n += len(t)

    csv(options['file'], f)
    print(options['file'], n)
    return n == 8 * 399

def test_data():
    data = DATA(options['file'])
    col=data.cols.x[1]
    # print(data.cols.x)
    print(col.lo, col.hi, col.mid(), col.div(), col)
    print(o(data.stats(data.cols.y, 2, what="mid")))
    
def test_clone():
    data1 = DATA(options['file'])
    data2 = data1.clone(data1.rows)
    print(data1.stats(data1.cols.y, 2, what="mid"))
    print(data2.stats(data2.cols.y, 2, what="mid"))

def test_cliffs():
    r1 = cliffsDelta([8,7,6,2,5,8,7,3],[8,7,6,2,5,8,7,3]) > options['cliffs']
    r2 = cliffsDelta([8,7,6,2,5,8,7,3],[9,9,7,8,10,9,6]) > options['cliffs']
    assert(False == r1)
    assert(True  == r2) 
    t1,t2=[],[]
    for i in range(1,1001):
        t1.append(rand(0,1)[0])
    for i in range(1,1001):
        t2.append(rand(0,1)[0]**.5)
    r1 = cliffsDelta(t1,t1) > options['cliffs']
    r2 = cliffsDelta(t1,t2) > options['cliffs']
    assert(False == r1) 
    assert(True  == r2) 
    diff =False
    j = 1.0
    while (not diff):
        def function(x):
            return x*j
        t3=list(map(function, t1))
        rx = cliffsDelta(t1,t3) > options['cliffs']
        diff= rx
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
    left,right,A,B,mid,c,_ = data.half() 
    print(len(left),len(right))
    l,r = data.clone(left), data.clone(right)
    print(A.cells, c)
    print(mid.cells) 
    print(B.cells)
    print("l", l.stats(l.cols.y, 2, what='mid'))
    print("r", r.stats(r.cols.y, 2, what="mid"))

def test_tree():
    data = DATA(options['file'])
    showTree(data.tree(),cols=data.cols.y, nPlaces=1, what="mid")

#


#eg('the','show options', disp_setting)
#eg('rand', 'demo random number generation', test_rand)
#eg("some","demo of reservoir sampling", test_some)
#eg('nums', 'demo of NUM', test_num)
#eg('sym', 'demo SYMS', test_sym)
#eg('csv', 'reading csv files', test_csv)
#eg('data', 'showing DATA sets', test_data)
#eg('clone', 'replicate structure of a DATA', test_clone)
#eg('cliffs', 'start tests', test_cliffs)
#eg('dist', 'distance test', test_dist)
#eg('half', 'divide data in half', test_half)
#eg('tree', 'make snd show tree of clusters', test_tree)
#eg('sway', 'optimizing', test_sway)
#eg('bins', 'find deltas between best and rest', test_bins)
#eg("xpln","explore explanation sets", test_xpln)

main(egs)



