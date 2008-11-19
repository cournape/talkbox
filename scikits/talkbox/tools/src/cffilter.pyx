import numpy as np
cimport numpy as c_np
cimport stdlib

def cslfilter(c_np.ndarray b, c_np.ndarray a, c_np.ndarray x):
    """Fast version of slfilter for a set of frames and filter coefficients.
    More precisely, given rank 2 arrays for coefficients and input, this
    computes:

    for i in range(x.shape[0]):
        y[i] = lfilter(b[i], a[i], x[i])

    This is mostly useful for processing on a set of windows with variable
    filters, e.g. to compute LPC residual from a signal chopped into a set of
    windows.

    Parameters
    ----------
        b: array
            recursive coefficients
        a: array
            non-recursive coefficients
        x: array
            signal to filter

    Note
    ----

    This is a specialized function, and does not handle other types than
    double, nor initial conditions."""

    cdef int na, nb, nfr, i, nx
    cdef double *raw_x, *raw_a, *raw_b, *raw_y
    cdef c_np.ndarray[double, ndim=2] tb
    cdef c_np.ndarray[double, ndim=2] ta
    cdef c_np.ndarray[double, ndim=2] tx
    cdef c_np.ndarray[double, ndim=2] ty

    dt = np.common_type(a, b, x)

    if not dt == np.float64:
        raise ValueError("Only float64 supported for now")

    if not x.ndim == 2:
        raise ValueError("Only input of rank 2 support")

    if not b.ndim == 2:
        raise ValueError("Only b of rank 2 support")

    if not a.ndim == 2:
        raise ValueError("Only a of rank 2 support")

    nfr = a.shape[0]
    if not nfr == b.shape[0]:
        raise ValueError("Number of filters should be the same")

    if not nfr == x.shape[0]:
        raise ValueError, \
              "Number of filters and number of frames should be the same"

    tx = np.ascontiguousarray(x, dtype=dt)
    ty = np.ones((x.shape[0], x.shape[1]), dt)

    na = a.shape[1]
    nb = b.shape[1]
    nx = x.shape[1]

    ta = np.ascontiguousarray(np.copy(a), dtype=dt)
    tb = np.ascontiguousarray(np.copy(b), dtype=dt)

    raw_x = <double*>tx.data
    raw_b = <double*>tb.data
    raw_a = <double*>ta.data
    raw_y = <double*>ty.data

    for i in range(nfr):
        filter_double(raw_b, nb, raw_a, na, raw_x, nx, raw_y)
        raw_b += nb
        raw_a += na
        raw_x += nx
        raw_y += nx

    return ty

# a and b are modified in place
cdef int filter_double(double* b, int nb, double* a, int na, double* x, int nx, double* y):

    cdef int i, j, ni, nf
    cdef double gain, acc

    if na > nb:
        nf = na
    else:
        nf = nb

    gain = a[0]
    if gain == 0:
        return -1

    if gain != 1:
        for i in range(na):
            a[i] /= gain
        for i in range(nb):
            b[i] /= gain

    for i in range(nf):
        acc = 0
        acc += x[i] * b[0]
        if nb < i+1:
            ni = nb
        else:
            ni = i+1
        for j in range(1, ni):
            acc += x[i-j] * b[j]

        if na < i+1:
            ni = na
        else:
            ni = i+1
        for j in range(1, ni):
            acc -= y[i-j] * a[j]

        y[i] = acc

    for i in range(nf, nx):
        acc = 0
        acc += x[i] * b[0]
        for j in range(1, nb):
            acc += x[i-j] * b[j]
        for j in range(1, na):
            acc -= y[i-j] * a[j]

        y[i] = acc

    return 0
