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


def test_csv():
    n = 0

    def f(t):
        nonlocal n
        n += len(t)

    csv(options['file'], f)
    return n == 8 * 399


def test_data():
    data = DATA(options["file"])

    return len(data.rows) == 398 and data.cols.y[0].w == -1 and data.cols.x[0].at == 0 and len(data.cols.x) == 4


def test_stats():
    data = DATA(options["file"])

    for k, cols in {"y": data.cols.y, "x": data.cols.x}.items():
        print(k, "\tmid\t", data.stats(cols, 2, what="mid"))
        print("", "\tdiv\t", data.stats(cols, 2, what="div"))

eg("csv", "read from csv", test_csv)
eg("data", "read DATA csv", test_data)
eg("num", "check nums", test_num)
eg("stats", "stats from DATA", test_stats)
eg("sym", "check syms", test_sym)
eg("the", "show settings", disp_setting)

main(egs)
