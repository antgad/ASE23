from ROW import ROW
from COLS import COLS
import utils
import math

class DATA:

    def __init__(self, src):
        self.rows = []
        self.cols = None
        def fun(x): self.add(x)
        if type(src)==str:
            utils.csv(src, fun)
        else:
            utils.map(src if src != None else [], fun)
            
    def add(self, t):
        if self.cols:
            t = t if isinstance(t, ROW) else ROW(t)
            self.rows.append(t)
            self.cols.add(t)
        else:
            self.cols = COLS(t)

    def clone(self, init):
        data=DATA({self.cols.names})
        utils.map(self.add, init if init!=None else [])
        return data

    def stats(self, cols, nPlaces, what): 
        def fun(_, col ):
            if what=='div':
                value= col.div()
            else:
                value=col.mid()
            return col.rnd(value,nPlaces), col.txt

        return utils.kap(cols or self.cols.y,fun)
    
    def better(self,row1,row2):
        s1,s2=0,0
        ys=self.cols.y
        for key,col in ys:
            x = col.norm(row1.cells[col.at])
            y = col.norm(row2.cells[col.at])
            s1 -= math.exp(col.w * (x-y)/len(ys))
            s2 -= math.exp(col.w * (y-x)/len(ys))
        return s1/len(ys)<s2/len(ys)
    
    def dist(self, row1,row2,cols):
        n,d=0,0
        for _,col in enumerate(cols or self.cols.x):
            n += 1
            d += math.pow(col.dist(row1.cells[col.at],row2.cells[col.at]),self.saved.p)
        return math.pow((d/n),(1/self.saved.p))
