Spectral analysis
=================

Spectral signal analysis is the field concerned with the estimation of the
distribution of a signal (more exactly its power) in the frequency domain.

The Power Spectrum Density (PSD) :math:`S_X` of :math:`X_n` is defined as the
squared discrete time Fourier transform of :math:`X_n`

.. math:: \forall f \in \mathbb{R}, \qquad 
        S_X = \left|{\sum_n{X_n e^{-2\pi j f n}}}\right|^2

Under suitable technical conditions, this is equal to the discrete time Fourier
transform of the autocorrelation function for stationary signals in the wide
sense:

.. math:: \forall f \in \mathbb{R}, \qquad S_X = \sum_n{\gamma(n) e^{-2\pi j f n}}

This is called the power spectrum density because integrating it over the
frequency domain gives you the average power of :math:`X` and because it can be
proved that :math:`S_X` is always positive for any :math:`f`.

Spectral density estimation
---------------------------

Since in practice, we only have finite signals, we need method to estimate the
PSD. talkbox implements various methods for PSD estimation, which are
classified in two broad classes:

        * non-parametric (general methods, estimate the PSD directly from the
          signal)
        * parametric (use an underlying signal model, for example AR; is less
          general, but generally more efficient in some sense if applicable).

Non-parametric estimation
-------------------------

Periodogram
^^^^^^^^^^^

The raw periodogram is a relatively straightforward estimator of the PSD. The
raw periodogram of a signal of length `n` is defined as:

.. math:: \forall k=0,\ldots,n-1, \qquad I(k/n) \triangleq 
	  n |{dft(k/n)}|^2 = \frac{1}{n}|{\sum_k{x[k] e^{-2\pi j k / n}}}^2|

where dft is the Discrete Fourier Transform.

.. autofunction:: scikits.talkbox.spectral.basic.periodogram

Parametric estimation
---------------------

ar method
^^^^^^^^^

Useful complements
------------------

A random signal :math:`X` is said to be (strictly) stationary if its
distribution does not depend on the time. For time-discrete signals :math:`X_n`
of distribution :math:`F_{X_n}` , this is written:

.. math:: \forall n, k, \qquad F_{X_n} = F_{X_{n+k}}

Other stationary concepts can be defined, when only some moments of the
signal do not depend on time. A widely used concept is weakly stationary
signals. A signal is said to be weakly stationary (or stationary in the wide
sense) if its means and covariance do not depend on time, and its covariance
function :math:`\gamma(n, k)` depends only on the time difference n-k:

.. math:: \forall n, k, \qquad \gamma(n, k) = 
          \mathbb{E}[(X[n]-m)(X[k] -m)] = \gamma(n-k)

