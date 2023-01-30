from main_hw2 import *
egs={}
def eg(key,s,fun):
    egs[key]=fun
    global help
    help+= "  -g  {}\t{}\n".format(key, s)

def disp_setting():
    return str(options)

def test_syms():
    sym=SYM()
    for x in ["a", "a", "a", "a", "b", "b", "c"]:
        sym.add(x) 
    assert "a" == sym.mid() and 1.379 == rnd(sym.div(), 3)
    print('sdf')
    return "a" == sym.mid() and 1.379 == rnd(sym.div(), 3)


eg("sym", "check syms", test_syms)
eg("the", "show settings", disp_setting)
main(egs)
