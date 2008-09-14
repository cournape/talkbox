#! /usr/bin/env python
# Last Change: Sun Sep 14 05:00 PM 2008 J

# Copyright (C) 2008 Cournapeau David <cournape@gmail.com>

descr   = """Talkbox, to make your numpy environment speech aware !

This is set of python modules for speech/signal processing. The goal of this
toolbox is to be a sandbox for features which may end up in scipy at some
point. I want to implement the following features:

    * Spectrum estimation related functions: both parametic (lpc, high
    resolution methods like music and co), and non-parametric (Welch,
    periodogram) will be implemented
    * Basic signal processing tasks such as resampling
    * Speech related functionalities: mfcc, mel spectrum, etc..
    * More as it comes

The 'vision' is to have a pure python implementation for everything, with
optional C/C++/Lisp for speed, because I want this to be educational and
useful: reading signal processing in C is no fun, and neither is waiting for
your mfcc computation one hour before ICASSP submission deadline :)."""

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
        version = '0.0.1',
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
