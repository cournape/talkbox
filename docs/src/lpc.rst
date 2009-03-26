Linear Prediction
=================

The goal of linear-prediction is to model a signal as a linear combination of
its past/future.

Yule-Walker equations
---------------------

For a discrete-time signal x, we want to approximate the sample x[n] as a
linear combination xp[n] of the k preceding samples:

    xp[n] = -c[1] * x[n-2] - ... - c[k-1] * x[n-k-1]

The best approximation in the mean-square sense is a tuple(c[1], ..., c[k])
such as the squared error:

    e = xp - x

Is minimal. Noting p(x) = xp, and x^{-k} the signal x^{-k}[n] = x[n-k], since p
is a linear combination of the (x^-1, ..., x^-k), we know that the error p(x) -
x is minimal for p the orthogonal project of x on the vector space V spanned by
the x^-1, ..., x^-k. In particular, the error e is then orthogonal to any
vector in V:

.. .. latex::
..     <x - p(x), x^-1> = 0
..     <x - p(x), x^-k> = 0
..
.. And:
..
..     <x - p(x), x> = <x, x>>

TODO: decent blob for above

.. math:: 

        \begin{pmatrix}
                -R[1] \\ 
                -R[2] \\ 
                \vdots \\ 
                -R[p] 
        \end{pmatrix}
        = 
        \begin{pmatrix}
                R[0]    & \overline{R}[1] & \dots  & \overline{R}[p-1] \\ 
                R[1]    & R[0]            & \ddots & \vdots \\
                \vdots  & \ddots          & \ddots & \overline{R}[1]\\
                R[p-1]  & \dots           & R[1]   & R[0]
        \end{pmatrix}
        \begin{pmatrix}
                a[1] \\
                \vdots \\
                \vdots \\
                a[p]
        \end{pmatrix}

Levinson-Durbin recursion
-------------------------

Levinson-Durbin recursion is a recursive algorithm to solve the Yule-Walker
equations in O(p^2) instead of O(p^3) usually necessary to inverse a matrix. It
uses the Hermitian-Toeplitz structure of the correlation matrix.

.. autofunction:: scikits.talkbox.levinson

Linear prediction coding
------------------------

Solve the Yule-Walker equation for a signal x, using the autocorelation method
and Levinson-Durbin for the Yule-Walker inversion.

.. autofunction:: scikits.talkbox.lpc
