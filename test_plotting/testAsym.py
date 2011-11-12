

import pylab
import numpy as num

npoint = 10
x = num.linspace(0,6*num.pi,npoint)
y = num.sin(x)

lowy = num.linspace(0,2,npoint)
uppy = num.linspace(0,3,npoint)

pylab.plot(x,y,'bo')
pylab.errorbar(x,y,yerr=[lowy,uppy],xerr=[uppy,lowy],fmt=None,marker=None)
pylab.show()
