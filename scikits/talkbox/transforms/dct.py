"""Module implementing various DCTs."""

# TODO:
# - make it work along an axis
# - implement dct I, II, III and IV
# - implement mdct
# - 2d version ?

# Would be nice but a lot of work
# - C implementation
import numpy as np
from scipy.fftpack import fft

def dctii(x):
    """Compute a Discrete Cosine Transform, type II.

    The DCT type II is defined as:

        \forall u \in 0...N-1, 
        dct(u) = a(u) sum_{i=0}^{N-1}{f(i)cos((i + 0.5)\pi u}

    Where a(0) = sqrt(1/(4N)), a(u) = sqrt(1/(2N)) for u > 0

    Parameters
    ==========
    x : array-like
        input signal

    Returns
    =======
    y : array-like
        DCT-II

    Note
    ====
    Use fft.
    """
    if not np.isrealobj(x):
        raise ValueError("Complex input not supported")
    n = x.size
    y = np.zeros(n * 4, x.dtype)
    y[1:2*n:2] = x
    y[2*n+1::2] = x[-1::-1]
    y = np.real(fft(y))[:n]
    y[0] *= np.sqrt(.25 / n)
    y[1:] *= np.sqrt(.5 / n)
    return y

if __name__ == "__main__":
    from dct_ref import direct_dctii_2
    a = np.linspace(0, 10, 11)
    print direct_dctii_2(a)
    print dctii(a)
