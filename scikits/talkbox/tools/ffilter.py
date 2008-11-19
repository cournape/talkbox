import numpy as np
from scipy.signal import lfilter

def slfilter(b, a, x):
    """Filter a set of frames and filter coefficients. More precisely, given
    rank 2 arrays for coefficients and input, this computes:

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

    This is a specialized function, and does not handle initial conditions,
    rank > 2 nor  arbitrary axis handling."""

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

    y = np.empty((x.shape[0], x.shape[1]), x.dtype)

    for i in range(nfr):
        y[i] = lfilter(b[i], a[i], x[i])

    return y

