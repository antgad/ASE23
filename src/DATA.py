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
    
    # TODO: modify
    def stats(self, cols, nPlaces, what): 
        cols = cols if cols else self.cols.y
        def fun(_, col ):
            return col.rnd(getattr(cols,what)(),nPlaces), col.txt
        return utils.kap(cols,fun)
    

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
        return sorted(list(map(function,rows)),key=lambda k: k['dist'])


    def half(self,rows=None,cols=None,above=None):
        def dist(row1,row2):
            return self.dist(row1,row2,cols)
        
        rows = rows if rows else self.rows
        some = utils.many(rows,self.config['Halves'],self.config['seed'])

        if self.config['Reuse']:
            A=above
        if not above or not self.config['Reuse']:
            A=utils.any(some, self.config['seed'])
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
        evals = 0
        for n,temp in enumerate(sorted(list(map(project,rows)),key = lambda k:k['dist'])):
            if n<=len(rows)//2:
                left.append(temp["row"])
                mid=temp['row']
            else:
                right.append(temp['row'])
        if self.config['Reuse'] and above:
            evals = 1
        else: 
            evals = 2
        return left,right,A,B,mid,c, evals


    '''def cluster(self,rows=None,min=None,cols=None,above=None):
        rows= rows if rows else self.rows
        cols=cols if cols else self.cols.x
        min = min or len(rows)**self.config['min']
        node = {'data' : self.clone(rows)}
        
        if len(rows)>=2*min:    
            left,right,node['A'],node['B'],node['mid'], _ = self.half(rows,cols,above)
            node['left']= self.cluster(rows=left, min=min, cols=cols, above=node['A'])
            node['right']= self.cluster(rows=right, min=min, cols=cols, above=node['B'])
        return node'''
    
    
    def sway(self,rows=None, min=None, cols=None, above=None):
        data = self
        def worker(rows, worse, evals0, above=None):
            if len(rows) <= len(data.rows)**self.config['min']:
                return rows, utils.many(worse, self.config['rest']*len(rows)), evals0
            else:
                l,r,A,B,C,D, evals = self.half(rows=rows, cols=None, above=above)
                if self.better(B,A):
                    l,r,A,B = r,l,B,A
                for row in r:
                    worse.append(row)
                return worker(l,worse,evals+evals0,A)
        best, rest, evals = worker(data.rows,[],0)
        return self.clone(best), self.clone(rest), evals
    
    def tree(self, rows=None , min=None, cols=None, above=None):
        rows = rows if rows else self.rows
        min = min if min else len(rows)**self.config['min']
        cols = cols if cols else self.cols.x
        node = {'data':self.clone(rows)}
        if len(rows)>2*min:

            left, right, node['A'], node['B'], node['mid'], _,_ =self.half(rows, cols, above)
            node['left'] = self.tree(left, min, cols, node['A'])
            node['right'] = self.tree(right, min, cols, node['B'])
        return node
    

    def prune(self,rule,max_size):
        n=0
        for txt,r in rule.items():
            n+=1
            if len(r) == max_size[txt]:
                n+=1
                rule[txt] = None
        if n>0:
            return rule
        
    def Rule(self,ranges, max_size):
        t={}
        for r in ranges:
            if r.txt not in t:
                t[r.txt]=[]
            t[r.txt].append({'lo':r.lo,'hi':r.hi,'at':r.at})
        return self.prune(t,max_size)
        
    def xpln(self,best,rest):
        temp = []
        max_size = {}
        def v(has):
            return utils.value(has,len(best.rows),len(rest.rows),'best')
        def score(ranges):
            rule = self.Rule(ranges,max_size)
            if rule:
                print(utils.showRule(rule))

    