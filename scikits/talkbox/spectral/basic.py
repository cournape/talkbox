import numpy as np
from scipy.fftpack import fft, ifft

def periodogram(x, nfft=None, fs=1):
    """Compute the periodogram of the given signal, with the given fft size.

    Parameters
    ----------
    x: array-like
        input signal
    nfft: int
        size of the fft to compute the periodogram. By default, the length of
        the signal.

    Notes
    -----
    Only real signals supported for now.

    Returns the one-sided version of the periodogram.

    Discrepency with matlab: matlab compute the psd in unit of power / radian /
    sample, and we compute the psd in unit of power / sample: to get the same
    result as matlab, just multiply the result from talkbox by 2pi"""
    # TODO: this is basic to the point of being useless:
    #   - support windowing
    #   - normalization/frequency unit + definition
    #   - one-sided vs two-sided
    #   - plot
    #   - support complex input
    #   - trend/mean handling
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
