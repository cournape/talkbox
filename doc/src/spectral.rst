Spectral analysis
=================

Spectral signal analysis is the field concerned with the estimation of the
distribution of a signal (more exactly its power) in the frequency domain.
talkbox has several methods to do spectral analysis, both parametric (with an
underlying signal model) and non-parametric (more general but less efficient
than parametric methods if the later are applicable).

First, since spectral analysis is usually done on stationary signals, let us
remind a few definitions on stationarity for stochastic processes

Stationary signals
------------------

A random signal X is said to be (strictly) stationary if its distribution does
not depend on the time. For time-discrete signals X[n], this is written:

.. math:: \forall n, k, \mathbb{P}[X[n]] = \mathbb{P}[X[n-k]]

Weaker stationarity can be defined, when only some moments of the signal do not
depend on time. A widely used concept it weakly stationary signals.  A signal
is said to be weakly stationary if it means and covariance do not depend on
time, and its covariance function :math:\gamma(n, k) depends only on the time
difference n-k: 

.. math:: \forall n, k, \gamma(n, k) = \mathbb{E}[(X[n]-m)(X[k] -m)] = \gamma(n-k)

Power Spectrum Density
----------------------

TODO: blob on ESD vs PSD.

.. The most commonly used measure of energy distribution in the frequency domain
   is the Power Spectrum Density (PSD). For signal s(t) of power P = s^2, the PSD
   is the Fourier Transform of P. Unfortunately, signals with nonzero average
   power <P> are not square integrable; in the case of stationary signals in the
   wide-sense, the Wiener-Khinchin theorem guarantees that

Non-parametric
--------------

Periodogram
^^^^^^^^^^^

.. autofunction:: scikits.talkbox.spectral.basic.periodogram

Parametric
----------

ar method
^^^^^^^^^
