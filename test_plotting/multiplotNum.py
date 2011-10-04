import numpy as np
import pylab

x = np.arange(10)

for i in range(4):
    pylab.subplot(2,2,i+1)
    pylab.plot(x,x,'b.')
    pylab.text(np.median(x),np.median(x),str(i+1))

pylab.show()

