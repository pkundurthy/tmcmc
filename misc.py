


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
