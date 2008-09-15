Introduction
============

Talkbox is a set of python modules to extend basic numpy/scipy capabilities for
signal and speech/audio processing. The focus is on getting python
implementation for every used algorithm, with optional C code where it makes
sense, so that it can be used both as a reference for algorithms (python code)
and reasonably sized problems (C code).

Prerequisites
-------------

Talkbox needs at least **Python 2.4** to run. It also needs Numpy_ and Scipy_,
as well as setuptools. Any recent version of numpy (1.0 and higher), scipy (0.6
and higher) should do.

.. _Numpy: http://www.scipy.org
.. _Scipy: http://www.scipy.org

Starting with talkbox
=====================

main namespace
--------------

The main functions are available through the main scikits.talkbox namespace:

.. code-block:: python
   :linenos:

    import scikits.talkbox as talk

Getting help
------------

All high level functions are duely documented, and are available through the
usual python facilities:

.. code-block:: python
   :linenos:

    import scikits.talkbox as talk
    help(talk)

Will give you online-help for the main talkbox functions.
