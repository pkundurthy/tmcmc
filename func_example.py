
import numpy as np

def quad(ModelParams,ObservedData):
    """ A quadratic function. Example for tmcmc."""
    
    x = np.array(ObservedData['all']['x'])
    
    y = ModelParams['a0']['value'] + ModelParams['a1']['value']*x +\
        ModelParams['a2']['value']*(x**2)
    
    ModelData = {}
    ModelData['all'] = {'y':y}
    return ModelData