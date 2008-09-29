"""Module implementing various DCTs."""

# TODO:
# - make it work along an axis
# - implement dct I, II, III and IV
# - implement mdct
# - 2d version ?

# Would be nice but a lot of work
# - C implementation
import numpy as np

# Definition of DCT in 1d (II type)
# dct(u) = a(u) \sum_{i=0}^{N-1}{f(x)cos(\pi(x + 0.5)u}

def direct_dctii(x):
    """Direct implementation (O(n^2)) of dct II.

    Notes
    -----

    Use it as a reference only, it is not suitable for any real computation."""
    n = x.size
    a = np.empty((n, n), dtype = x.dtype)
    for i in xrange(n):
        for j in xrange(n):
            a[i, j] = x[j] * np.cos(np.pi * (0.5 + j) * i / n)

    a[0] *= np.sqrt(1. / n)
    a[1:] *= np.sqrt(2. / n)

    return a.sum(axis = 1)

def direct_dctii_2(x):
    """Direct implementation (O(n^2)) of dct."""
    # We are a bit smarter here by computing the coefficient matrix directly,
    # but still O(N^2)
    n = x.size

    a = np.cos(np.pi / n * np.linspace(0, n - 1, n)[:, None]
                         * np.linspace(0.5, 0.5 + n - 1, n)[None, :])
    a *= x
    a[0] *= np.sqrt(1. / n)
    a[1:] *= np.sqrt(2. / n)

    return a.sum(axis = 1)

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
    n = x.size
    y = np.zeros(n * 4, x.dtype)
    y[1:2*n:2] = x
    y[2*n+1::2] = x[-1::-1]
    y = np.real(np.fft.fft(y))[:n]
    y[0] *= np.sqrt(.25 / n)
    y[1:] *= np.sqrt(.5 / n)
    return y

if __name__ == "__main__":
    a = np.linspace(0, 10, 11)
    print direct_dctii_2(a)
    a = np.linspace(0, 10, 11)
    print direct_dctii_2(a)
    b = dctii(a)
    print b
