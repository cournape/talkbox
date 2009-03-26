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
educational purpose and reproducibility - and optional C for speed."""

DISTNAME            = 'scikits.talkbox'
DESCRIPTION         = 'Talkbox, a set of python modules for speech/signal processing'
LONG_DESCRIPTION    = descr
MAINTAINER          = 'David Cournapeau',
MAINTAINER_EMAIL    = 'david@ar.media.kyoto-u.ac.jp',
URL                 = 'http://projects.scipy.org/scipy/scikits'
LICENSE             = 'MIT'
DOWNLOAD_URL        = URL

MAJOR = 0
MINOR = 2
MICRO = 3
DEV = False

CLASSIFIERS = [ 'Development Status :: 1 - Planning',
              'Environment :: Console',
              'Intended Audience :: Developers',
              'Intended Audience :: Science/Research',
              'License :: OSI Approved :: BSD License',
              'Topic :: Scientific/Engineering']

def build_verstring():
    return '%d.%d.%d' % (MAJOR, MINOR, MICRO)

def build_fverstring():
    if DEV:
        return build_verstring() + '.dev'
    else:
        return build_verstring()

def write_version(fname):
    f = open(fname, "w")
    f.write("""
short_version='%s'
version=short_version
dev=%s
if dev:
    version += '.dev'
""" % (build_verstring(), DEV))
    f.close()

VERSION = build_fverstring()
INSTALL_REQUIRE = 'numpy'
