import numpy as np

__all__ = ["demean"]

def demean(x, axis=-1):
    return x - np.mean(x,axis)
