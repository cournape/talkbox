Introduction
============

The following document describes how to use the talkbox scikits for signal
processing. The document assumes basic knowledge of signal processing (Fourier
Transform, Linear Time Invariant systems).

Talkbox is set of python modules for speech/signal processing. The following features are planned before a 1.0 release:

    * Spectrum estimation related functions: both parametic (lpc, high
      resolution methods like music and co), and non-parametric (Welch,
      periodogram)
    * Fourier-like transforms (DCT, DST, MDCT, etc...)
    * Basic signal processing tasks such as resampling
    * Speech related functionalities: mfcc, mel spectrum, etc..
    * More as it comes

The goal of this toolbox is to be a sandbox for features which may end up in
scipy at some point. I also want talkbox to be useful for both research and
educational purpose. As such, a requirement is to have a pure python
implementation for everything, with optional C/C++/Lisp for speed: reading
signal processing in C is no fun, and neither is waiting for your mfcc
computation one hour before ICASSP submission deadline :).

Prerequisites
-------------

Talkbox needs at least **Python 2.4** to run. It also needs Numpy_ and Scipy_,
as well as setuptools. Any recent version of numpy (1.0 and higher), scipy (0.6
and higher) should do.

.. _Numpy: http://www.scipy.org
.. _Scipy: http://www.scipy.org

Other useful packages are matplotlib, and audiolab scikits. They are not
mandatory, but will be assumed for the examples in this documentation.

Installing talkbox
------------------

Unfortunately, at this point, your only option is to install talkbox from
sources:

.. code-block:: python
        :linenos:

        svn co http://svn.scipy.org/svn/scikits/trunk/talkbox

You can install talkbox with the usual setup.py method in the talkbox source
tree:

.. code-block:: python
        :linenos:

        python setup.py install

If you don't want to install it as a python egg (for stow, etc...), you can use:

.. code-block:: python
        :linenos:

        python setup.py install --single-version-externally-managed --record=/dev/null

Starting with talkbox
---------------------

main namespace
^^^^^^^^^^^^^^

The main functions are available through the main scikits.talkbox namespace::

    import scikits.talkbox as talk

Getting help
^^^^^^^^^^^^

All high level functions are duely documented, and are available through the
usual python facilities::

    import scikits.talkbox as talk
    help(talk)

Will give you online-help for the main talkbox functions.
