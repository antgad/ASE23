from ROW import ROW
from COLS import COLS
import utils
import math
import functools
import json
import random
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.cluster import KMeans

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
    
    def subset(self,rows):
        dataSubset = DATA([self.cols.names])
        for row in rows:
            if row != None:
                dataSubset.add(row)
        return dataSubset


    def clone(self, init={}):
        data = DATA([self.cols.names])
        _ = list(map(lambda x: data.add(x), init if init!=None else []))
        return data
    
    # TODO: modify
    def stats(self, cols=None, nPlaces=2, what='mid'): 
        cols = cols if cols else self.cols.y
        def fun(_, col ):
            return col.rnd(getattr(col,what)(),nPlaces), col.txt
        tmp=utils.kap(cols,fun)
        tmp['N']=len(self.rows)
        return tmp
    
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
        if self.config['Type']==0:
            for col in cols or self.cols.x:
               
                n += 1
                d += math.pow(col.dist(row1.cells[col.at],row2.cells[col.at]),self.config['p'])
            return math.pow((d/n),(1/self.config['p']))
        else:
           
            for col in cols or self.cols.x:
                n += 1
                d += col.dist(row1.cells[col.at],row2.cells[col.at])
            return d/(n+d)

    def around(self,row1,rows=None,cols=None):
        rows = rows if rows else self.rows
        cols =  cols if cols else self.cols.x
        def function(row2):
            return {"row": row2, "dist":self.dist(row1,row2,cols)}
        return sorted(list(map(function,rows or self.rows)),key=lambda k: k['dist'])


    def half(self,rows=None,cols=None,above=None,type=0):
        def dist(row1,row2):
            return self.dist(row1,row2,cols)
        
        rows = rows if rows else self.rows
        some = utils.many(rows,self.config['Halves'],self.config['seed'])

        if self.config['Reuse'] and above:
            A=above
        else:
            A=utils.any(some, self.config['seed'])
        temp=self.around(A,some)
        B = temp[int(self.config['Far'] * (len(temp) -1 ))//1]['row']
        c = temp[int(self.config['Far'] * (len(temp) -1 ))//1]['dist']#dist(A,B)
        left,right=[],[]

        def project(row):
            '''x,y = utils.cosine(dist(row,A), dist(row,B),c)
            # row.__setattr__('x', x)
            if 'x' not in vars(row).keys() or not row.x:
                row.__setattr__('x', x)
            if 'y' not in vars(row).keys() or not row.y:
                row.__setattr__('y', y)
            row.x = row.x if row.x else x
            row.y = row.y if row.y else y'''
            return {'row':row, 'dist': utils.cosine(dist(row,A), dist(row,B), c,type=type)}
        
        mid=None
        evals = 0
        
        for n,temp in enumerate(sorted((map(project,rows)),key = lambda k:k['dist'])):
            if n+1 <= len(rows)//2:
                left.append(temp["row"])
                mid=temp['row']
            else:
                right.append(temp['row'])
        if self.config['Reuse'] and above:
            evals = 1
        else: 
            evals = 2
        return left,right,A,B,c,mid, evals

    def cluster(self,rows=None,min=None,cols=None,above=None):
        rows= rows if rows else self.rows
        cols=cols if cols else self.cols.x
        min = min or len(rows)**self.config['min']
        node = {'data' : self.clone(rows)}
        
        if len(rows)>=2*min:    
            left,right,node['A'],node['B'],node['c'],node['mid'], _ = self.half(rows,cols,above)
            node['left']= self.cluster(rows=left, min=min, cols=cols, above=node['A'])
            node['right']= self.cluster(rows=right, min=min, cols=cols, above=node['B'])
        return node
        
    def sway(self,rows=None, min=None, cols=None, above=None,type=0):
        
        data = self
        def worker(rows, worse, evals0=None, above=None):
            if len(rows) <= len(data.rows)**self.config['min']:
                return rows, utils.many(worse, self.config['rest']*len(rows)), evals0
            else:
               
                l,r,A,B,C,D, evals = self.half(rows=rows, cols=None, above=above,type=type)
                
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
                n-=1
                rule[txt] = None
        if n>0:
            return {k:v for k, v in rule.items() if v!=None}
        
    def Rule(self,ranges,max_size):
        t={}
        for r in ranges:
            t[r['txt']] = t.get(r['txt']) or []
            t[r['txt']].append({'lo':r['lo'],'hi':r['hi'],'at':r['at']})
        return self.prune(t,max_size)
    
    def xpln(self,best,rest):
        temp = []
        max_size = {}
        def v(has):
            return utils.value(has,len(best.rows),len(rest.rows),'best')
        def score(ranges):
            rule = self.Rule(ranges,max_size)

            if rule:
               # utils.oo(utils.showRule(rule))
                bestr = utils.selects(rule, best.rows)
                restr = utils.selects(rule, rest.rows)
                if len(bestr) + len(restr) >0:
                    return v({'best':len(bestr), 'rest': len(restr)}) , rule
            return None,None
        for ranges in utils.bins(self.cols.x,{'best':best.rows, 'rest':rest.rows}):
            max_size[ranges[0]['txt']] = len(ranges)
            
            for r in ranges:
                val = v(r['y'].has)
                temp.append({'range': r, 'max': len(ranges), 'val': val})
        rule, most = utils.firstN(sorted(temp,key = lambda k: k['val'], reverse = True), score)        
        return rule, most
    def betters(self,n):
        sorted_rows = list(sorted(self.rows, key=functools.cmp_to_key(self.better)))
        return n and sorted_rows[:n], sorted_rows[n+1:] or sorted_rows
    
    def xpln2(self, best,rest):
        xBest=[]
        yBest=[]
        xRest=[]
        yRest=[]
        xTest=[]

        for row in best.rows:
            xBest.append([row.cells[col.at] for col in best.cols.x])
            yBest.append("BEST")
        for row in rest.rows:
            xRest.append([row.cells[col.at] for col in rest.cols.x])
            yRest.append("REST")
        for row in self.rows:
            xTest.append([row.cells[col.at] for col in self.cols.x])
        xTrain = xBest+xRest
        yTrain = yBest+yRest
        dtc=DecisionTreeClassifier(random_state=self.config['seed'])
        dtc.fit(xTrain,yTrain)
        bestPred=[]
        restPred=[]
        for indx,row in enumerate(xTest):
            if dtc.predict([row]) =="BEST":
                bestPred.append(self.rows[indx])
            else:
                restPred.append(self.rows[indx])
        return bestPred,restPred
    
    def kmean_sway(self,rows=None):
        left=[]
        right=[]
        A=None
        B=None
        def minDist(c,row,A):
            if not A:
                A=row
            if self.dist(A,c)>self.dist(A,row):
                return row
            else:
                return A
        if not rows:
            rows=self.rows
        row_list = np.array([row.cells for row in rows])
        km=KMeans(n_clusters=2,random_state=self.config['seed'],n_init=10)
        km.fit(row_list)
        leftCluster = ROW(km.cluster_centers_[0])
        rightCluster = ROW(km.cluster_centers_[1])
        for key, value in enumerate(km.labels_):
            if value == 0:
                A = minDist(leftCluster, rows[key], A)
                left.append(rows[key])
            else:
                B = minDist(rightCluster, rows[key], B)
                right.append(rows[key])
        return left, right, A, B, 1




    