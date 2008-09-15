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

.. latex::
    <x - p(x), x^-1> = 0
    <x - p(x), x^-k> = 0

And:

    <x - p(x), x> = <x, x>>
