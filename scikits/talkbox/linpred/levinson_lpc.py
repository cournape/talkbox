#! /usr/bin/env python

# Last Change: Wed Sep 24 06:00 PM 2008 J

import numpy as np
from scipy.fftpack import fft, ifft

from scikits.talkbox.tools import nextpow2

from scikits.talkbox.linpred._lpc import levinson as c_levinson

__all__ = ['levinson', 'lpc']

def lpc(signal, order, axis=-1):
    """Compute the Linear Prediction Coefficients.

    Return the order + 1 LPC coefficients for the signal. c = lpc(x, k) will
    find the k+1 coefficients of a k order linear filter:

      xp[n] = -c[1] * x[n-2] - ... - c[k-1] * x[n-k-1]

    Such as the sum of the squared-error e[i] = xp[i] - x[i] is minimized.

    Parameters
    ----------
    signal: array_like
        input signal
    order : int
        LPC order (the output will have order + 1 items)

    Returns
    -------
    a : array-like
        the solution of the inversion.
    e : array-like
        the prediction error.
    k : array-like
        reflection coefficients.

    Notes
    -----
    This uses Levinson-Durbin recursion for the autocorrelation matrix
    inversion, and fft for the autocorrelation computation.

    For small order, particularly if order << signal size, direct computation
    of the autocorrelation is faster: use levinson and correlate in this case."""
    n = signal.shape[axis]
    if order > n:
        raise ValueError("Input signal must have length >= order")

    r = acorr_lpc(signal, axis)
    return levinson(r, order, axis)

def _acorr_last_axis(x, nfft, maxlag):
    a = np.real(ifft(np.abs(fft(x, n=nfft) ** 2)))
    return a[..., :maxlag+1] / x.shape[-1]

def acorr_lpc(x, axis=-1):
    """Compute autocorrelation of x along the given axis.

    This compute the biased autocorrelation estimator (divided by the size of
    input signal)

    Notes
    -----
        The reason why we do not use acorr directly is for speed issue."""
    if not np.isrealobj(x):
        raise ValueError("Complex input not supported yet")

    maxlag = x.shape[axis]
    nfft = 2 ** nextpow2(2 * maxlag - 1)

    if axis != -1:
        x = np.swapaxes(x, -1, axis)
    a = _acorr_last_axis(x, nfft, maxlag)
    if axis != -1:
        a = np.swapaxes(a, -1, axis)
    return a

def levinson(r, order, axis = -1):
    """Levinson-Durbin recursion, to efficiently solve symmetric linear systems
    with toeplitz structure.

    Parameters
    ----------
    r : array-like
        input array to invert (since the matrix is symmetric Toeplitz, the
        corresponding pxp matrix is defined by p items only). Generally the
        autocorrelation of the signal for linear prediction coefficients
        estimation. The first item must be a non zero real, and corresponds
        to the autocorelation at lag 0 for linear prediction.
    order : int
        order of the recursion. For order p, you will get p+1 coefficients.
    axis : int, optional
        axis over which the algorithm is applied. -1 by default.

    Returns
    -------
    a : array-like
        the solution of the inversion (see notes).
    e : array-like
        the prediction error.
    k : array-like
        reflection coefficients.

    Notes
    -----
    Levinson is a well-known algorithm to solve the Hermitian toeplitz
    equation: ::

                       _          _
        -R[1] = R[0]   R[1]   ... R[p-1]    a[1]
         :      :      :          :         :
         :      :      :          _      *  :
        -R[p] = R[p-1] R[p-2] ... R[0]      a[p]

    with respect to a. Using the special symmetry in the matrix, the inversion
    can be done in O(p^2) instead of O(p^3).

    Only double argument are supported: float and long double are internally
    converted to double, and complex input are not supported at all.
    """
    if axis != -1:
        r = np.swapaxes(r, axis, -1)
    a, e, k = c_levinson(r, order)
    if axis != -1:
        a = np.swapaxes(a, axis, -1)
        e = np.swapaxes(e, axis, -1)
        k = np.swapaxes(k, axis, -1)
    return a, e, k
