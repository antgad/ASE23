import utils
from DATA import DATA

def repCols(cols):
    cols=utils.copy(cols)
    for i, col in enumerate(cols):
        cols[i] = col[1:-1] + [col[0]+":"+col[-1]]
    cols.insert(0, ["Num"+str(k) for k in range(1,len(cols[0]))])
    cols[0].append("thingX")
    return DATA(cols)

def repPlace(data):
    n,g=20,{}
    for i in range(n):
        g[i]={}
        for j in range(n):
            g[i][j]=' '
    maxy=0
    print()
    for r,row in enumerate(data.rows):
        c=chr(r+65)
        print(c,row.cells[-1])
        x,y = int(row.x*n),int(row.y*n)
        maxy=max(maxy,y)
        g[x][y]=c
        print()
        for y in range(maxy):
            utils.oo(g[y])
    pass

def repgrid(sFile):
    t=utils.dofile(sFile)
    rows=repRows(t,transpose(t['cols']))
    cols=repCols(t['cols'])
    utils.show_grid(rows.cluster())
    utils.show_grid(cols.cluster())
    repPlace(rows)

def repRows(t, rows):
    rows = utils.copy(rows)
    for j, s in enumerate(rows[-1]):
        rows[0][j] = rows[0][j] + ":" + s
    rows.pop(-1) # rows[-1]=None (remove last row)
    for n, row in enumerate(rows):
        # print(n, row)
        # print(f'Fetch {(len(t["rows"]) - n)} out of 0:{len(t["rows"])-1}' )
        if n==0:
            row.append("thingX")
        else:
            u = t['rows'][len(t['rows']) - n ]
            row.append(u[-1])
        # print('Rows:')
        # print(rows)
        # print("Lengths:", [len(i) for i in rows])
    # print(rows)
    return DATA(rows)

def transpose(t):
    u = []
    for i in range(len(t[1])):
        u.append([])
        for j in range(len(t)):
            u[i].append(t[j][i])
    return u

