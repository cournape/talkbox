import numpy as np

from scipy.signal import lfilter

#from scikits.talkbox.linpred import lpc
from scikits.talkbox.linpred.levinson_lpc import levinson, lpc
from scikits.talkbox.tools import slfilter
from scikits.talkbox.tools.cacorr import acorr

__all__ = ["lpcres"]

def lpcres(signal, order, usefft=True):
    """Compute the LPC residual of a signal.

    The LPC residual is the 'error' signal from LPC analysis, and is defined
    as:

        res[n] = x[n] - xe[n] = 1 + a[1] x[n-1] + ... + a[p] x[n-p]

    Where x is the input signal and xe the linear prediction of x.

    Parameters
    ----------
    signal : array-like
        input signal. If rank of signal is 2, each row is assumed to be an
        independant signal on which the LPC is computed. Rank > 2 is not
        supported.
    order : int
        LPC order

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
    if signal.ndim == 1:
        return lfilter(lpc(signal, order)[0], 1., signal)
    elif signal.ndim == 2:
        if usefft:
            cf = lpc(signal, order, axis=-1)[0]
        else:
            c = acorr(signal, maxlag=order, onesided=True)/signal.shape[-1]
            cf = levinson(c, order, axis=-1)[0]
        return slfilter(cf, np.ones((cf.shape[0], 1)), signal)
    else:
        raise ValueError("Input of rank > 2 not supported yet")
