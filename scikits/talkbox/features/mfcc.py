import numpy as np

from scipy.io import loadmat
from scipy.signal import lfilter, hamming
from scipy.fftpack import fft
from scipy.fftpack.realtransforms import dct2

from scikits.talkbox import segment_axis

from mel import hz2mel

def mfcc(input, nwin=256, nfft=512, fs=16000, nceps=13):
    # MFCC parameters: taken from auditory toolbox
    over = nwin - 160
    prefac = 0.97

    #lowfreq = 400 / 3.
    lowfreq = 133.33
    #highfreq = 6855.4976
    linsc = 200/3.
    logsc = 1.0711703

    nlinfil = 13
    nlogfil = 27
    nfil = nlinfil + nlogfil

    w = hamming(nwin, sym=0)

    #------------------------
    # Compute the filter bank
    #------------------------
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

    #------------------
    # Compute the MFCC 
    #------------------
    extract = preemp(input, prefac)
    framed = segment_axis(extract, nwin, over) * w

    # Compute the spectrum magnitude
    spec = np.abs(fft(framed, nfft, axis=-1))
    # Filter the spectrum trhough the triangle filterbank
    espec = np.log10(np.dot(spec, fbank.T))
    # Use the DCT to 'compress' the coefficients (spectrum -> cepstrum domain)
    ceps = dct2(espec, norm='ortho', axis=-1)[:, :nceps]

    return ceps

def preemp(input, p):
    """Pre-emphasis filter."""
    return lfilter([1., -p], 1, input)

if __name__ == '__main__':
    extract = loadmat('extract.mat')['extract']
    ceps = mfcc(extract)
