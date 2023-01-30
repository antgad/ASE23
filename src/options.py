import re
import sys
from utils import coerce

class options:
    
    def __init__(self):
        self.t={}
    
    def cli_setting(self,help):
        s=re.findall("\n[\s]+[-][\S]+[\s]+[-][-]([\S]+)[^\n]+= ([\S]+)", help)
        for k,v in s:
            self.t[k] = coerce(v)
        for k,v in self.t.items():
            v=str(v)
            for n,x in enumerate(sys.argv):
                if x=='-'+k[0] or x=='--'+k:
                    v=(sys.argv[n+1] if n+1<len(sys.argv) else False) or v=='Flase' and 'true' or v=='True' and 'flase'
                self.t[k]=coerce(v)
    def items(self):
        return self.t.items()
    
    def __getitem__(self, key):
        return self.t[key]

    def __setitem__(self, key, value):
        self.t[key] = value