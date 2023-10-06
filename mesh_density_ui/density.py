import numpy as np

# Example density function, returns the value of a 2D gaussian at lat and lon
def get_density(x, y):
    sx = 10
    sy = 10
    mx = 0
    my = 0
    out = 1. / (2. * np.pi * sx * sy) * np.exp(-((y - mx)**2. / (2. * sx**2.) + (x - my)**2. / (2. * sy**2.)))
    return out