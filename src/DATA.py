from ROW import ROW
from COLS import COLS
import utils

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
            t = t if t.cells else ROW(t)
            self.rows.append(t)
            self.cols.add(t)
        else:
            self.cols = COLS(t)

    def clone(self, init):
        data=DATA({self.cols.names})
        utils.map(self.add, init if init!=None else [])
        return data

    def stats(self, cols, nPlaces, what='mid'): #--> t; reports mid or div of cols (defaults to i.cols.y)
        # TODO
        # def fun(k,col): return col.rnd(getmetatable(col)[what if what else "mid"](col),nPlaces), col.txt
        # 
        # return utils.kap(cols or self.cols.y, fun)
        return dict(sorted({ col.txt: col.rnd(getattr(col,what)(),nPlaces) for col in cols or self.cols.y }.items()))