from ROW import ROW
from COLS import COLS
import utils
import math

import json
import random

class DATA:
    """
        Store many rows, summarized into columns
    """
    def __init__(self, src):
        self.rows = []
        self.cols = None
        self.config={}
        with open('config.json') as json_file:
            self.config = json.load(json_file)
        def fun(x): 
            self.add(x)
        if type(src)==str:
            utils.csv(src, fun)
        else:
            list(map(self.add , src if src != None else []))
    
   


    def add(self, t):
        if self.cols:
            t = t if isinstance(t, ROW) else ROW(t)
            self.rows.append(t)
            self.cols.add(t)
        else:
            self.cols = COLS(t)
    

    def clone(self, init={}):
        data = DATA([self.cols.names])
        _ = list(map(lambda x: data.add(x), init if init!=None else []))
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
        for col in ys:
            x = col.norm(row1.cells[col.at])
            y = col.norm(row2.cells[col.at])
            s1 -= math.exp(col.w * (x-y)/len(ys))
            s2 -= math.exp(col.w * (y-x)/len(ys))
        return s1/len(ys)<s2/len(ys)

    def dist(self, row1,row2,cols=None):
        n,d=0,0
        for col in cols or self.cols.x:
            n += 1
            d += math.pow(col.dist(row1.cells[col.at],row2.cells[col.at]),self.config['p'])
        return math.pow((d/n),(1/self.config['p']))

    def around(self,row1,rows=None,cols=None):
        rows = rows if rows else self.rows
        cols =  cols if cols else self.cols.x
        def function(row2):
            return {"row": row2, "dist":self.dist(row1,row2,cols)}
        return sorted(list(map(function,rows or self.rows)),key=lambda k: k['dist'])


    def half(self,rows=None,cols=None,above=None):
        def dist(row1,row2):
            return self.dist(row1,row2,cols)
        
        rows = rows if rows else self.rows
        some = utils.many(rows,self.config['Halves'])

        A = above or utils.any(some)
        B = self.around(A,some)[int(self.config['Far'] * len(rows))//1]['row']
        c = dist(A,B)
        left,right=[],[]

        def project(row):
            x,y = utils.cosine(dist(row,A), dist(row,B),c)
            # row.__setattr__('x', x)
            if 'x' not in vars(row).keys() or not row.x:
                row.__setattr__('x', x)
            if 'y' not in vars(row).keys() or not row.y:
                row.__setattr__('y', y)
            row.x = row.x if row.x else x
            row.y = row.y if row.y else y
            return {'row':row, 'dist': utils.cosine(dist(row,A), dist(row,B), c)}
        
        mid=None
        for n,temp in enumerate(sorted(list(map(project,rows)),key = lambda k:k['dist'])):
            if n<len(rows)//2:
                left.append(temp["row"])
                mid=temp['row']
            else:
                right.append(temp['row'])
        return left,right,A,B,mid,c


    def cluster(self,rows=None,min=None,cols=None,above=None):
        rows= rows if rows else self.rows
        cols=cols if cols else self.cols.x
        min = min or len(rows)**self.config['min']
        node = {'data' : self.clone(rows)}
        
        if len(rows)>=2*min:    
            left,right,node['A'],node['B'],node['mid'], _ = self.half(rows,cols,above)
            node['left']= self.cluster(rows=left, min=min, cols=cols, above=node['A'])
            node['right']= self.cluster(rows=right, min=min, cols=cols, above=node['B'])
        return node
    

    def sway(self,rows=None, min=None, cols=None, above=None):
        data = self
        def worker(rows, worse, above=None):
            if len(rows) <= len(data.rows)**self.config['min']:
                return rows, utils.many(worse, self.config['rest']*len(rows))
            else:
                l,r,A,B,C,D = self.half(rows=rows, cols=None, above=above)
                if self.better(B,A):
                    l,r,A,B = r,l,B,A
                for row in r:
                    worse.append(row)
                return worker(l,worse,A)
        best, rest = worker(data.rows,[])
        return self.clone(best), self.clone(rest)
    
    def tree(self, rows=None , min=None, cols=None, above=None):
        rows = rows if rows else self.rows
        min = min if min else len(rows)**self.config['min']
        cols = cols if cols else self.cols.x
        node = {'data':self.clone(rows)}
        if len(rows)>2*min:

            left, right, node['A'], node['B'], node['mid'], _ =self.half(rows, cols, above)
            node['left'] = self.tree(left, min, cols, node['A'])
            node['right'] = self.tree(right, min, cols, node['B'])
        return node
    