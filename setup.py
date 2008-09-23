#! /usr/bin/env python
# Last Change: Tue Sep 23 04:00 PM 2008 J

# Copyright (C) 2008 Cournapeau David <cournape@gmail.com>

descr   = """Talkbox, to make your numpy environment speech aware !

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
a requirement is to have a pure python implementation for everything - for
educational purpose and reproducibility - and optional C/C++/Lisp for speed -
because waiting for your mfcc computation one hour before ICASSP submission
deadline :)."""

import os
import sys

DISTNAME            = 'scikits.talkbox'
DESCRIPTION         = 'Talkbox, a set of python modules for speech/signal processing'
LONG_DESCRIPTION    = descr
MAINTAINER          = 'David Cournapeau',
MAINTAINER_EMAIL    = 'david@ar.media.kyoto-u.ac.jp',
URL                 = 'http://projects.scipy.org/scipy/scikits'
LICENSE             = 'MIT'
DOWNLOAD_URL        = URL

import setuptools
from numpy.distutils.core import setup

def configuration(parent_package='', top_path=None):
    if os.path.exists('MANIFEST'): os.remove('MANIFEST')

    from numpy.distutils.misc_util import Configuration
    config = Configuration(None, parent_package, top_path,
        maintainer  = MAINTAINER,
        maintainer_email = MAINTAINER_EMAIL,
        description = DESCRIPTION,
        license = LICENSE,
        url = URL,
        download_url = DOWNLOAD_URL,
        long_description = LONG_DESCRIPTION)

    #config.set_options(
    #            ignore_setup_xxx_py=True,
    #            assume_default_configuration=True,
    #            delegate_options_to_subpackages=True,
    #            quiet=True,
    #)

    config.add_subpackage('scikits')
    config.add_subpackage(DISTNAME)
    #config.add_data_files('scikits/__init__.py')

    return config

if __name__ == "__main__":
    setup(configuration = configuration,
        name = DISTNAME,
        install_requires = 'numpy',
        namespace_packages = ['scikits'],
        packages = setuptools.find_packages(),
        version = '0.2dev',
        include_package_data = True,
        #test_suite="tester", # for python setup.py test
        zip_safe = True, # the package can run out of an .egg file
        classifiers =
            [ 'Development Status :: 1 - Planning',
              'Environment :: Console',
              'Intended Audience :: Developers',
              'Intended Audience :: Science/Research',
              'License :: OSI Approved :: BSD License',
              'Topic :: Scientific/Engineering'],
    )
