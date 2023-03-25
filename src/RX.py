class RX:
    
    def __init__(self, t=[], s=""):
        t.sort()
        self.name = s
        self.rank = 0
        self.n = len(t)
        self.show = ""
        self.has = t

    def mid(self, t=None):
        t = t or self.has
        n = len(t)//2
        return len(t)%2==0 and (t[n] +t[n+1])/2 or t[n+1]
    
    def div(self, t=None):
        t = t or self.has
        return (t[ len(t)*9//10 ] - t[ len(t)*1//10 ])/2.56

    def merge(self, rx2):
        rx1 = self
        rx3 = RX([], rx1.name)
        rx3.has = rx1.has + rx2.has
        rx3.has.sort()
        rx3.n = len(rx3.has)
        return rx3
