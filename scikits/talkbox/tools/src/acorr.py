import numpy as np

def acorr(x, axis=-1, maxlag=None, onesided=False):
    if maxlag is None:
        maxlag = x.shape[axis]

    def tmpcorr(x):
        return _acorr1(x, maxlag, onesided)

    return np.apply_along_axis(tmpcorr, axis, x)

def _acorr1(x, maxlag, onesided):
    """Autocorrelation of a rank one array.
    
    Pure python, without vectorization: will be used for reference to the
    cython version"""
    if onesided:
        y = np.zeros(maxlag, x.dtype)
        for i in range(y.size):
            for j in range(x.size - i):
                y[i] += x[j] * x[i+j]
    else:
        y = np.zeros(2 * maxlag - 1, x.dtype)
        for i in range(maxlag):
            for j in range(x.size - i):
                y[i+maxlag-1] += x[j] * x[i+j]
        for i in range(0, maxlag-1):
            y[i] = y[-i-1]

    return y
