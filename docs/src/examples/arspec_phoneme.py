import numpy as np
import matplotlib.pylab as plt

from scikits.audiolab import wavread
from scikits.samplerate import resample

from scikits.talkbox.spectral.basic import periodogram, arspec

a, fs = wavread('voice-womanKP-01.wav')[:2]

fr = 4000.
ra = resample(a, fr / fs)

frame = ra[500:500+256]
px, fx = periodogram(frame, 2048, fr)
plt.grid(True)
plt.plot(fx, 10 * np.log10(px))

apx, afx = arspec(frame, 12, 2048, fr)
plt.plot(afx, 10 * np.log10(apx))
