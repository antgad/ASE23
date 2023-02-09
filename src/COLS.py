import re

from NUM import NUM
from SYM import SYM
from ROW import ROW

class COLS:
    """
        Factory for managing a set of NUMs or SYMs
    """
    def __init__(self,t):
        self.names = t
        self.all = []
        self.x = []
        self.y = []
        self.klass = None    

        for n, s in enumerate(t):
            col =  NUM(n, s) if re.search("^[A-Z]+",s) else SYM(n, s)
            self.all.append(col)

            if not re.findall(r"X$", s):
                if re.findall(r"!$", s):
                    self.klass = col
                if re.findall(r"[!+-]$", s):
                    self.y.append(col)
                else:
                    self.x.append(col)

    def add(self, row):
        for _, t in enumerate([self.x, self.y]):
            for _, col in enumerate(t):
                col.add(row.cells[col.at])
                
