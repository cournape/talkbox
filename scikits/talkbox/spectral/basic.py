import numpy as np
from scipy.fftpack import fft, ifft

def periodogram(x, nfft=256):
    """Compute the periodogram of the given signal, with the given fft size.

    Parameters
    ---------
    x: array-like
        input signal
    nfft: int
        size of the fft to compute the periodogram

    Notes
    ----
    Only real signals supported for now.

    Returns the one-sided version of the periodogram.

    Discrepency with matlab: matlab compute the psd in unit of power / radian /
    sample, and we compute the psd in unit of power / sample: to get the same
    result as matlab, just multiply the result from talkbox by 2pi"""
    x = np.atleast_1d(x)
    n = x.size

    if x.ndim > 1:
        raise ValueError("Only rank 1 input supported for now.")
    if not np.isrealobj(x):
        raise ValueError("Only real input supported for now.")
    if nfft < size:
        raise ValueError("nfft < signal size not supported yet")

    pxx = np.abs(fft(x, nfft)) ** 2
    if nfft % 2 == 0:
        pn = nfft / 2 + 1
    else:
        pn = (nfft + 1 )/ 2

    return pxx[:pn] / x.size
