import utils
from DATA import DATA

def repCols(cols):
    cols=utils.copy(cols)
    for i, col in enumerate(cols):
        cols[i] = col[1:-1] + [col[0]+":"+col[-1]]
    cols.insert(0, ["Num"+str(k) for k in range(1,len(cols[0]))])
    cols[0].append("thingX")
    return DATA(cols)
