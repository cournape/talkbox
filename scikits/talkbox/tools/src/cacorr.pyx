import numpy as np
cimport numpy as c_np
cimport stdlib

def acorr(c_np.ndarray x, maxlag=None, onesided=False, axis=-1):
    """Cython version of autocorrelation, direct implementation. This can be
    faster than FFT for small size or for maxlag << x.shape[axis]."""
    cdef double *raw_x, *raw_y
    cdef int raw_maxlag, nfr, raw_onesided, nx, ny
    cdef c_np.ndarray[double, ndim=2] tx
    cdef c_np.ndarray[double, ndim=2] ty

    if not x.dtype == np.float64:
        raise ValueError("Only float64 supported for now")

    if not x.ndim == 2:
        raise ValueError("Rank != 2 not supported yet")

    axis = axis % x.ndim
    if not axis == 1:
        raise ValueError("Axis != 1 not supported yet")

    tx = np.ascontiguousarray(x)

    if maxlag is None:
        raw_maxlag = x.shape[axis] - 1
    else:
        raw_maxlag = maxlag

    nfr = tx.shape[0]
    nx = tx.shape[axis]
    if onesided:
        ny = raw_maxlag+1
        ty = np.zeros((nfr, ny), x.dtype)
        raw_onesided = 1
    else:
        ny = 2*raw_maxlag+1
        ty = np.zeros((nfr, ny), x.dtype)
        raw_onesided = 0

    raw_x = <double*>tx.data
    raw_y = <double*>ty.data

    for i in range(nfr):
        acorr_double(raw_x, nx, raw_maxlag, raw_onesided, raw_y)
        raw_x += nx
        raw_y += ny

    return ty

# y values are assumed to be set to 0
cdef int acorr_double(double* x, int nx, int maxlag, int onesided, double* y):
    cdef int i, j, ni, nf
    cdef double gain, acc

    if onesided:
        for i in range(maxlag+1):
            for j in range(nx-i):
                y[i] += x[j] * x[i+j]
    else:
        for i in range(maxlag+1):
            for j in range(nx-i):
                y[i+maxlag] += x[j] * x[i+j]
        for i in range(maxlag):
            y[i] = y[2*maxlag-i]

    return 0
