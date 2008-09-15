###################
 scikits.talkbox
###################

.. htmlonly::

    :Release: |version|
    :Date: |today|

Welcome to talkbox documentation
--------------------------------

Talkbox is set of python modules for speech/signal processing. The goal of this
toolbox is to be a sandbox for features which may end up in scipy at some
point. The following features are planned before a 1.0 release:

    * Spectrum estimation related functions: both parametic (lpc, high
      resolution methods like music and co), and non-parametric (Welch,
      periodogram)
    * Fourier-like transforms (DCT, DST, MDCT, etc...)
    * Basic signal processing tasks such as resampling
    * Speech related functionalities: mfcc, mel spectrum, etc..
    * More as it comes

I want talkbox to be useful for both research and educational purpose. As such,
a requirement is to have a pure python implementation for everything, with
optional C/C++/Lisp for speed: reading signal processing in C is no fun, and
neither is waiting for your mfcc computation one hour before ICASSP submission
deadline :).

.. toctree::
   :maxdepth: 2

   intro
   spectral
   lpc

.. htmlonly::

  * :ref:`genindex`
  * :ref:`modindex`
  * :ref:`search`
