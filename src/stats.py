import json
import random
import math
from RX import RX
from NUM import NUM


config = {}
def load_configs():
    global config
    with open('config.json') as json_file:
        config = json.load(json_file)


def erf(x):
    # -- from Abramowitz and Stegun 7.1.26 
    # -- https://s3.amazonaws.com/nrbook.com/AandS-a4-v1-2.pdf
    # -- (easier to read at https://en.wikipedia.org/wiki/Error_function#Approximation_with_elementary_functions)
    a1 =  0.254829592
    a2 = -0.284496736
    a3 =  1.421413741
    a4 = -1.453152027
    a5 =  1.061405429
    p  =  0.3275911
    # -- Save the sign of x
    sign = 1
    if x < 0:
        sign = -1
    x = abs(x)
    # -- A&S formula 7.1.26
    t = 1.0/(1.0 + p*x)
    y = 1.0 - (((((a5*t + a4)*t) + a3)*t + a2)*t + a1)*t*math.exp(-x*x)
    return sign*y


def gaussian(mu=0,sd=1):
    return mu + sd * math.sqrt(-2*math.log(random.random())) * math.cos(2*math.pi*random.random())


def samples(t, n=None):
    u = []
    n = n or len(t)
    for i in range(n):
        u.append(t[random.randint(0, n-1)])
    return u


def cliffsDelta(ns1,ns2) -> bool: #; true if different by a trivial amount
    n,gt,lt = 0,0,0
    if len(ns1)> 128: ns1 = samples(ns1,128)
    if len(ns2)> 128: ns2 = samples(ns2,128)
    for x in ns1:
        for y in ns2:
            n = n + 1
            if x > y: gt += 1
            if x < y: lt += 1
    return abs(lt - gt)/n <= config['cliff']


def delta(i:NUM, other:NUM):
    e, y, z= 1e-32, i, other
    return abs(y.mu - z.mu) / ((e + y.sd**2/y.n + z.sd**2/z.n)**.5)


def bootstrap(y0, z0):
    # local n, x,y,z,xmu,ymu,zmu,yhat,zhat,tobs
    x, y, z, yhat, zhat = NUM(), NUM(), NUM(), [], []
    # -- x will hold all of y0,z0
    # -- y contains just y0
    # -- z contains just z0
    for y1 in y0: 
        x.add(y1)
        y.add(y1)
    for z1 in z0: 
        x.add(z1)
        z.add(z1)
    xmu, ymu, zmu = x.mu, y.mu, z.mu
    # -- yhat and zhat are y,z fiddled to have the same mean
    for y1 in y0:
        yhat.append(y1 - ymu + xmu)
    for z1 in z0:
        zhat.append(z1 - zmu + xmu)
    # -- tobs is some difference seen in the whole space
    tobs = delta(y,z)
    n = 0
    
    for _ in range(config['bootstrap']):
        # -- here we look at some delta from just part of the space
        # -- it the part delta is bigger than the whole, then increment n
        if delta(NUM(t=samples(yhat)), NUM(t=samples(zhat))) > tobs:
            n = n + 1
    # -- if we have seen enough n, then we are the same
    # -- On Tuesdays and Thursdays I lie awake at night convinced this should be "<"
    # -- and the above "> obs" should be "abs(delta - tobs) > someCriticalValue". 
    return n / config['bootstrap'] >= config['conf']


def scottKnot(rxs):
    
    def merges(i,j):
        out = RX([],rxs[i].name)
        for k in range(i,j+1):
            out = out.merge(rxs[k]) # Doubt:should this be k? 
        return out 
    
    def same(lo,cut,hi):
        l= merges(lo,cut)
        r= merges(cut+1,hi)
        return cliffsDelta(l.has, r.has) and bootstrap(l.has, r.has) 
    
    def recurse(lo,hi,rank):
        cut,best,l,l1,r,r1,now,b4 = None, None, None, None, None, None, None, None
        # cut = None
        b4 = merges(lo,hi)
        best = 0
        for j in range(lo,hi):
            l   = merges(lo,  j)
            r   = merges(j+1, hi)
            now = (l.n*(l.mid() - b4.mid())**2 + r.n*(r.mid() - b4.mid())**2) / (l.n + r.n)
            if now > best:
                if abs(l.mid() - r.mid()) >= cohen:
                    cut, best = j, now
        
        if cut and not same(lo,cut,hi):
            rank = recurse(lo, cut, rank) + 1
            rank = recurse(cut+1, hi,  rank) 
        else:
            for i in range(lo,hi+1):
                rxs[i].rank = rank
        return rank
    
    rxs.sort(key=lambda x: x.mid())
    cohen = merges(0,len(rxs)-1).div() * config['cohen']
    recurse(0, len(rxs)-1, 1)
    
    return rxs


def tiles(rxs):
    lo, hi = math.inf, -math.inf
    for rx in rxs: 
        lo,hi = min(lo,rx.has[1]), max(hi, rx.has[-1]) 
    for rx in rxs:
        t, u = rx.has, []
        def of(x,most): 
            return int(max(1, min(most, x)))
        def at(x):
            return t[of(len(t)*x//1, len(t))-1]
        def pos(x):
            return math.floor(of(config['width']*(x-lo)/(hi-lo+1E-32)//1, config['width']))
        for i in range(config['width']+1):
            u.append(" ")
        a,b,c,d,e= at(.1), at(.3), at(.5), at(.7), at(.9) 
        A,B,C,D,E= pos(a), pos(b), pos(c), pos(d), pos(e)
        for i in range(A,B+1):
            u[i] = "-"
        for i in range(D,E+1):
            u[i] = "-"
        u[config['width']//2] = "|" 
        u[C] = "*"
        rx.show = "".join(u) + " {" + str(config['Fmt'])%(a)
        for x in [b,c,d,e]:
            rx.show = rx.show + ", " + str(config['Fmt']) % x 
        rx.show = rx.show + "}"
    
    return rxs
        

