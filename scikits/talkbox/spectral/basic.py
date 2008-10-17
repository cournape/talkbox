import numpy as np
from scipy.fftpack import fft, ifft

from scikits.talkbox.linpred import lpc

def periodogram(x, nfft=None, fs=1):
    """Compute the periodogram of the given signal, with the given fft size.

    Parameters
    ----------
    x : array-like
        input signal
    nfft : int
        size of the fft to compute the periodogram. If None (default), the
        length of the signal is used. if nfft > n, the signal is 0 padded.
    fs : float
        Sampling rate. By default, is 1 (normalized frequency. e.g. 0.5 is the
        Nyquist limit).

    Returns
    -------
    pxx : array-like
        The psd estimate.
    fgrid : array-like
        Frequency grid over which the periodogram was estimated.

    Examples
    --------
    Generate a signal with two sinusoids, and compute its periodogram:

    >>> fs = 1000
    >>> x = np.sin(2 * np.pi  * 0.1 * fs * np.linspace(0, 0.5, 0.5*fs))
    >>> x += np.sin(2 * np.pi  * 0.2 * fs * np.linspace(0, 0.5, 0.5*fs))
    >>> px, fx = periodogram(x, 512, fs)

    Notes
    -----
    Only real signals supported for now.

    Returns the one-sided version of the periodogram.

    Discrepency with matlab: matlab compute the psd in unit of power / radian /
    sample, and we compute the psd in unit of power / sample: to get the same
    result as matlab, just multiply the result from talkbox by 2pi"""
    # TODO: this is basic to the point of being useless:
    #   - support Daniel smoothing
    #   - support windowing
    #   - trend/mean handling
    #   - one-sided vs two-sided
    #   - plot
    #   - support complex input
    x = np.atleast_1d(x)
    n = x.size

    if x.ndim > 1:
        raise ValueError("Only rank 1 input supported for now.")
    if not np.isrealobj(x):
        raise ValueError("Only real input supported for now.")
    if not nfft:
        nfft = n
    if nfft < n:
        raise ValueError("nfft < signal size not supported yet")

    pxx = np.abs(fft(x, nfft)) ** 2
    if nfft % 2 == 0:
        pn = nfft / 2 + 1
    else:
        pn = (nfft + 1 )/ 2

    fgrid = np.linspace(0, fs * 0.5, pn)
    return pxx[:pn] / (n * fs), fgrid

def arspec(x, order, nfft=None, fs=1):
    """Compute the spectral density using an AR model.

    An AR model of the signal is estimated through the Yule-Walker equations;
    the estimated AR coefficient are then used to compute the spectrum, which
    can be computed explicitely for AR models.

    Parameters
    ----------
    x : array-like
        input signal
    order : int
        Order of the LPC computation.
    nfft : int
        size of the fft to compute the periodogram. If None (default), the
        length of the signal is used. if nfft > n, the signal is 0 padded.
    fs : float
        Sampling rate. By default, is 1 (normalized frequency. e.g. 0.5 is the
        Nyquist limit).

    Returns
    -------
    pxx : array-like
        The psd estimate.
    fgrid : array-like
        Frequency grid over which the periodogram was estimated.
    """

    x = np.atleast_1d(x)
    n = x.size

    if x.ndim > 1:
        raise ValueError("Only rank 1 input supported for now.")
    if not np.isrealobj(x):
        raise ValueError("Only real input supported for now.")
    if not nfft:
        nfft = n
    if nfft < n:
        raise ValueError("nfft < signal size not supported yet")

    a, e, k = lpc(x, order)

    # This is not enough to deal correctly with even/odd size
    if nfft % 2 == 0:
        pn = nfft / 2 + 1
    else:
        pn = (nfft + 1 )/ 2

    px = 1 / np.fft.fft(a, nfft)[:pn]
    pxx = np.real(np.conj(px) * px)
    pxx /= fs / e
    fx = np.linspace(0, fs * 0.5, pxx.size)
    return pxx, fx

def taper(n, p=0.1):
    """Return a split cosine bell taper (or window)

    Parameters
    ----------
        n: int
            number of samples of the taper
        p: float
            proportion of taper (0 <= p <= 1.)

    Note
    ----
    p represents the proportion of tapered (or "smoothed") data compared to a
    boxcar.
    """
    if p > 1. or p < 0:
        raise ValueError("taper proportion should be betwen 0 and 1 (was %f)"
                         % p)
    w = np.ones(n)
    ntp = np.floor(0.5 * n * p)
    w[:ntp] = 0.5 * (1 - np.cos(np.pi * 2 * np.linspace(0, 0.5, ntp)))
    w[-ntp:] = 0.5 * (1 - np.cos(np.pi * 2 * np.linspace(0.5, 0, ntp)))

    return w
