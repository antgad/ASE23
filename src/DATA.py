from ROW import ROW
from COLS import COLS
import utils
import math

import json

class DATA:

    def __init__(self, src):
        self.rows = []
        self.cols = None
        self.config={}
        with open('config.json') as json_file:
            self.config = json.load(json_file)
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
        data=DATA(list(self.cols.names))
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
            d += math.pow(col.dist(row1.cells[col.at],row2.cells[col.at]),self.config.p)
        return math.pow((d/n),(1/self.config.p))
    
    def around(self,row1,rows,cols):
        rows = rows if rows else self.rows
        cols =  cols if cols else self.cols
        def fun(row2):
            return {"row": row2, "dist":self.dist(row1,row2,cols)}
        return sorted(list(map(fun,rows)),key=lambda k: k['dist'])

    def half(self,rows,cols,above):
        def project(row):
            return {"row": row, "dist": math.cosine(dist(row,A),dist(row,B),C)}
        
        def dist(row1,row2):
            return self.dist(row1,row2,cols)
        rows = rows if rows else self.rows
        some = utils.many(rows,self.config.Sample)
        A = above or utils.any(some)
        B = self.around(A,some)[self.config.Far * len(rows)//1].row
        C = dist(A,B)
        left,right=[],[]
        mid=None
        for n,temp in enumerate(sorted(map(rows,project),key = lambda k:k['dist'])):
            if n<len(rows)//2:
                left.append(temp["row"])
                mid=temp['row']
            else:
                right.append(temp['row'])
        return left,right,A,B,mid,C

    def cluster(self,rows=None,min=None,cols=None,above=None):
        rows= rows if rows else self.rows()

        min=min if min else self.min
        cols=cols if cols else self.cols
        node={'data':self.clone(rows)}
        if len(rows)>2*min:
            left,right,node['A'],node['B'],node.mid=self.half(rows,cols,above)
            node['left']= self.cluster(left,min,cols,node['A'])
            node['right']= self.cluster(right,min,cols,node['B'])
        return node
    
    def sway(self,rows=None, min=None, cols=None, above=None):
        rows= rows if rows else self.rows()

        min=min if min else self.min
        cols=cols if cols else self.cols
        node={'data':self.clone(rows)}
        if len(rows)>2*min:
            left,right,node['A'],node['B'],node.mid=self.half(rows,cols,above)
            if self.better(node.B,node.A):
                left,right,node['A'],node['B'] = right,left,node['B'],node['A']
            node['left']=self.sway(left,min,cols,node["A"])
        return node
            
