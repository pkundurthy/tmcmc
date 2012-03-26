import numpy as num

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
