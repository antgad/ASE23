from NUM import NUM
from SYM import SYM
import utils

def test_sym():
    sym=SYM()
    for x in ["a","a","a","a","b","b","c"]:
        sym.add(x)
    assert sym.mid=="a" and utils.rand(sym.div())==1.379

def test_num():
    sym=SYM()
    for x in [1,1,1,1,2,2,3]:
        sym.add(x)
    assert sym.mid==11/7 and utils.rnd(sym.div())==0.787 


    