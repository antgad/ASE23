from ROW import ROW
from COLS import COLS
import utils
import math

import json

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
    

    def clone(self, init):
        data = DATA([self.cols.names])
        list(map(lambda x: data.add(x), init if init!=None else []))
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
        for _,col in enumerate(cols or self.cols.x):
            n += 1
            d += math.pow(col.dist(row1.cells[col.at],row2.cells[col.at]),self.config['p'])
        return math.pow((d/n),(1/self.config['p']))
    

    def around(self,row1,rows=None,cols=None):
        rows = rows if rows else self.rows
        cols =  cols if cols else self.cols.x
        def fun(row2):
            return {"row": row2, "dist":self.dist(row1,row2,cols)}
        return sorted(list(map(fun,rows)),key=lambda k: k['dist'])
    
    def furthest(self,row1,rows,cols):
        t=self.around(row1,rows,cols)
        return t[-1]
    

    def half(self,rows=None,cols=None,above=None):
        
        def project(row):
            x,y = utils.cosine(dist(row,A), dist(row,B),c)
            # row.__setattr__('x', x)
            if 'x' not in vars(row).keys() or not row.x:
                row.__setattr__('x', x)
            if 'y' not in vars(row).keys() or not row.y:
                row.__setattr__('y', y)
            row.x = row.x if row.x else x
            row.y = row.y if row.y else y
            return {'row':row, 'x':x, 'y':y}
        def dist(row1,row2):
            return self.dist(row1,row2,cols)
        rows = rows if rows else self.rows
        # some = utils.many(rows,self.config['Sample'])
        A = above or utils.any(rows)
        B = self.furthest(A, rows, None)['row']
        c = dist(A,B)
        left,right=[],[]
        mid=None
        for n,temp in enumerate(sorted(map(project,rows),key = lambda k:k['x'])):
            if n<len(rows)//2:
                left.append(temp["row"])
                mid=temp['row']
            else:
                right.append(temp['row'])
        return left,right,A,B,mid,c


    def cluster(self,rows=None,cols=None,above=None):
        rows= rows if rows else self.rows
        cols=cols if cols else self.cols.x
        node={'data':self.clone(rows)}
        
        if len(rows)>=2:    
            left,right,node['A'],node['B'],node['mid'], node['c'] = self.half(rows,cols,above)
            node['left']= self.cluster(rows=left, cols=cols, above=node['A'])
            node['right']= self.cluster(rows=right, cols=cols, above=node['B'])
        return node
    

    def sway(self,rows=None, min=None, cols=None, above=None):
        rows = rows if rows else self.rows
        min = min if min else len(rows)**self.config['min']
        cols = cols if cols else self.cols.x
        node = {'data':self.clone(rows)}
        if len(rows)>2*min:
            left,right,node['A'],node['B'],node['mid'], _=self.half(rows,cols,above)
            if self.better(node['B'],node['A']):
                left,right,node['A'],node['B'] = right,left,node['B'],node['A']
            node['left']=self.sway(left,min,cols,node["A"])
        return node
            
