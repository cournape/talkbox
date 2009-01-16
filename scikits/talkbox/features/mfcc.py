import numpy as np

from scipy.io import loadmat
from scipy.signal import lfilter, hamming
from scipy.fftpack import fft
from scipy.fftpack.realtransforms import dct2

from scikits.talkbox import segment_axis

from mel import hz2mel

def mfcc(frame):
    pass

def preemp(input, p):
    """Pre-emphasis filter."""
    return lfilter([1., -p], 1, input)

# MFCC parameters: taken from auditory toolbox
nwin = 256
over = nwin - 160
prefac = 0.97
nfft = 512
fs = 16000

#lowfreq = 400 / 3.
lowfreq = 133.33
#highfreq = 6855.4976
linsc = 200/3.
logsc = 1.0711703

nlinfil = 13
nlogfil = 27
nfil = nlinfil + nlogfil

# Compute start/middle/end points of the triangular filters
freqs = np.zeros(nfil+2)
freqs[:nlinfil] = lowfreq + np.arange(nlinfil) * linsc
freqs[nlinfil:] = freqs[nlinfil-1] * logsc ** np.arange(1, nlogfil + 3)
heights = 2./(freqs[2:] - freqs[0:-2])

# Compute filterbank coeff (in fft domain, in bins)
fbank = np.zeros((nfil, nfft))
# FFT bins (in Hz)
nfreqs = np.arange(nfft) / (1. * nfft) * fs
for i in range(nfil):
    low = freqs[i]
    cen = freqs[i+1]
    hi = freqs[i+2]

    lid = np.arange(np.floor(low * nfft / fs) + 1,
                    np.floor(cen * nfft / fs) + 1, dtype=np.int)
    lslope = heights[i] / (cen - low)
    rid = np.arange(np.floor(cen * nfft / fs) + 1,
                    np.floor(hi * nfft / fs) + 1, dtype=np.int)
    rslope = heights[i] / (hi - cen)
    fbank[i][lid] = lslope * (nfreqs[lid] - low)
    fbank[i][rid] = rslope * (hi - nfreqs[rid])

extract = loadmat('extract.mat')['extract']
extract = preemp(extract, prefac)
framed = segment_axis(extract, nwin, over)
w = hamming(nwin)

ceps = np.empty((framed.shape[0], nfil))
for i in range(framed.shape[0]):
    frame = framed[i] * w
    spec = np.abs(fft(frame, nfft))
    espec = np.log10(np.dot(fbank, spec))
    ceps[i] = dct2(espec)
