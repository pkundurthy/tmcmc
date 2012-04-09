import numpy as num
import scipy.integrate

def String2Bool(inStr):
    """ Returns String representations to Boolean type. """
    
    return inStr.lower() in ['yes','true','t','1']

def String2IntFloat(inStr):
    """ Convert string to either int or float. """
    
    try:
        ret = int(inStr)
    except ValueError:
        ret = float(inStr)
    return ret

def format(str, form):
    if form == 'n':
        form ='d'
    return eval(' \'%s%s\' %s (%s)' % ('%', form, '%', str))

def quickMean(itr):
    
    return num.sum(itr)/len(itr)

def linefitquick_werr(x,y,yerr):
    """
    fit line of the form
    y = a + b x
    given 
    """
    x = num.array(x)
    y = num.array(y)
    yerr = num.array(yerr)
    
    wsum = num.sum(1e0/(yerr**2))
    wsumx = num.sum(x/(yerr**2))
    wsumy = num.sum(y/(yerr**2))
    wsumxy = num.sum((x*y)/(yerr**2))
    wsumx2 = num.sum((x**2)/(yerr**2))
    
    delta = wsum*wsumx2 - wsumx**2
    a = (1e0/delta)*(wsumx2*wsumy - wsumx*wsumxy)
    b = (1e0/delta)*(wsum*wsumxy - wsumx*wsumy)
    
    siga = num.sqrt((1e0/delta)*(wsumx2))
    sigb = num.sqrt((1e0/delta)*(wsum))

    return (b,sigb),(a,siga)

#def normal_func(x,mu,sig):
    """                 """
    #return (1e0/(sig*num.sqrt(2e0*num.pi)))*num.exp( (-1e0*(x-mu)**2)/(2e0*(sig**2)))

def min_2normals(m1,s1,m2,s2):
    """             """
    
    
    #m1,s1,m2,s2 = 5.871741,0.037418,5.869499,0.038057
    A1 = 1e0/(s1*num.sqrt(2e0*num.pi))
    pTerm1 = -1e0/(2e0*s1*s1)
    A2 = 1e0/(s2*num.sqrt(2e0*num.pi))
    pTerm2 = -1e0/(2e0*s2*s2)
    #print m1, m2, s1, s2
    #print m1, m2

    def func(t):
        #print m1, m2
        f1 = num.abs(A1*num.exp(pTerm1*(t-m1)*(t-m1)))
        f2 = num.abs(A2*num.exp(pTerm2*(t-m2)*(t-m2)))
        #print t,min1, min2
        return min([f1,f2])

    return func

def ovl_coefficient(mu1,sig1,mu2,sig2):

    
    Int1 = \
    scipy.integrate.quad(min_2normals(mu1,sig1,mu2,sig2),-num.inf,min([mu1,mu2]))
    Int2 = \
    scipy.integrate.quad(min_2normals(mu1,sig1,mu2,sig2),min([mu1,mu2]),max([mu1,mu2]))
    #print Int1[0], Int2[0]
    Int3 = \
    scipy.integrate.quad(min_2normals(mu1,sig1,mu2,sig2),max([mu1,mu2]),num.inf)
    
    return Int1[0]+Int2[0]+Int3[0]