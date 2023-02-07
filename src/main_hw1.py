from DATA import DATA
from NUM import NUM
import OPTIONS
from SYM import SYM
from utils import *
options=OPTIONS.OPTIONS()
help="""
data.py : an example csv reader script
(c)2023
USAGE:   data.py  [OPTIONS] [-g ACTION]
OPTIONS:
  -d  --dump  on crash, dump stack = false
  -f  --file  name of file         = ../etc/data/auto93.csv
  -g  --go    start-up action      = data
  -h  --help  show help            = false
  -s  --seed  random number seed   = 937162211
ACTIONS:
"""

def main(funs,saved={},fails=0):

    options.cli_setting(help)
    for k,v in options.items():
        saved[k]=v
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


def test_rand():
    num1=NUM.NUM()
    num2=NUM.NUM()
    for i in range(1,10**3):
        num1.add(rand(0,1))

    Seed=937162211
    for i in range(1,10**3):
        num2.add(rand(0,1))
    
    m1=rnd(num1.mid(),10)
    m2=rnd(num2.mid(),10)
    assert abs(m1-m2)/m1<=0.05 and rnd(m1,1)==0.5


eg("num", "check nums", test_num)
eg("sym", "check syms", test_sym)
eg("the", "show settings", disp_setting)
eg("rand","generate, reset, regenerate same", test_rand)
main(egs)