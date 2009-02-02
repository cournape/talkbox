import numpy as np
from scipy.fftpack import fft, ifft

__all__ = ['nextpow2', 'acorr']

def nextpow2(n):
    """Return the next power of 2 such as 2^p >= n.

    Notes
    -----

    Infinite and nan are left untouched, negative values are not allowed."""
    if np.any(n < 0):
        raise ValueError("n should be > 0")

    if np.isscalar(n):
        f, p = np.frexp(n)
        if f == 0.5:
            return p-1
        elif np.isfinite(f):
            return p
        else:
            return f
    else:
        f, p = np.frexp(n)
        res = f
        bet = np.isfinite(f)
        exa = (f == 0.5)
        res[bet] = p[bet]
        res[exa] = p[exa] - 1
        return res

def _acorr_last_axis(x, nfft, maxlag, onesided=False, scale='none'):
    a = np.real(ifft(np.abs(fft(x, n=nfft) ** 2)))
    if onesided:
        b = a[..., :maxlag]
    else:
        b = np.concatenate([a[..., nfft-maxlag+1:nfft],
                            a[..., :maxlag]], axis=-1)
    #print b, a[..., 0][..., np.newaxis], b / a[..., 0][..., np.newaxis]
    if scale == 'coeff':
        return b / a[..., 0][..., np.newaxis]
    else:
        return b

def acorr(x, axis=-1, onesided=False, scale='none'):
    """Compute autocorrelation of x along given axis.

    Parameters
    ----------
        x : array-like
            signal to correlate.
        axis : int
            axis along which autocorrelation is computed.
        onesided: bool, optional
            if True, only returns the right side of the autocorrelation.
        scale: {'none', 'coeff'}
            scaling mode. If 'coeff', the correlation is normalized such as the
            0-lag is equal to 1.

    Notes
    -----
        Use fft for computation: is more efficient than direct computation for
        relatively large n.
    """
    if not np.isrealobj(x):
        raise ValueError("Complex input not supported yet")
    if not scale in ['none', 'coeff']:
        raise ValueError("scale mode %s not understood" % scale)

    maxlag = x.shape[axis]
    nfft = 2 ** nextpow2(2 * maxlag - 1)

    if axis != -1:
        x = np.swapaxes(x, -1, axis)
    a = _acorr_last_axis(x, nfft, maxlag, onesided, scale)
    if axis != -1:
        a = np.swapaxes(a, -1, axis)
    return a
