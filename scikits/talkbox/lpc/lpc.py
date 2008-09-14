#! /usr/bin/env python

# Last Change: Sun Sep 14 06:00 PM 2008 J

import numpy as np

from _lpc import levinson as c_levinson

def levinson(r, order, axis = -1):
    """Levinson-Durbin recursion, to efficiently solve symmetric linear systems
    with toeplitz structure.

    Arguments
    ---------
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
    --------
        a : array-like
            the solution of the inversion (see notes).
        e : array-like
            the prediction error.
        k : array-like
            reflection coefficients.

    Notes
    -----
    Levinson is a well-known algorithm to solve the Hermitian toeplitz
    equation:

                       _          _
        -R[1] = R[0]   R[1]   ... R[p-1]    a[1]
         :      :      :          :      *  :
         :      :      :          _      *  :
        -R[p] = R[p-1] R[p-2] ... R[0]      a[p]
                       _
    with respect to a (  is the complex conjugate). Using the special symmetry
    in the matrix, the inversion can be done in O(p^2) instead of O(p^3).

    """
    if axis != -1:
        r = np.swapaxes(r, -1)
    a, e, k = c_levinson(r, order)
    if axis != -1:
        a = np.swapaxes(a, -1)
        e = np.swapaxes(e, -1)
        k = np.swapaxes(k, -1)
    return a, e, k
