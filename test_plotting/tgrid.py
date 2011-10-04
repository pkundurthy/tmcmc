
x = ['a','b','c','d','e']
iplot = 1
Npar = len(x)
for iy in range(Npar):
    for ix in range(Npar):
        if not ix >= iy:
            print x[ix], x[iy], iplot, '(',ix,',',iy,')'
        if iy != 0 and ix != Npar-1:
            iplot += 1 