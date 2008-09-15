Spectral analysis
=================

Spectral signal analysis is the field concerned with the estimation of the
distribution of a signal (more exactly its power) in the frequency domain.

Stationary signals
------------------

Spectral analysis is usually done in stationary signals. A random signal X is
said to be (strictly) stationary if its distribution does not depend on the
time.

TODO: wide-sense stationarity and co.

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

.. autofunction:: scikits.talkbox.spectral.basic.periodogram

Parametric
----------
