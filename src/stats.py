import json
import random
import math

from NUM import NUM
# def NUM(t=[]):
#     i= {'n':0,'mu':0,'m2':0,'sd':0}
#     for _,x in enumerate(t): 
#         add(i,x) 
#     return i end

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
    with open('config.json') as json_file:
        config = json.load(json_file)
    return abs(lt - gt)/n <= config['cliff']

def delta(i:NUM, other:NUM):
    e, y, z= 1E-32, i, other
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
    with open('config.json') as json_file:
        config = json.load(json_file)
    for _ in range(config['bootstrap']):
        # -- here we look at some delta from just part of the space
        # -- it the part delta is bigger than the whole, then increment n
        if delta(NUM(t=samples(yhat)), NUM(t=samples(zhat))) > tobs:
            n = n + 1
    # -- if we have seen enough n, then we are the same
    # -- On Tuesdays and Thursdays I lie awake at night convinced this should be "<"
    # -- and the above "> obs" should be "abs(delta - tobs) > someCriticalValue". 
    return n / config['bootstrap'] >= config['conf']