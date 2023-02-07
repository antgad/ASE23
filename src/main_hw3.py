from DATA import DATA
from NUM import NUM
import OPTIONS
from SYM import SYM
import os
from utils import *
import json
options=OPTIONS.OPTIONS()
help="""
data.py : an example csv reader script
(c)2023
USAGE:   data.py  [OPTIONS] [-g ACTION]
OPTIONS:
  -d  --dump    on crash, dump stack   = false
  -f  --file    name of file           = ../etc/data/auto93.csv
  -F  --Far     distance to "faraway"  = .95
  -g  --go      start-up action        = data
  -h  --help    show help              = false
  -m  --min     stop clusters at N^min = .5
  -p  --p       distance coefficient   = 2
  -s  --seed    random number seed     = 937162211
  -S  --Sample  sampling data size     = 512
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

    return "a" == sym.mid() and 1.379 == rnd(sym.div(), 3)


def test_num():
    num = NUM.NUM()

    for x in [1, 1, 1, 1, 2, 2, 3]:
        num.add(x)

    return 11 / 7 == num.mid() and 0.787 == rnd(num.div(), 3)

def test_data():
    data = DATA(options["file"])

    return len(data.rows) == 398 and data.cols.y[0].w == -1 and data.cols.x[0].at == 0 and len(data.cols.x) == 4

def test_clone():
    data1=DATA(options['file'])
    # print("Cloning")
    data2 = data1.clone(data1.rows)
    # print(len(data1.rows) == len(data2.rows) )
    # print(data1.cols.y[1].w == data2.cols.y[1].w)
    # print(data1.cols.x[1].at == data2.cols.x[1].at)
    # print(len(data1.cols.x) == len(data2.cols.x))

    return (len(data1.rows) == len(data2.rows) 
            and data1.cols.y[1].w == data2.cols.y[1].w
            and data1.cols.x[1].at == data2.cols.x[1].at
            and len(data1.cols.x) == len(data2.cols.x) )

def test_around():
    data=DATA(options['file'])
    print(0,0,data.rows[0].cells)
    for n,t in enumerate(data.around(data.rows[1])):
        if n%50==0:
            print(n,rnd(t['dist'],2),t['row'].cells)

def test_half():
    data=DATA(options['file'])
    left,right,A,B,mid,C=data.half()
    print("Left: ",str(len(left)))
    print("Right: ",str(len(right)))
    print("Rows: ",str(len(data.rows)))
    print("A: ",str(A.cells))
    print("C: ",str(C))
    print("mid: ",str(mid.cells))
    print("B: ",str(B.cells))
    
def test_cluster():
    data=DATA(options['file'])
    show(data.cluster(),"mid",data.cols.y,1)

def test_sway():
    data=DATA(options['file'])
    show(data.sway(),"mid",data.cols.y,1)


eg("the", "show settings", disp_setting)
eg("sym", "check syms", test_sym)
eg("num", "check nums", test_num)
eg("data", "read DATA csv", test_data)
eg("clone","duplicate Structure", test_clone)
eg("around","sorting nearest neighbours",test_around)
eg("half","1-level bi-clustering",test_half)
eg("cluster", "N-level bi-clustering", test_cluster)
# eg("optimize", "semi-supervised optimization", test_sway)



main(egs)
