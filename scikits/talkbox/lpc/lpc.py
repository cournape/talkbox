#! /usr/bin/env python

# Last Change: Mon Sep 08 10:00 PM 2008 J

import numpy as np
import scipy as sp
import scipy.signal as sig

def lpc_ref(signal, order):
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

    Note
    ----

    This is just for reference, as it is using the direct inversion of the
    toeplitz matrix, which is really slow"""
    if signal.ndim > 1:
        raise ValueError("Array of rank > 1 not supported yet")
    if order > signal.size:
        raise ValueError("Input signal must have a lenght >= lpc order")

    if order > 0:
        p = order + 1
        r = np.zeros(p, signal.dtype)
        # Number of non zero values in autocorrelation one needs for p LPC
        # coefficients
        nx = np.min([p, signal.size])
        x = np.correlate(signal, signal, 'full')
        r[:nx] = x[signal.size-1:signal.size+order]
        phi = np.dot(sp.linalg.inv(sp.linalg.toeplitz(r[:-1])), -r[1:])
        return np.concatenate(([1.], phi))
    else:
        return np.ones(1, dtype = signal.dtype)

def levinson(r, order):
    """Levinson-Durbin recursion, to efficiently solve symmetric linear systems
    with toeplitz structure.

    Arguments
    ---------
        r : array-like
            input array to invert (since the matrix is symmetric Toeplitz, the
            corresponding pxp matrix is defined by p items only). Generally the
            autocorrelation of the signal for linear prediction coefficients
            estimation.

    Note
    ----
    This implementation is in python, hence unsuitable for any serious
    computation. Use it as educational and reference purpose only.

    Levinson is a well-known algorithm to solve the symmetric toeplitz
    equation :

        -R[1] = R[0]   R[1]   ... R[p-1]    a[1]
         :      :      :          :      *  :
        -R[p] = R[p-1] R[p-2] ... R[0]      a[p]

    with respect to a. Using the special symmetry in the matrix, the inversion
    can be done in O(p^2) instead of O(p^3).
    
    Hermitian (complex matrix) is not supported."""
    r = np.atleast_1d(r)
    if r.ndim > 1:
        raise ValueError("Only rank 1 are supported for now.")
    n = r.size
    if order > n - 1:
        raise ValueError("Order should be <= size-1")
    elif n < 1:
        raise ValueError("Cannot operate on empty array !")

    # Estimated coefficients
    a = np.empty(order+1, r.dtype)
    # temporary array
    t = np.empty(order+1, r.dtype)
    # Reflection coefficients
    k = np.empty(order, r.dtype)

    a[0] = 1.
    e = r[0]

    for i in xrange(1, order+1):
        acc = r[i]
        for j in range(1, i):
            acc += a[j] * r[i-j]
        k[i-1] = -acc / e
        a[i] = k[i-1]

        for j in range(order):
            t[j] = a[j]

        for j in range(1, i):
            a[j] += k[i-1] * t[i-j]

        e *= 1 - k[i-1] * k[i-1]

    return a, e, k
