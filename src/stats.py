import random

# def NUM(t=[]):
#     i= {'n':0,'mu':0,'m2':0,'sd':0}
#     for _,x in enumerate(t): 
#         add(i,x) 
#     return i end

def samples(t, n=None):
    u = []
    n = n or len(t)
    for i in range(n):
        u.append(t[random.randint(0, n-1)])
    return u
