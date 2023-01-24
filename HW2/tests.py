from NUM import NUM
from SYM import SYM
import utils

def test_sym():
    sym=SYM()
    for x in ["a","a","a","a","b","b","c"]:
        sym.add(x)
    assert sym.mid=="a" and utils.rand(sym.div())==1.379

def test_num():
    num=NUM()
    for x in [1,1,1,1,2,2,3]:
        num.add(x)
    assert num.mid==11/7 and utils.rnd(num.div())==0.787 
def test_rand():
    num1=NUM()
    num2=NUM()
    for i in range(1,10^3):
        num1.add(utils.rand(0,1))
    for i in range(1,10^3):
        num2.add(utils.rand(0,1))
    m1=utils.rnd(num1.mid(),10)
    m2=utils.rnd(num2.mid(),10)
    assert m1==m2 and utils.rnd(m1,1)==0.5


