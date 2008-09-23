from scipy.signal import lfilter
from scikits.talkbox.linpred import lpc

def lpcres(signal, order, axis = -1):
    """Compute the LPC residual of a signal.

    The LPC residual is the 'error' signal from LPC analysis, and is defined
    as:

        res[n] = x[n] - xe[n] = 1 + a[1] x[n-1] + ... + a[p] x[n-p]

    Where x is the input signal and xe the linear prediction of x.

    Parameters
    ----------
    signal : array-like
        input signal
    order : int
        LPC order
    axis : int
        axis along which to compute the LPC residual

    Returns
    -------
    res : array-like
        LPC residual

    Note
    ----
    The LPC residual can also be seen as the input of the LPC analysis filter.
    As the LPC filter is a whitening filter, it is a whitened version of the
    signal.

    In AR modelling, the residual is simply the estimated excitation of the AR
    filter.
    """
    return lfilter(lpc(signal, order)[0], 1., signal, axis)
