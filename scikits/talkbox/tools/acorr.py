import numpy as np
from scipy.fftpack import fft

def nextpow2(n):
    """Return the next power of 2 such as 2^p >= n.

    Note
    ----

    Infinite and nan are left untouched, negative values are not allowed."""
    if np.any(n < 0):
        raise ValueError("n should be > 0")
    f, p = np.frexp(n)
    res = f
    bet = np.isfinite(f)
    exa = (f == 0.5)
    res[bet] = p[bet]
    res[exa] = p[exa] - 1
    return res
